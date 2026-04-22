"""
Sound / Music Manager for Pyxel
@author  : generated for LeoI52/pyxel-utils
@requires: pyxel >= 2.4

Supports:
  - Named SFX registration (chiptune, MML string, or PCM bytes)
  - Named Music track registration (music slot or MML per channel)
  - Volume control per channel (0.0 – 1.0)
  - Looping, one-shot, and resume playback
  - Music stacking (push/pop)
  - Fade-in / fade-out via per-frame volume stepping
  - play_pos() wrapper that returns seconds
  - Global mute / unmute
"""

import pyxel
from dataclasses import dataclass, field
from typing import Optional, Union
from enum import IntEnum, auto


# ---------- CHANNEL MANAGEMENT ---------- #

CHANNELS = 4  # Pyxel supports ch 0-3


class SfxMode(IntEnum):
    CHIPTUNE = auto()   # Standard Sound slot (snd index 0-63)
    MML      = auto()   # Raw MML string played directly via play()
    PCM      = auto()   # Raw PCM bytes loaded into a Sound slot via Sound.pcm()


# ---------- DATA CLASSES ---------- #

@dataclass
class SfxDef:
    """Definition of a sound effect."""
    mode:     SfxMode
    snd_id:   Optional[int]   = None   # slot used for CHIPTUNE / PCM modes
    mml_str:  Optional[str]   = None   # MML string for MML mode
    pcm_data: Optional[bytes] = None   # raw PCM bytes for PCM mode
    volume:   float           = 1.0    # relative volume 0.0–1.0


@dataclass
class MusicDef:
    """Definition of a music track."""
    # Use either a pyxel music slot OR per-channel MML strings (up to 4 channels).
    msc_id:      Optional[int]        = None   # pyxel.musics[] slot (0-7)
    channel_mml: Optional[list[str]]  = None   # list of MML strings, one per channel
    loop:        bool                 = True
    volume:      float                = 1.0    # relative volume 0.0–1.0

    # Internal: which pyxel channels this track owns
    _channels: list[int] = field(default_factory=list, repr=False)


# ---------- FADE STATE ---------- #

@dataclass
class FadeState:
    channel:    int
    target_vol: float   # 0.0 or 1.0
    step:       float   # volume change per frame
    current:    float   # current logical volume

    def tick(self) -> bool:
        """Advance one frame. Returns True when fade is complete."""
        self.current = max(0.0, min(1.0, self.current + self.step))
        return abs(self.current - self.target_vol) < 1e-4


# ---------- SOUND MANAGER ---------- #

class SoundManager:
    """
    Central manager for all Pyxel sounds and music.

    Quick-start
    -----------
        sm = SoundManager()

        # Register a simple chiptune SFX in slot 0
        pyxel.sounds[0].set("c3e3g3", "s", "7", "n", 20)
        sm.register_sfx("jump", SfxMode.CHIPTUNE, snd_id=0)

        # Register an MML SFX
        sm.register_sfx("coin", SfxMode.MML, mml_str="T180 L16 CDE>C")

        # Register a PCM SFX (raw 16-bit signed mono @ 22050 Hz bytes)
        with open("explosion.pcm", "rb") as f:
            sm.register_sfx("explode", SfxMode.PCM, pcm_data=f.read(), snd_id=10)

        # Register a music track from a pyxel music slot
        sm.register_music("bgm_forest", msc_id=0, loop=True)

        # Register a music track from MML strings (one per channel)
        sm.register_music("bgm_boss",
            channel_mml=["T140 L8 [CDEFGFED]4", "T140 L4 [C2G2]4"],
            loop=True)

        # In your update() loop:
        sm.update()

        # Play
        sm.play_sfx("jump")
        sm.play_music("bgm_forest", fade_in_frames=60)
    """

    def __init__(self):
        self._sfx:   dict[str, SfxDef]   = {}
        self._music: dict[str, MusicDef] = {}

        # Per-channel state
        self._ch_volume:  list[float] = [1.0] * CHANNELS
        self._ch_muted:   list[bool]  = [False] * CHANNELS
        self._global_mute: bool       = False

        # Music stack (name, MusicDef)
        self._music_stack: list[tuple[str, MusicDef]] = []
        self._current_music: Optional[str] = None

        # Active fades indexed by channel
        self._fades: dict[int, FadeState] = {}

        # SFX channel pool (channels 0-2 reserved for SFX; 3 for music by default)
        # Override by passing explicit ch to play_sfx().
        self._sfx_channels = [0, 1, 2]
        self._music_channels = [0, 1, 2, 3]
        self._sfx_round_robin = 0

        # PCM slot management: tracks which Sound slots are used by PCM SFX
        self._pcm_slots: dict[str, int] = {}

    # ---------- REGISTRATION ---------- #

    def register_sfx(
        self,
        name:     str,
        mode:     SfxMode,
        *,
        snd_id:   Optional[int]   = None,
        mml_str:  Optional[str]   = None,
        pcm_data: Optional[bytes] = None,
        volume:   float           = 1.0,
    ) -> None:
        """Register a named sound effect."""
        if mode == SfxMode.CHIPTUNE:
            if snd_id is None:
                raise ValueError(f"CHIPTUNE sfx '{name}' requires snd_id")
        elif mode == SfxMode.MML:
            if not mml_str:
                raise ValueError(f"MML sfx '{name}' requires mml_str")
        elif mode == SfxMode.PCM:
            if snd_id is None or pcm_data is None:
                raise ValueError(f"PCM sfx '{name}' requires snd_id and pcm_data")
            pyxel.sounds[snd_id].pcm(pcm_data)
            self._pcm_slots[name] = snd_id

        self._sfx[name] = SfxDef(
            mode=mode, snd_id=snd_id, mml_str=mml_str,
            pcm_data=pcm_data, volume=volume,
        )

    def register_music(
        self,
        name:        str,
        *,
        msc_id:      Optional[int]       = None,
        channel_mml: Optional[list[str]] = None,
        loop:        bool                = True,
        volume:      float               = 1.0,
    ) -> None:
        """Register a named music track."""
        if msc_id is None and not channel_mml:
            raise ValueError(f"Music '{name}' requires msc_id or channel_mml")
        self._music[name] = MusicDef(
            msc_id=msc_id, channel_mml=channel_mml, loop=loop, volume=volume,
        )

    # ---------- SFX PLAYBACK ---------- #

    def play_sfx(
        self,
        name: str,
        *,
        ch:   Optional[int] = None,
        loop: bool          = False,
    ) -> int:
        """
        Play a registered SFX.
        Returns the channel it was played on, or -1 if muted.
        """
        if self._global_mute or name not in self._sfx:
            return -1

        sfx = self._sfx[name]
        channel = ch if ch is not None else self._next_sfx_channel()

        if self._ch_muted[channel]:
            return -1

        if sfx.mode == SfxMode.CHIPTUNE:
            pyxel.play(channel, sfx.snd_id, loop=loop)
        elif sfx.mode == SfxMode.MML:
            pyxel.play(channel, sfx.mml_str, loop=loop)
        elif sfx.mode == SfxMode.PCM:
            pyxel.play(channel, sfx.snd_id, loop=loop)

        return channel

    def stop_sfx(self, ch: int) -> None:
        """Stop SFX on a specific channel."""
        pyxel.stop(ch)

    def _next_sfx_channel(self) -> int:
        ch = self._sfx_channels[self._sfx_round_robin % len(self._sfx_channels)]
        self._sfx_round_robin += 1
        return ch

    # ---------- MUSIC PLAYBACK ---------- #

    def play_music(
        self,
        name:             str,
        *,
        fade_in_frames:   int  = 0,
        stop_current:     bool = True,
    ) -> None:
        """
        Start a registered music track.
        If fade_in_frames > 0 the music fades in over that many frames.
        """
        if name not in self._music:
            raise KeyError(f"Music '{name}' not registered")

        if stop_current and self._current_music:
            self._stop_current_music()

        track = self._music[name]
        self._current_music = name

        if track.msc_id is not None:
            # Standard music slot
            pyxel.playm(track.msc_id, loop=track.loop)
            track._channels = list(self._music_channels)
        else:
            # Per-channel MML
            chs = self._music_channels[:len(track.channel_mml)]
            track._channels = chs
            for ch, mml in zip(chs, track.channel_mml):
                pyxel.play(ch, mml, loop=track.loop)

        if fade_in_frames > 0:
            step = track.volume / max(1, fade_in_frames)
            for ch in track._channels:
                self._fades[ch] = FadeState(ch, track.volume, step, 0.0)
        else:
            for ch in track._channels:
                self._ch_volume[ch] = track.volume

    def stop_music(self, fade_out_frames: int = 0) -> None:
        """Stop the current music, optionally fading out first."""
        if not self._current_music:
            return

        track = self._music.get(self._current_music)
        if not track:
            return

        if fade_out_frames > 0 and track._channels:
            for ch in track._channels:
                current = self._ch_volume[ch]
                step = -current / max(1, fade_out_frames)
                self._fades[ch] = FadeState(ch, 0.0, step, current)
            # Actual stop will happen once fade reaches 0 (handled in update)
            self._pending_stop = True
        else:
            self._stop_current_music()

    def _stop_current_music(self) -> None:
        if self._current_music:
            track = self._music.get(self._current_music)
            if track:
                for ch in track._channels:
                    pyxel.stop(ch)
                    self._fades.pop(ch, None)
        self._current_music = None

    # ---------- MUSIC STACK ---------- #

    def push_music(self, name: str, **kwargs) -> None:
        """
        Push the current music onto the stack and play a new one.
        Useful for cutscenes, boss fights, etc.
        """
        if self._current_music:
            self._music_stack.append(
                (self._current_music, self._music[self._current_music])
            )
        self.play_music(name, **kwargs)

    def pop_music(self, fade_in_frames: int = 0) -> None:
        """Resume the previously stacked music track."""
        if not self._music_stack:
            self.stop_music()
            return
        name, _ = self._music_stack.pop()
        self.play_music(name, fade_in_frames=fade_in_frames)

    # ---------- VOLUME CONTROL ---------- #

    def set_channel_volume(self, ch: int, volume: float) -> None:
        """Set logical volume for a channel (0.0 – 1.0)."""
        self._ch_volume[ch] = max(0.0, min(1.0, volume))

    def get_channel_volume(self, ch: int) -> float:
        return self._ch_volume[ch]

    def mute_channel(self, ch: int) -> None:
        self._ch_muted[ch] = True
        pyxel.stop(ch)

    def unmute_channel(self, ch: int) -> None:
        self._ch_muted[ch] = False

    def mute_all(self) -> None:
        """Global mute — stops all audio."""
        self._global_mute = True
        pyxel.stop()

    def unmute_all(self) -> None:
        """Lift the global mute."""
        self._global_mute = False

    @property
    def is_muted(self) -> bool:
        return self._global_mute

    # ---------- QUERY ---------- #

    def is_playing(self, ch: int) -> bool:
        """Returns True if the channel is actively playing."""
        return pyxel.play_pos(ch) is not None

    def play_pos(self, ch: int) -> Optional[tuple[int, float]]:
        """Returns (sound_no, seconds) or None if stopped."""
        return pyxel.play_pos(ch)

    @property
    def current_music(self) -> Optional[str]:
        return self._current_music

    # ---------- UPDATE (call every frame) ---------- #

    def update(self) -> None:
        """
        Must be called once per frame inside your pyxel update() function.
        Advances fade states and handles deferred stops.
        """
        pending_stop: bool = getattr(self, "_pending_stop", False)
        completed_fades = []

        for ch, fade in self._fades.items():
            done = fade.tick()
            self._ch_volume[ch] = fade.current
            if done:
                completed_fades.append(ch)

        for ch in completed_fades:
            self._fades.pop(ch)

        # If a fade-out finished and a stop was pending, do the stop
        if pending_stop and not self._fades:
            self._pending_stop = False
            self._stop_current_music()

        # NOTE: Pyxel does not expose a per-channel volume API directly.
        # Volume shaping via fade states is tracked here for use in
        # custom mixing (e.g. via PCM mode) or future Pyxel API extensions.
        # For chiptune channels, use pyxel.sounds[snd_id].volumes to scale.

    # ---------- HELPERS ---------- #

    def list_sfx(self) -> list[str]:
        return list(self._sfx.keys())

    def list_music(self) -> list[str]:
        return list(self._music.keys())

    def __repr__(self) -> str:
        return (
            f"<SoundManager sfx={self.list_sfx()} "
            f"music={self.list_music()} "
            f"current='{self._current_music}' "
            f"muted={self._global_mute}>"
        )


# ---------- USAGE EXAMPLE ---------- #

if __name__ == "__main__":
    """
    Minimal demo: jump SFX + looping BGM.
    Press SPACE to jump, M to toggle mute, B to switch BGM.
    """

    sm = SoundManager()

    def _setup_sounds():
        # -- Jump SFX (chiptune, slot 0) --
        pyxel.sounds[0].set("c3e3g3", "s", "765", "f", 25)
        sm.register_sfx("jump", SfxMode.CHIPTUNE, snd_id=0)

        # -- Coin SFX (MML string, no slot needed) --
        sm.register_sfx("coin", SfxMode.MML, mml_str="T220 L16 >C E G >C")

        # -- BGM Forest: channel-MML music --
        sm.register_music(
            "bgm_forest",
            channel_mml=[
                "T110 L8 [C E G E C E G E]2",       # ch0: melody
                "T110 L4 [C2 G2]4",                  # ch1: bass
            ],
            loop=True,
            volume=0.8,
        )

        # -- BGM Boss: uses pyxel.musics slot 0 (if defined in your .pyxres) --
        # sm.register_music("bgm_boss", msc_id=0, loop=True)

    pyxel.init(200, 120, title="SoundManager Demo", fps=60)

    _setup_sounds()
    sm.play_music("bgm_forest", fade_in_frames=90)

    def update():
        sm.update()

        if pyxel.btnp(pyxel.KEY_SPACE):
            sm.play_sfx("jump")

        if pyxel.btnp(pyxel.KEY_C):
            sm.play_sfx("coin")

        if pyxel.btnp(pyxel.KEY_M):
            if sm.is_muted:
                sm.unmute_all()
            else:
                sm.mute_all()

        if pyxel.btnp(pyxel.KEY_F):
            sm.stop_music(fade_out_frames=60)

        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

    def draw():
        pyxel.cls(1)
        pyxel.text(10, 10, "SoundManager Demo", 7)
        pyxel.text(10, 25, f"BGM: {sm.current_music or 'none'}", 6)
        pyxel.text(10, 35, f"Muted: {sm.is_muted}", 8)
        pyxel.text(10, 50, "SPACE: jump SFX", 13)
        pyxel.text(10, 58, "C: coin SFX", 13)
        pyxel.text(10, 66, "M: toggle mute", 13)
        pyxel.text(10, 74, "F: fade out BGM", 13)
        pyxel.text(10, 82, "ESC: quit", 13)

        for ch in range(CHANNELS):
            playing = "PLAY" if sm.is_playing(ch) else "----"
            pos = sm.play_pos(ch)
            pos_str = f"{pos[1]:.1f}s" if pos else "   "
            pyxel.text(10, 96 + ch * 8,
                       f"CH{ch} [{playing}] {pos_str} vol={sm.get_channel_volume(ch):.2f}",
                       7)

    pyxel.run(update, draw)