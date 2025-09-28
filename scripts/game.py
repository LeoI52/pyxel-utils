"""
@author : Léo Imbert
@created : 15/10/2024
@updated : 28/09/2025

pyxel.load(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), self.__current_scene.pyxres_path))

TODO :
- Change scene reloads
"""

from tweening import Tween
from particles import *
from gui import Text
from vars import *
import random
import pyxel
import math
import time

class Transition:

    def __init__(self, new_scene_id:int, speed:int, transition_color:int, new_camera_x:int=0, new_camera_y:int=0, action=None):
        self.new_scene_id = new_scene_id
        self.speed = speed
        self.transition_color = transition_color
        self.new_camera_x = new_camera_x
        self.new_camera_y = new_camera_y
        self.action = action
        self.direction = 1

class TransitionDither(Transition):

    def __init__(self, new_scene_id:int, duration:float, transition_color:int, new_camera_x:int=0, new_camera_y:int=0, action=None, fps:int=60):
        super().__init__(new_scene_id, 1 / (duration / 2 * fps), transition_color, new_camera_x, new_camera_y, action)
        self.dither = 0

    def update(self, pyxel_manager):
        self.dither += self.speed * self.direction

        if self.dither > 1 and self.direction == 1:
            self.direction = -1
            pyxel_manager.change_scene(self.new_scene_id, self.new_camera_x, self.new_camera_y, self.action)
        if self.dither < 0 and self.direction == -1:
            pyxel_manager.finish_transition()
            return

    def draw(self, pyxel_manager):
        pyxel.dither(self.dither)
        pyxel.rect(pyxel_manager.camera_x, pyxel_manager.camera_y, pyxel.width, pyxel.height, self.transition_color)
        pyxel.dither(1)

class TransitionCircle(Transition):

    def __init__(self, new_scene_id:int, duration:float, transition_color:int, new_camera_x:int=0, new_camera_y:int=0, action=None, fps:int=60):
        self.radius = 0
        self.max_radius = math.hypot(pyxel.width, pyxel.height) / 2
        super().__init__(new_scene_id, self.max_radius / (duration / 2 * fps), transition_color, new_camera_x, new_camera_y, action)

    def update(self, pyxel_manager):
        self.radius += self.speed * self.direction

        if self.radius > self.max_radius and self.direction == 1:
            self.direction = -1
            pyxel_manager.change_scene(self.new_scene_id, self.new_camera_x, self.new_camera_y, self.action)
        if self.radius < 0 and self.direction == -1:
            pyxel_manager.finish_transition()
            return

    def draw(self, pyxel_manager):
        pyxel.circ(pyxel_manager.camera_x + pyxel.width / 2, pyxel_manager.camera_y + pyxel.height / 2, self.radius, self.transition_color)

class TransitionClosingDoors(Transition):

    def __init__(self, new_scene_id:int, duration:float, transition_color:int, new_camera_x:int=0, new_camera_y:int=0, action=None, fps:int=60):
        super().__init__(new_scene_id, pyxel.width / (duration * fps), transition_color, new_camera_x, new_camera_y, action)
        self.w = 0
        self.x = pyxel.width

    def update(self, pyxel_manager):
        self.w += self.speed * self.direction
        self.x -= self.speed * self.direction

        if self.w > pyxel.width // 2 and self.direction == 1:
            self.direction = -1
            pyxel_manager.change_scene(self.new_scene_id, self.new_camera_x, self.new_camera_y, self.action)
            self.x = pyxel.width // 2
        if self.w < 0 and self.direction == -1:
            pyxel_manager.finish_transition()
            return

    def draw(self, pyxel_manager):
        pyxel.rect(pyxel_manager.camera_x, pyxel_manager.camera_y, self.w, pyxel.height, self.transition_color)
        pyxel.rect(pyxel_manager.camera_x + self.x, pyxel_manager.camera_y, self.w, pyxel.height, self.transition_color)

class TransitionRectangle(Transition):

    def __init__(self, new_scene_id:int, duration:float, transition_color:int, dir:int=LEFT, new_camera_x:int=0, new_camera_y:int=0, action=None, fps:int=60):
        speed = pyxel.width / (duration / 2 * fps) if dir in [LEFT, RIGHT] else pyxel.height / (duration / 2 * fps)
        super().__init__(new_scene_id, speed, transition_color, new_camera_x, new_camera_y, action)
        self.dir = dir
        self.w = 0
        self.x = pyxel.width if dir == RIGHT else 0
        self.y = pyxel.height if dir == BOTTOM else 0

    def update(self, pyxel_manager):
        if self.dir in [RIGHT, LEFT]:
            self.w += self.speed * self.direction

            if (self.direction == 1 and self.dir == RIGHT) or (self.direction == -1 and self.dir == LEFT):
                self.x = self.x - self.speed if self.dir == RIGHT else self.x + self.speed
            if self.w > pyxel.width and self.direction == 1:
                self.direction = -1
                pyxel_manager.change_scene(self.new_scene_id, self.new_camera_x, self.new_camera_y, self.action)
                self.x = 0
            if self.w < 0 and self.direction == -1:
                pyxel_manager.finish_transition()
                return
        elif self.dir in [TOP, BOTTOM]:
            self.w += self.speed * self.direction

            if (self.direction == 1 and self.dir == BOTTOM) or (self.direction == -1 and self.dir == TOP):
                self.y = self.y - self.speed if self.dir == BOTTOM else self.y + self.speed
            if self.w > pyxel.height and self.direction == 1:
                self.direction = -1
                pyxel_manager.change_scene(self.new_scene_id, self.new_camera_x, self.new_camera_y, self.action)
                self.y = 0
            if self.w < 0 and self.direction == -1:
                pyxel_manager.finish_transition()
                return

    def draw(self, pyxel_manager):
        if self.dir in [RIGHT, LEFT]:
            pyxel.rect(pyxel_manager.camera_x + self.x, pyxel_manager.camera_y, self.w, pyxel.height, self.transition_color)
        elif self.dir in [TOP, BOTTOM]:
            pyxel.rect(pyxel_manager.camera_x, pyxel_manager.camera_y + self.y, pyxel.width, self.w, self.transition_color)

class TransitionOuterCircle(Transition):

    def __init__(self, new_scene_id:int, duration:float, transition_color:int, new_camera_x:int=0, new_camera_y:int=0, action=None, fps:int=60):
        self.start_end = int(math.hypot(pyxel.width, pyxel.height) / 2) + 1
        self.end = self.start_end
        super().__init__(new_scene_id, math.ceil(self.start_end / (duration / 2 * fps)), transition_color, new_camera_x, new_camera_y, action)

    def update(self, pyxel_manager):
        self.end -= self.speed * self.direction

        if self.end < 0 and self.direction == 1:
            self.direction = -1
            pyxel_manager.change_scene(self.new_scene_id, self.new_camera_x, self.new_camera_y, self.action)
        if self.end > self.start_end and self.direction == -1:
            pyxel_manager.finish_transition()
            return

    def draw(self, pyxel_manager):        
        for radius in range(self.start_end, self.end, -1):
            pyxel.ellib(pyxel_manager.camera_x + pyxel.width / 2 - radius, pyxel_manager.camera_y + pyxel.height / 2 - radius, radius * 2, radius * 2, self.transition_color)
            pyxel.ellib(pyxel_manager.camera_x + pyxel.width / 2 - radius + 1, pyxel_manager.camera_y + pyxel.height / 2 - radius, radius * 2, radius * 2, self.transition_color)

class TransitionTriangle(Transition):

    def __init__(self, new_scene_id:int, duration:float, transition_color:int, new_camera_x:int=0, new_camera_y:int=0, action=None, fps:int=60):
        super().__init__(new_scene_id, (max(pyxel.width, pyxel.height) * 2.5) / (duration / 2 * fps), transition_color, new_camera_x, new_camera_y, action)
        self.size = 0
        self.angle = 270

    def update(self, pyxel_manager):
        self.size += self.speed * self.direction
        self.angle += 5 * self.direction

        if self.size / 2.5 > max(pyxel.width, pyxel.height) and self.direction == 1:
            self.direction = -1
            pyxel_manager.change_scene(self.new_scene_id, self.new_camera_x, self.new_camera_y, self.action)
        if self.size < 0 and self.direction == -1:
            pyxel_manager.finish_transition()
            return

    def draw(self, pyxel_manager):
        d = math.sqrt(3) / 3 * self.size
        x1, y1 = pyxel_manager.camera_x + pyxel.width / 2 + d * math.cos(math.radians(0 + self.angle)), pyxel_manager.camera_y + pyxel.height / 2 + d * math.sin(math.radians(0 + self.angle))
        x2, y2 = pyxel_manager.camera_x + pyxel.width / 2 + d * math.cos(math.radians(120 + self.angle)), pyxel_manager.camera_y + pyxel.height / 2 + d * math.sin(math.radians(120 + self.angle))
        x3, y3 = pyxel_manager.camera_x + pyxel.width / 2 + d * math.cos(math.radians(240 + self.angle)), pyxel_manager.camera_y + pyxel.height / 2 + d * math.sin(math.radians(240 + self.angle))
        pyxel.tri(x1, y1, x2, y2, x3, y3, self.transition_color)

class TransitonPixelate(Transition):

    def __init__(self, new_scene_id:int, duration:float, cell_size:int, transition_color:int, new_camera_x:int=0, new_camera_y:int=0, action=None, fps:int=60):
        super().__init__(new_scene_id, round((pyxel.width // cell_size) * (pyxel.height // cell_size) / (duration / 2 * fps)), transition_color, new_camera_x, new_camera_y, action)
        self.hidden_pixels = [(x, y) for x in range(0, pyxel.width, cell_size) for y in range(0, pyxel.height, cell_size)]
        self.visible_pixels = []
        self.cell_size = cell_size

    def update(self, pyxel_manager):
        if len(self.hidden_pixels) > 0 and self.direction == 1:
            for _ in range(self.speed):
                if len(self.hidden_pixels) <= 0:
                    break
                self.visible_pixels.append(self.hidden_pixels.pop(random.randint(0, len(self.hidden_pixels) - 1)))
        elif self.direction == 1:
            self.direction = -1
            pyxel_manager.change_scene(self.new_scene_id, self.new_camera_x, self.new_camera_y, self.action)
        elif len(self.visible_pixels) > 0 and self.direction == -1:
            for _ in range(self.speed):
                if len(self.visible_pixels) <= 0:
                    break
                self.hidden_pixels.append(self.visible_pixels.pop(random.randint(0, len(self.visible_pixels) - 1)))
        elif self.direction == -1:
            pyxel_manager.finish_transition()
            return

    def draw(self, pyxel_manager):
        for px, py in self.visible_pixels:
            pyxel.rect(pyxel_manager.camera_x + px, pyxel_manager.camera_y + py, self.cell_size, self.cell_size, self.transition_color)

class TransitionDiagonal(Transition):
    def __init__(self, new_scene_id:int, duration:float, transition_color:int, dir:int=TOP_LEFT, new_camera_x:int=0, new_camera_y:int=0, action=None, fps:int=60):
        self.max_pos = pyxel.width + pyxel.height
        super().__init__(new_scene_id,  self.max_pos / (duration / 2 * fps), transition_color, new_camera_x, new_camera_y, action)
        self.start = self.end = 0
        self.dir = dir

    def update(self, pyxel_manager):
        if self.direction == 1:   self.end += self.speed
        else:                     self.start += self.speed

        if self.end > self.max_pos and self.direction == 1:
            self.direction = -1
            pyxel_manager.change_scene(self.new_scene_id, self.new_camera_x, self.new_camera_y, self.action)
        if self.start > self.max_pos and self.direction == -1:
            pyxel_manager.finish_transition()
            return

    def draw(self, pyxel_manager):
        for i in range(round(self.start), round(self.end) + 1):
            if self.dir == TOP_LEFT:
                pyxel.line(pyxel_manager.camera_x, pyxel_manager.camera_y + i, pyxel_manager.camera_x + i, pyxel_manager.camera_y, self.transition_color)
            elif self.dir == TOP_RIGHT:
                pyxel.line(pyxel_manager.camera_x + pyxel.width, pyxel_manager.camera_y + i, pyxel_manager.camera_x + pyxel.width - i, pyxel_manager.camera_y, self.transition_color)
            elif self.dir == BOTTOM_LEFT:
                pyxel.line(pyxel_manager.camera_x, pyxel_manager.camera_y + pyxel.height - i, pyxel_manager.camera_x + i, pyxel_manager.camera_y + pyxel.height, self.transition_color)
            else:
                pyxel.line(pyxel_manager.camera_x + pyxel.width, pyxel_manager.camera_y + pyxel.height - i, pyxel_manager.camera_x + pyxel.width - i, pyxel_manager.camera_y + pyxel.height, self.transition_color)

class PyxelManager:

    def __init__(self, width:int, height:int, scenes:list, default_scene_id:int=0, fps:int=60, fullscreen:bool=False, mouse:bool=False, quit_key:int=pyxel.KEY_ESCAPE, camera_x:int=0, camera_y:int=0, debug_background_color:int=0, debug_text_color:int=7):
        
        self.__scenes_dict = {scene.id:scene for scene in scenes}
        self.__current_scene = self.__scenes_dict[default_scene_id]
        self.__transition = None

        self.__cam_x = self.__cam_tx = camera_x
        self.__cam_y = self.__cam_ty = camera_y
        self.__cam_bounds = (-float("inf"), -float("inf"), float("inf"), float("inf"))
        self.__shake_amount = 0
        self.__shake_decay = 0

        self.__flash = {}

        self.__fps = fps
        self.__previous_frame_time = time.time()
        self.__current_fps = 0

        self.debug = False
        self.debug_background_color = debug_background_color
        self.debug_text_color = debug_text_color

        pyxel.init(width, height, fps=fps, quit_key=quit_key)
        pyxel.fullscreen(fullscreen)
        pyxel.mouse(mouse)

        if self.__current_scene.pyxres_path:
            pyxel.load(self.__current_scene.pyxres_path)
        pyxel.title(self.__current_scene.title)
        pyxel.screen_mode(self.__current_scene.screen_mode)
        pyxel.colors.from_list(self.__current_scene.palette)

    @property
    def camera_x(self)-> int|float:
        return self.__cam_x
    
    @property
    def camera_y(self)-> int|float:
        return self.__cam_y

    @property
    def mouse_x(self)-> int:
        return self.__cam_x + pyxel.mouse_x
    
    @property
    def mouse_y(self)-> int:
        return self.__cam_y + pyxel.mouse_y
    
    def set_camera(self, new_camera_x:int, new_camera_y:int):
        self.__cam_x = self.__cam_tx = max(self.__cam_bounds[0], min(new_camera_x, self.__cam_bounds[2] - pyxel.width))
        self.__cam_y = self.__cam_ty = max(self.__cam_bounds[1], min(new_camera_y, self.__cam_bounds[3] - pyxel.height))

    def move_camera(self, new_camera_x:int, new_camera_y:int):
        self.__cam_tx = max(self.__cam_bounds[0], min(new_camera_x, self.__cam_bounds[2] - pyxel.width))
        self.__cam_ty = max(self.__cam_bounds[1], min(new_camera_y, self.__cam_bounds[3] - pyxel.height))

    def set_camera_bounds(self, min_x:int, min_y:int, max_x:int, max_y:int):
        self.__cam_bounds = (min_x, min_y, max_x, max_y)
        self.__cam_tx = max(self.__cam_bounds[0], min(self.__cam_tx, self.__cam_bounds[2] - pyxel.width))
        self.__cam_ty = max(self.__cam_bounds[1], min(self.__cam_ty, self.__cam_bounds[3] - pyxel.height))
        self.__cam_x = max(self.__cam_bounds[0], min(self.__cam_x, self.__cam_bounds[2] - pyxel.width))
        self.__cam_y = max(self.__cam_bounds[1], min(self.__cam_y, self.__cam_bounds[3] - pyxel.height))

    def shake_camera(self, amount:int, decay:float):
        self.__shake_amount = amount
        self.__shake_decay = decay

    def flash(self, lifespan:int, color:int, intensity:float):
        self.__flash = {"life":lifespan, "color":color, "intensity":intensity}

    def change_scene(self, new_scene_id:int, new_camera_x:int=0, new_camera_y:int=0, action=None):
        self.set_camera(new_camera_x, new_camera_y)

        self.__current_scene = self.__scenes_dict[new_scene_id]
        if action:
            action()

        if self.__current_scene.pyxres_path:
            pyxel.load(self.__current_scene.pyxres_path)
        pyxel.colors.from_list(self.__current_scene.palette)
        pyxel.title(self.__current_scene.title)
        pyxel.screen_mode(self.__current_scene.screen_mode)

    def change_scene_transition(self, transition:Transition):
        self.__transition = transition

    def finish_transition(self):
        self.__transition = None

    def apply_palette_effect(self, effect_function, **kwargs):
        pyxel.colors.from_list(effect_function(self.__current_scene.palette, kwargs))

    def reset_palette(self):
        pyxel.colors.from_list(self.__current_scene.palette)

    def update(self):
        if self.__transition:
            self.__transition.update(self)

        self.__cam_x += (self.__cam_tx - self.__cam_x) * 0.1
        self.__cam_y += (self.__cam_ty - self.__cam_y) * 0.1

        if self.__shake_amount > 0:
            a = self.__shake_amount
            pyxel.camera(self.__cam_x + random.uniform(-a, a), self.__cam_y + random.uniform(-a, a))
            self.__shake_amount = max(0, self.__shake_amount - self.__shake_decay)
        else:
            pyxel.camera(self.__cam_x, self.__cam_y)

        if not self.__transition:
            self.__current_scene.update()

    def draw(self):
        self.__current_scene.draw()
        if self.__transition:
            self.__transition.draw(self)

        if self.__flash:
            pyxel.dither(self.__flash["intensity"])
            pyxel.rect(self.__cam_x, self.__cam_y, pyxel.width, pyxel.height, self.__flash["color"])
            pyxel.dither(1)
            self.__flash["life"] -= 1
            if self.__flash["life"] == 0:
                self.__flash = {}

        if self.debug:
            pyxel.rect(self.__cam_x + 1, self.__cam_y + 1, 66, 27, self.debug_background_color)
            pyxel.text(self.__cam_x + 3, self.__cam_y + 3, f"Scene[{self.__current_scene.id}]", self.debug_text_color)
            pyxel.text(self.__cam_x + 3, self.__cam_y + 9, f"Screen[{pyxel.mouse_x},{pyxel.mouse_y}]", self.debug_text_color)
            pyxel.text(self.__cam_x + 3, self.__cam_y + 15, f"World[{self.mouse_x:.0f},{self.mouse_y:.0f}]", self.debug_text_color)
            pyxel.text(self.__cam_x + 3, self.__cam_y + 21, f"Fps[{self.__current_fps:.0f}]", self.debug_text_color)

        if pyxel.frame_count % self.__fps == 0:
            self.__current_fps = 1 / (time.time() - self.__previous_frame_time)
        self.__previous_frame_time = time.time()

    def run(self):
        pyxel.run(self.update, self.draw)

class Scene:

    def __init__(self, id:int, title:str, update, draw, pyxres_path:str=None, palette:list=DEFAULT_PYXEL_COLORS, screen_mode:int=0):
        self.id = id
        self.title = title
        self.update = update
        self.draw = draw
        self.pyxres_path = pyxres_path
        self.palette = palette
        self.screen_mode = screen_mode

class CutsceneAction:

    def __init__(self, duration:float, update_action=None, draw_action=None):
        self.duration = duration
        self.update_action = update_action
        self.draw_action = draw_action
        self.elapsed = 0
        self.finished = False

    def update(self, dt:float):
        if self.finished:
            return
        
        if self.update_action:
            self.update_action(self, dt)

        self.elapsed += dt
        if self.elapsed >= self.duration:
            self.finished = True

    def draw(self):
        if self.draw_action and not self.finished:
            self.draw_action(self)

class Cutscene:

    def __init__(self):
        self.actions = []
        self.action_index = 0
        self.active = False
        self.finished = False

    def add_action(self, action:CutsceneAction):
        self.actions.append(action)

    def start(self):
        self.active = True
        self.finished = False
        self.action_index = 0
        for action in self.actions:
            action.elapsed = 0
            action.finished = False

    def update(self, dt:float):
        if not self.active or self.finished:
            return
        
        if self.action_index < len(self.actions):
            action = self.actions[self.action_index]
            action.update(dt)
            if action.finished:
                self.action_index += 1
        else:
            self.finished = True
            self.active = False

    def draw(self):
        if not self.active or self.finished:
            return
        
        if self.action_index < len(self.actions):
            action = self.actions[self.action_index]
            action.draw()

def parallel_action(actions:list, duration:float):
    def update(action, dt):
        for act in actions:
            act.update(dt)

    def draw(action):
        for act in actions:
            act.draw()

    return CutsceneAction(duration, update, draw)

def wait_action(duration:float):
    return CutsceneAction(duration)

def tween_camera_action(manager:PyxelManager, start_x:int, start_y:int, end_x:int, end_y:int, duration:float, easing=None):
    tween_x = Tween(start_x, end_x, duration, autostart=True, easing_function=easing)
    tween_y = Tween(start_y, end_y, duration, autostart=True, easing_function=easing)

    def update(action, dt):
        manager.set_camera(int(tween_x.update(dt)), int(tween_y.update(dt)))

    return CutsceneAction(duration, update)

def shake_camera_action(manager:PyxelManager, amount:int, decay:float, duration:float):
    def update(action, dt):
        if not action.finished:
            manager.shake_camera(amount, decay)

    return CutsceneAction(duration, update)

def palette_effect_action(manager:PyxelManager, effect_function, duration:float, **kwargs):
    def update(action, dt):
        manager.apply_palette_effect(effect_function, **kwargs)
        if action.finished:
            manager.reset_palette()

    return CutsceneAction(duration, update)

def tween_move_object_action(obj, start_x:float, start_y:float, end_x:float, end_y:float, duration:float, easing=None):
    tween_x = Tween(start_x, end_x, duration, autostart=True, easing_function=easing)
    tween_y = Tween(start_y, end_y, duration, autostart=True, easing_function=easing)

    def update(action, dt):
        obj.x = tween_x.update(dt)
        obj.y = tween_y.update(dt)

    return CutsceneAction(duration, update)

def particles_action(manager:ParticleManager, particle_factory, count:int, duration:float=0.01):
    def update(action, dt):
        for _ in range(count):
            manager.add_particle(particle_factory())

    return CutsceneAction(duration, update)

def shockwave_action(manager:ShockwaveManager, shockwave:CircleShockwave, duration:float=0.01):
    def update(action, dt):
        manager.add_shockwave(shockwave)

    return CutsceneAction(duration, update)

def typewriter_text_action(text:Text, duration:float):
    visible_chars = [0]
    total_chars = len(text.text)

    def update(action, dt):
        text.update()
        progress = min(action.elapsed / duration, 1.0)
        visible_chars[0] = int(total_chars * progress)

    def draw(action):
        partial_text = text.text[:visible_chars[0]]
        Text(
            partial_text, text.x, text.y,
            text.text_colors, text.font_size, text.font,
            anchor=text._Text__anchor,
            relative=text.relative,
            color_mode=text.color_mode,
            wavy=text.wavy,
            shadow=text.shadow, shadow_color=text.shadow_color,
            outline=text.outline, outline_color=text.outline_color,
            glitch_intensity=text.glitch_intensity
        ).draw()

    return CutsceneAction(duration, update, draw)

if __name__ == "__main__":
    from tweening import ease_out_quint

    def update_1():
        if pyxel.btnp(pyxel.KEY_F):
            pm.flash(3, 7, 1)

        if pyxel.btnp(pyxel.KEY_B):
            pm.debug = not pm.debug
        if pyxel.btnp(pyxel.KEY_SPACE):
            pm.change_scene_transition(TransitionDiagonal(1, 2, 1, BOTTOM_RIGHT))
        if pyxel.btnp(pyxel.KEY_C):
            pm.change_scene_transition(TransitionTriangle(2, 4, 1, action=lambda: cutscene.start()))

    def draw_1():
        pyxel.cls(10)

    def update_2():
        if pyxel.btnp(pyxel.KEY_B):
            pm.debug = not pm.debug
        if pyxel.btnp(pyxel.KEY_SPACE):
            pm.change_scene_transition(TransitionTriangle(0, 1, 1))

    def draw_2():
        pyxel.cls(3)

    def update_3():
        cutscene.update(1/60)

        if cutscene.finished:
            pm.change_scene_transition(TransitionClosingDoors(0, 4, 1))

    def draw_3():
        pyxel.cls(12)

        pyxel.rect(10, 10, 50, 50, 8)

        cutscene.draw()

    s1 = Scene(0, "Game.py Example - Scene 1", update_1, draw_1)
    s2 = Scene(1, "Game.py Example - Scene 2", update_2, draw_2)
    s3 = Scene(2, "Game.py Example - Scene 3", update_3, draw_3)
    pm = PyxelManager(228, 128, [s1, s2, s3], mouse=True)

    cutscene = Cutscene()

    cutscene.add_action(wait_action(1))
    cutscene.add_action(tween_camera_action(pm, 0, 0, -50, -50, 2, ease_out_quint))
    cutscene.add_action(shake_camera_action(pm, 5, 0.5, 1))
    cutscene.add_action(wait_action(0.5))

    pm.run()