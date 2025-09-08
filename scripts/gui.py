"""
@author : Léo Imbert
@created : 15/10/2024
@updated : 07/09/2025

TODO :
- Checkbox
- Vertical Slider
- Scrollable Panel
"""

from draw import rounded_rect, rounded_rectb
from other import get_anchored_position
from vars import *
import random
import pyxel
import math

class Text:

    def __init__(self, text:str, x:int, y:int, text_colors:int|list, font_size:int=0, font:dict=FONT_DEFAULT, anchor:int=ANCHOR_TOP_LEFT, relative:bool=False, color_mode:int=NORMAL_COLOR_MODE, color_change_time:int=5, wavy:bool=False, wave_speed:int=10, amplitude:int=3, shadow:bool=False, shadow_color:int=0, shadow_offset:int=1, outline:bool=False, outline_color:int=0, glitch_intensity:int=0):
        self.text = text
        self.x, self.y = x, y
        self.font_size = font_size
        self.font = font
        self.__anchor = anchor
        self.relative = relative
        self.wavy = wavy
        self.wave_speed = wave_speed
        self.amplitude = amplitude
        self.shadow = shadow
        self.shadow_color = shadow_color
        self.shadow_offset = shadow_offset
        self.outline = outline
        self.outline_color = outline_color
        self.glitch_intensity = glitch_intensity

        self.text_colors = [text_colors] if isinstance(text_colors, int) else text_colors
        self.original_text_colors = [x for x in self.text_colors]
        self.color_mode = color_mode
        self.color_change_time = color_change_time
        self.__last_change_color_time = pyxel.frame_count

        _, text_height = text_size(text, font_size)
        _, self.y = get_anchored_position(0, y, 0, text_height, anchor)

    def __draw_line(self, text:str, y:int, camera_x:int=0, camera_y:int=0):
        text_width, _ = text_size(text, self.font_size)
        x, _ = get_anchored_position(self.x, 0, text_width, 0, self.__anchor)

        if self.relative:
            x += camera_x
            y += camera_y

        if self.shadow:
            Text(text, x + self.shadow_offset, y + self.shadow_offset, self.shadow_color, self.font_size, wavy=self.wavy, wave_speed=self.wave_speed, amplitude=self.amplitude).draw()

        if self.outline:
            Text(text, x - 1, y, self.outline_color, self.font_size, wavy=self.wavy, wave_speed=self.wave_speed, amplitude=self.amplitude).draw()
            Text(text, x + 1, y, self.outline_color, self.font_size, wavy=self.wavy, wave_speed=self.wave_speed, amplitude=self.amplitude).draw()
            Text(text, x, y - 1, self.outline_color, self.font_size, wavy=self.wavy, wave_speed=self.wave_speed, amplitude=self.amplitude).draw()
            Text(text, x, y + 1, self.outline_color, self.font_size, wavy=self.wavy, wave_speed=self.wave_speed, amplitude=self.amplitude).draw()

        if self.font_size > 0:
            for char_index, char in enumerate(text):
                    x += random.uniform(-self.glitch_intensity, self.glitch_intensity)
                    char_y = y + math.cos(pyxel.frame_count / self.wave_speed + char_index * 0.3) * self.amplitude if self.wavy else y
                    char_y += random.uniform(-self.glitch_intensity, self.glitch_intensity)

                    if char in self.font:
                        char_matrix = self.font[char]
                        char_width = len(char_matrix[0]) * self.font_size
                        
                        for row_index, row in enumerate(char_matrix):
                            for col_index, pixel in enumerate(row):
                                if pixel:
                                    pyxel.rect(x + col_index * self.font_size, char_y + row_index * self.font_size + (1 * self.font_size if char in "gjpqy" else 0), self.font_size, self.font_size, self.text_colors[char_index % len(self.text_colors)])
                        
                        x += char_width + 1
        else:
            for char_index, char in enumerate(text):
                x += random.uniform(-self.glitch_intensity, self.glitch_intensity)
                char_y = y + math.cos(pyxel.frame_count / self.wave_speed + char_index * 0.3) * self.amplitude if self.wavy else y
                char_y += random.uniform(-self.glitch_intensity, self.glitch_intensity)
                pyxel.text(x, char_y, char, self.text_colors[char_index % len(self.text_colors)])
                x += 4

    def update(self):
        if self.color_mode != NORMAL_COLOR_MODE and pyxel.frame_count - self.__last_change_color_time >= self.color_change_time:
            if self.color_mode == ROTATING_COLOR_MODE:
                self.__last_change_color_time = pyxel.frame_count
                self.text_colors = [self.text_colors[-1]] + self.text_colors[:-1]
            elif self.color_mode == RANDOM_COLOR_MODE:
                self.__last_change_color_time = pyxel.frame_count
                self.text_colors = [random.choice(self.original_text_colors) for _ in range(len(self.text))]

    def draw(self, camera_x:int=0, camera_y:int=0):
        if "\n" in self.text:
            lines = self.text.split("\n")
            for i, line in enumerate(lines):
                if self.font_size > 0:
                    self.__draw_line(line, self.y + i * (11 * self.font_size), camera_x, camera_y)
                else:
                    self.__draw_line(line, self.y + i * 9, camera_x, camera_y)
        else:
            self.__draw_line(self.text, self.y, camera_x, camera_y)

class Button:

    def __init__(self, text:str, x:int, y:int, corner_radius:int, background_color:int, text_colors:list|int, hover_background_color:int, hover_text_colors:list|int, font_size:int=1, font:dict=FONT_DEFAULT, border:bool=False, border_color:int=0, color_mode:int=NORMAL_COLOR_MODE, color_change_time:int=10, relative:bool=True, anchor:int=ANCHOR_TOP_LEFT, command=None):
        self.x = x
        self.y = y
        self.corner_radius = corner_radius
        self.__width, self.__height = text_size(text, font_size)
        self.__height -= 2 * font_size if font_size > 0 else 2
        self.__width += 4 + corner_radius if border else 2 + corner_radius
        self.__height += 4 if border else 2
        self.background_color = background_color
        self.hover_background_color = hover_background_color
        self.border = border
        self.border_color = border_color
        self.relative = relative
        self.command = command

        self.x, self.y = get_anchored_position(self.x, self.y, self.__width, self.__height, anchor)

        self.text = Text(text, self.x + 2 + corner_radius / 2 if border else self.x + 1, self.y + 2 if border else self.y + 1, text_colors, font_size, font, color_mode=color_mode, color_change_time=color_change_time, relative=relative)
        self.hover_text = Text(text, self.x + 2 + corner_radius / 2 if border else self.x + 1 + corner_radius / 2, self.y + 2 if border else self.y + 1, hover_text_colors, font_size, font, color_mode=color_mode, color_change_time=color_change_time, relative=relative)

    def is_hovered(self, camera_x:int=0, camera_y:int=0)-> bool:
        if self.x <= pyxel.mouse_x < self.x + self.__width and self.y <= pyxel.mouse_y < self.y + self.__height and self.relative:
            return True
        if self.x <= camera_x + pyxel.mouse_x < self.x + self.__width and self.y <= camera_y + pyxel.mouse_y < self.y + self.__height and not self.relative:
            return True
        
    def update(self, camera_x:int=0, camera_y:int=0):
        self.text.update()
        self.hover_text.update()
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and self.is_hovered(camera_x, camera_y) and self.command:
            self.command()

    def draw(self, camera_x:int=0, camera_y:int=0):
        x = camera_x + self.x if self.relative else self.x
        y = camera_y + self.y if self.relative else self.y
        if self.is_hovered(camera_x, camera_y):
            rounded_rect(x, y, self.__width, self.__height, self.corner_radius, self.hover_background_color)
            self.hover_text.draw(camera_x, camera_y)
        else:
            rounded_rect(x, y, self.__width, self.__height, self.corner_radius, self.background_color)
            self.text.draw(camera_x, camera_y)
        if self.border:
            rounded_rectb(x, y, self.__width, self.__height, self.corner_radius, self.border_color)

class Entry:

    def __init__(self, x:int, y:int, width:int, corner_radius:int, text_color:int, unfocused_color:int, focused_color:int, font_size:int=1, font:dict=FONT_DEFAULT, text_cursor_color:int=0, relative:bool=True, anchor:int=ANCHOR_TOP_LEFT):
        self.x = x
        self.y = y
        self.width = width
        self.__height = text_size("A", font_size)[1]
        self.__height -= 2 * font_size if font_size > 0 else 2
        self.corner_radius = corner_radius
        self.font_size = font_size
        self.unfocused_color = unfocused_color
        self.focused_color = focused_color
        self.focused = False
        self.text_cursor_color = text_cursor_color
        self.relative = relative

        self.x, self.y = get_anchored_position(self.x, self.y, self.width, self.__height, anchor)

        self.text = Text("", self.x + 1 + self.corner_radius / 2, self.y + 1, text_color, font_size, font, relative=relative)

    def is_hovered(self, camera_x:int=0, camera_y:int=0)-> bool:
        if self.x <= pyxel.mouse_x < self.x + self.width and self.y <= pyxel.mouse_y < self.y + self.__height + 2 and self.relative:
            return True
        elif self.x <= camera_x + pyxel.mouse_x < self.x + self.width and self.y <= camera_y + pyxel.mouse_y < self.y + self.__height + 2 and not self.relative:
            return True
        
    def update(self, camera_x:int=0, camera_y:int=0):
        self.text.update()
        if self.is_hovered(camera_x, camera_y) and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.focused = True
        elif pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.focused = False

        if self.focused:
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.focused = False
            elif pyxel.btnp(pyxel.KEY_BACKSPACE):
                self.text.text = self.text.text[:-1]
            for k, v in keys_to_chars.items():
                if pyxel.btnp(pyxel.KEY_LSHIFT, hold=1, repeat=1) and pyxel.btnp(k):
                    self.text.text += v.upper()
                elif pyxel.btnp(k):
                    self.text.text += v
            if text_size(self.text.text, self.font_size)[0] > self.width - 1 - self.corner_radius:
                self.text.text = self.text.text[:-1]
                self.focused = False

    def draw(self, camera_x:int=0, camera_y:int=0):
        x = camera_x + self.x if self.relative else self.x
        y = camera_y + self.y if self.relative else self.y
        rounded_rect(x, y, self.width, self.__height + 2, self.corner_radius, self.focused_color if self.focused else self.unfocused_color)
        self.text.draw(camera_x, camera_y)
        if self.focused and pyxel.frame_count % (30 * 2) < 30:
            pyxel.rect(x + self.font_size + 1 + self.corner_radius / 2 + text_size(self.text.text, self.font_size)[0], y + 1, self.font_size, self.__height, self.text_cursor_color)

class UIBar:

    def __init__(self, x:int, y:int, width:int, height:int, corner_radius:int, border_color:int, bar_color:int, starting_value:int, max_value:int, relative:bool=True, horizontal:bool=True, regen:bool=False, speed_regen:int=0.5, value_regen:int=1, anchor:int=ANCHOR_TOP_LEFT):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.corner_radius = corner_radius
        self.border_color = border_color
        self.bar_color = bar_color

        self.value = starting_value
        self.max_value = max_value
        self.relative = relative
        self.horizontal = horizontal

        self.regen = regen
        self.speed_regen = speed_regen
        self.__regen_timer = 0
        self.value_regen = value_regen
        self.__bar_width = 0
        self.__bar_height = 0

        self.x, self.y = get_anchored_position(self.x, self.y, self.width + 2, self.height + 2, anchor)

    def update(self):
        self.__regen_timer += 1
        if self.value < 0:
            self.value = 0
        if self.value < self.max_value and self.regen and self.__regen_timer >= self.speed_regen:
            self.__regen_timer = 0
            self.value += self.value_regen
        while self.value > self.max_value:
            self.value -= 1
        self.__bar_width = self.width * self.value / self.max_value
        self.__bar_height = self.height * self.value / self.max_value

    def draw(self, camera_x:int=0, camera_y:int=0):
        if self.relative:
            if self.horizontal:
                rounded_rect(camera_x + self.x, camera_y + self.y, self.__bar_width, self.height, self.corner_radius, self.bar_color) if self.__bar_width > 0 else None
                rounded_rectb(camera_x + self.x, camera_y + self.y, self.width, self.height, self.corner_radius, self.border_color)
            else:
                rounded_rect(camera_x + self.x, camera_y + self.y + self.height - self.__bar_height, self.width, self.__bar_height, self.corner_radius, self.bar_color) if self.__bar_width > 0 else None
                rounded_rectb(camera_x + self.x, camera_y + self.y, self.width, self.height, self.corner_radius, self.border_color)
        else:
            if self.horizontal:
                rounded_rect(self.x, self.y, self.__bar_width, self.height, self.corner_radius, self.bar_color) if self.__bar_width > 0 else None
                rounded_rectb(self.x, self.y, self.width, self.height, self.corner_radius, self.border_color)
            else:
                rounded_rect(self.x, self.y + self.height - self.__bar_height, self.width, self.__bar_height, self.corner_radius, self.bar_color) if self.__bar_width > 0 else None
                rounded_rectb(self.x, self.y, self.width, self.height, self.corner_radius, self.border_color)

def text_size(text:str, font_size:int=1, font:dict=FONT_DEFAULT)-> tuple:
    lines = text.split("\n")
    if font_size == 0:
        return (max(len(line) * 4 for line in lines), 9 * len(lines))
    text_width = max(sum(len(font[char][0]) * font_size + 1 for char in line) - 1 for line in lines)
    text_height = (11 * font_size + 1) * len(lines)

    return (text_width, text_height)

def corrupted_text(text:str, corruption_letters:list|str, corruption_chance:float=0.1)-> str:
    return "".join([random.choice(corruption_letters) if random.random() < corruption_chance else char for char in text])

if __name__ == "__main__":
    pyxel.init(228, 128, title="Gui.py Example", fps=60)
    pyxel.mouse(True)

    u = UIBar(2, 2, 40, 8, 4, 0, 8, 50, 100)
    t1 = Text("Hello World!", 114, 10, [8, 9, 10, 11], font_size=2, anchor=ANCHOR_TOP, wavy=True, shadow=True, shadow_color=0, shadow_offset=1, color_mode=ROTATING_COLOR_MODE, color_change_time=30)
    t2 = Text("This is a longer text to test\nmultiple lines support.", 114, 70, 11, font_size=1, anchor=ANCHOR_CENTER, outline=True, outline_color=0)
    e = Entry(2, 100, 100, 5, 7, 5, 8, font_size=1, text_cursor_color=7)
    b = Button("Click Me!", 150, 100, 0, 12, 0, 14, 7, font_size=1, border=True, border_color=0, command=lambda: print("Button Clicked!"))

    def update():
        u.update()
        t1.update()
        t2.update()
        e.update()
        b.update()

        if pyxel.btnp(pyxel.KEY_UP):
            u.value += 10
        if pyxel.btnp(pyxel.KEY_DOWN):
            u.value -= 10

    def draw():
        pyxel.cls(12)

        u.draw()
        t1.draw()
        t2.draw()
        e.draw()
        b.draw()

    pyxel.run(update, draw)