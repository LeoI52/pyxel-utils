"""
@author : Léo Imbert
@created : 15/10/2024
@updated : 21/04/2026
"""

#? -------------------- IMPORTATIONS -------------------- ?#

import colorsys
import random
import math
import time

#? -------------------- CONVERSION -------------------- ?#

def hex_to_rgb(hex_val:int)-> tuple:
    r = (hex_val >> 16) & 0xFF
    g = (hex_val >> 8) & 0xFF
    b = hex_val & 0xFF
    return r, g, b

def rgb_to_hex(r:int, g:int, b:int)-> int:
    return int(f"0x{r:02X}{g:02X}{b:02X}", 16)

#? -------------------- PALETTES -------------------- ?#

def inverted_palette(original_palette:list)-> list:
    palette = []
    for color in original_palette:
        r, g, b = hex_to_rgb(color)
        r, g, b = 255 - r, 255 - g, 255 - b
        palette.append(rgb_to_hex(r, g, b))

    return palette

def grayscaled_palette(original_palette:list)-> list:
    palette = []
    for color in original_palette:
        r, g, b = hex_to_rgb(color)
        gray = int((r + g + b) / 3)
        palette.append(rgb_to_hex(gray, gray, gray))

    return palette

def black_white_palette(original_palette:list, kwargs:dict={})-> list:
    """
    kwargs : threshold (128)
    """
    palette = []
    threshold = kwargs.get("threshold", 128)
    for color in original_palette:
        r, g, b = hex_to_rgb(color)
        avg = (r + g + b) // 3
        palette.append(0xFFFFFF if avg > threshold else 0x000000)

    return palette

def random_color_jitter_palette(original_palette:list, kwargs:dict={})-> list:
    """
    kwargs : amount (30)
    """
    palette = []
    amount = kwargs.get("amount", 30)
    for color in original_palette:
        r, g, b = hex_to_rgb(color)
        palette.append(rgb_to_hex(min(max(r + random.randint(-amount, amount), 0), 255), 
           min(max(g + random.randint(-amount, amount), 0), 255), 
           min(max(b + random.randint(-amount, amount), 0), 255)))
        
    return palette

def night_vision_palette(original_palette:list)-> list:
    palette = []
    for color in original_palette:
        r, g, b = hex_to_rgb(color)
        avg = (r + g + b) // 3
        palette.append(rgb_to_hex(avg // 2, avg, avg // 2))
        
    return palette

def heat_map_palette(original_palette:list)-> list:
    palette = []
    for color in original_palette:
        r, g, b = hex_to_rgb(color)
        avg = (r + g + b) // 3
        if avg < 85:
            palette.append(rgb_to_hex(0, avg * 3, 255))
        elif avg < 170:
            palette.append(rgb_to_hex((avg - 85) * 3, 255, (170 - avg) * 3))
        else:
            palette.append(rgb_to_hex(255, (255 - avg) * 3, 0))
        
    return palette

def water_palette(original_palette:list)-> list:
    palette = []
    for color in original_palette:
        r, g, b = hex_to_rgb(color)
        palette.append(rgb_to_hex(r // 2, g // 2, min(255, b + 50)))
        
    return palette

def fire_palette(original_palette:list)-> list:
    palette = []
    for color in original_palette:
        r, g, b = hex_to_rgb(color)
        avg = (r + g + b) // 3
        palette.append(rgb_to_hex(min(255, avg * 2), max(0, avg - 100), 0))
        
    return palette

def psychedelic_shifting_palette(original_palette:list, kwargs:dict={})-> list:
    """
    kwargs : speed (1)
    """
    palette = []
    for color in original_palette:
        r, g, b = hex_to_rgb(color)
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        h = (h + time.time() * kwargs.get("speed", 1) % 1) % 1
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        palette.append(rgb_to_hex(int(r * 255), int(g * 255), int(b * 255)))
        
    return palette

def sepia_palette(original_palette:list)-> list:
    palette = []
    for color in original_palette:
        r, g, b = hex_to_rgb(color)
        new_r = min(255, int(0.393 * r + 0.769 * g + 0.189 * b))
        new_g = min(255, int(0.349 * r + 0.686 * g + 0.168 * b))
        new_b = min(255, int(0.272 * r + 0.534 * g + 0.131 * b))
        palette.append(rgb_to_hex(new_r, new_g, new_b))

    return palette

def neon_palette(original_palette:list)-> list:
    palette = []
    for color in original_palette:
        r, g, b = hex_to_rgb(color)
        brightness = (r + g + b) / 3
        if brightness > 30:
            max_val = max(r, g, b)
            if max_val == r:
                r = min(255, int(r * 1.5))
            elif max_val == g:
                g = min(255, int(g * 1.5))
            elif max_val == b:
                b = min(255, int(b * 1.5))
        palette.append(rgb_to_hex(r, g, b))

    return palette

def brightness_adjusted_palette(original_palette:list, kwargs:dict={})-> list:
    """
    kwargs : factor (1)
    """
    palette = []
    factor = kwargs.get("factor", 1)
    for color in original_palette:
        r, g, b = hex_to_rgb(color)
        new_r = min(255, max(0, int(r * factor)))
        new_g = min(255, max(0, int(g * factor)))
        new_b = min(255, max(0, int(b * factor)))
        palette.append(rgb_to_hex(new_r, new_g, new_b))
    return palette

def posterize_palette(original_palette:list, kwargs:dict={})-> list:
    """
    kwargs : levels (4)
    """
    palette = []
    levels = kwargs.get("levels", 4)
    factor = 255 // (levels - 1)
    for color in original_palette:
        r, g, b = hex_to_rgb(color)
        r = round(r / factor) * factor
        g = round(g / factor) * factor
        b = round(b / factor) * factor
        palette.append(rgb_to_hex(r, g, b))
    return palette

def duotone_palette(original_palette:list, kwargs:dict={})-> list:
    """
    kwargs : tone_1 ((0, 128, 255)), tone_2 ((255, 0, 128))
    """
    palette = []
    tone1 = kwargs.get("tone_1", (0, 128, 255))
    tone2 = kwargs.get("tone_2", (255, 0, 128))
    for color in original_palette:
        r, g, b = hex_to_rgb(color)
        gray = (r + g + b) / 765
        nr = int(tone1[0] + (tone2[0] - tone1[0]) * gray)
        ng = int(tone1[1] + (tone2[1] - tone1[1]) * gray)
        nb = int(tone1[2] + (tone2[2] - tone1[2]) * gray)
        palette.append(rgb_to_hex(nr, ng, nb))
    return palette

def glitch_palette(original_palette:list)-> list:
    palette = []
    for color in original_palette:
        r, g, b = hex_to_rgb(color)
        choice = random.choice([(r,g,b), (g,b,r), (b,r,g), (r,b,g)])
        palette.append(rgb_to_hex(*choice))
    return palette

def vaporwave_palette(original_palette:list)-> list:
    palette = []
    for color in original_palette:
        r, g, b = hex_to_rgb(color)
        r = min(255, int(r * 1.1 + 30))
        g = min(255, int(g * 0.8 + 20))
        b = min(255, int(b * 1.2 + 40))
        palette.append(rgb_to_hex(r, g, b))
    return palette

def iridescent_palette(original_palette:list, kwargs:dict={})-> list:
    """
    kwargs : speed (2)
    """
    speed = kwargs.get("speed", 2)
    palette = []
    for color in original_palette:
        r, g, b = hex_to_rgb(color)
        h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
        h = (h + math.sin(time.time() * speed) * 0.1) % 1
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        palette.append(rgb_to_hex(int(r*255), int(g*255), int(b*255)))
    return palette

#? -------------------- EXAMPLE -------------------- ?#

if __name__ == "__main__":
    from vars import DEFAULT_PYXEL_COLORS
    import pyxel

    pyxel.init(128, 128, title="Palette.py Example")
    pyxel.mouse(True)

    def change_palette(new_palette):
        pyxel.colors.clear()
        pyxel.colors.extend(new_palette)

    def update():
        if pyxel.btnp(pyxel.KEY_A):
            change_palette(DEFAULT_PYXEL_COLORS)
        if pyxel.btnp(pyxel.KEY_Z):
            change_palette(inverted_palette(DEFAULT_PYXEL_COLORS))
        if pyxel.btnp(pyxel.KEY_E):
            change_palette(grayscaled_palette(DEFAULT_PYXEL_COLORS))
        if pyxel.btnp(pyxel.KEY_R):
            change_palette(black_white_palette(DEFAULT_PYXEL_COLORS, {"threshold":128}))
        if pyxel.btnp(pyxel.KEY_T):
            change_palette(random_color_jitter_palette(DEFAULT_PYXEL_COLORS, {"amount":30}))
        if pyxel.btnp(pyxel.KEY_Y):
            change_palette(night_vision_palette(DEFAULT_PYXEL_COLORS))
        if pyxel.btnp(pyxel.KEY_U):
            change_palette(heat_map_palette(DEFAULT_PYXEL_COLORS))
        if pyxel.btnp(pyxel.KEY_I):
            change_palette(water_palette(DEFAULT_PYXEL_COLORS))
        if pyxel.btnp(pyxel.KEY_O):
            change_palette(fire_palette(DEFAULT_PYXEL_COLORS))
        if pyxel.btn(pyxel.KEY_P):
            change_palette(psychedelic_shifting_palette(DEFAULT_PYXEL_COLORS, {"speed":0.2}))
        if pyxel.btnp(pyxel.KEY_Q):
            change_palette(sepia_palette(DEFAULT_PYXEL_COLORS))
        if pyxel.btnp(pyxel.KEY_S):
            change_palette(neon_palette(DEFAULT_PYXEL_COLORS))
        if pyxel.btnp(pyxel.KEY_D):
            change_palette(brightness_adjusted_palette(DEFAULT_PYXEL_COLORS, {"factor":1.5}))
        if pyxel.btnp(pyxel.KEY_F):
            change_palette(posterize_palette(DEFAULT_PYXEL_COLORS, {"levels":3}))
        if pyxel.btnp(pyxel.KEY_G):
            change_palette(duotone_palette(DEFAULT_PYXEL_COLORS, {"tone_1":(0,128,255), "tone_2":(255,0,128)}))
        if pyxel.btnp(pyxel.KEY_H):
            change_palette(glitch_palette(DEFAULT_PYXEL_COLORS))
        if pyxel.btnp(pyxel.KEY_J):
            change_palette(vaporwave_palette(DEFAULT_PYXEL_COLORS))
        if pyxel.btn(pyxel.KEY_K):
            change_palette(iridescent_palette(DEFAULT_PYXEL_COLORS, {"speed":2}))

    def draw():
        pyxel.cls(0)
        c = 0
        for y in range(0, 128, 32):
            for x in range(0, 128, 32):
                pyxel.rect(x, y, 32, 32, c)
                c += 1

    pyxel.run(update, draw)