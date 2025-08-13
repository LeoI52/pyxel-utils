"""
@author : Léo Imbert
@created : 15/10/2024
@updated : 13/08/2025

TODO :
- Checkbox
- Vertical Slider
- Scrollable Panel
"""

from other import get_anchored_position, clamp
from draw import Sprite, rounded_rect
from animations import lerp
from vars import *
import random
import pyxel
import math

class Text:

    def __init__(self, text:str, x:int, y:int, text_colors:list|int, font_size:int=0, anchor:int=ANCHOR_TOP_LEFT, color_mode:int=NORMAL_COLOR_MODE, color_speed:int=5, relative:bool=False, wavy:bool=False, wave_speed:int=10, wave_height:int=3, shadow:bool=False, shadow_color:int=0, shadow_offset:int=1, glitch_intensity:int=0, underline:bool=False, underline_color:int=0, blinking:bool=False, blinking_frames:int=30):
        self.text = text
        self.x = x
        self.y = y
        self.__font_size = font_size
        self.__text_width, self.__text_height = text_size(text, font_size)
        self.__anchor = anchor
        self.__relative = relative
        self.__wavy = wavy
        self.__wave_speed = wave_speed
        self.__wave_height = wave_height
        self.__shadow = shadow
        self.__shadow_color = shadow_color
        self.__shadow_x = self.x + shadow_offset
        self.__shadow_y = self.y + shadow_offset
        self.__shadow_offset = shadow_offset
        self.__glitch_intensity = glitch_intensity
        self.__underline = underline
        self.__underline_color = underline_color
        self.__blinking = blinking
        self.__blinking_frames = blinking_frames

        self.__text_colors = [text_colors] if isinstance(text_colors, int) else text_colors
        self.__original_text_colors = [x for x in self.__text_colors]
        self.__color_mode = color_mode
        self.__color_speed = color_speed
        self.__last_change_color_time = pyxel.frame_count

        if "\n" not in self.text:
            self.x, self.y = get_anchored_position(self.x, self.y, self.__text_width, self.__text_height, anchor)

    def __draw_line(self, text:str, y:int, camera_x:int=0, camera_y:int=0):
        x = self.x
        text_width, text_height = text_size(text, self.__font_size)

        if self.__shadow:
            Text(text, x + self.__shadow_offset, y + self.__shadow_offset, self.__shadow_color, self.__font_size, self.__anchor, relative=self.__relative, underline=self.__underline, underline_color=self.__shadow_color, wavy=self.__wavy, wave_height=self.__wave_height, wave_speed=self.__wave_speed).draw(camera_x, camera_y)

        x, y = get_anchored_position(x, y, text_width, self.__text_height, self.__anchor)

        if self.__relative:
            x += camera_x
            y += camera_y

        char_x = x

        if self.__font_size > 0:
            for char_index, char in enumerate(text):
                char_y = y + math.cos(pyxel.frame_count / self.__wave_speed + char_index * 0.3) * self.__wave_height if self.__wavy else y

                if char in characters_matrices:
                    char_matrix = characters_matrices[char]
                    char_width = len(char_matrix[0]) * self.__font_size

                    x += random.uniform(-self.__glitch_intensity, self.__glitch_intensity)
                    char_y += random.uniform(-self.__glitch_intensity, self.__glitch_intensity)
                    
                    for row_index, row in enumerate(char_matrix):
                        for col_index, pixel in enumerate(row):
                            if pixel:
                                pyxel.rect(x + col_index * self.__font_size, char_y + row_index * self.__font_size + (1 * self.__font_size if char in "gjpqy" else 0), self.__font_size, self.__font_size, self.__text_colors[char_index % len(self.__text_colors)])
                    
                    x += char_width + self.__font_size

            if self.__underline:
                pyxel.rect(char_x, y + text_height - self.__font_size, text_width, self.__font_size, self.__underline_color)
        else:
            for char_index, char in enumerate(text):
                char_y = y + math.cos(pyxel.frame_count / self.__wave_speed + char_index * 0.3) * self.__wave_height if self.__wavy else y
                x += random.uniform(-self.__glitch_intensity, self.__glitch_intensity)
                char_y += random.uniform(-self.__glitch_intensity, self.__glitch_intensity)
                pyxel.text(x, char_y, char, self.__text_colors[char_index % len(self.__text_colors)])
                x += 4

    def update(self):
        if self.__color_mode and pyxel.frame_count - self.__last_change_color_time >= self.__color_speed:
            if self.__color_mode == ROTATING_COLOR_MODE:
                self.__last_change_color_time = pyxel.frame_count
                self.__text_colors = [self.__text_colors[-1]] + self.__text_colors[:-1]
            elif self.__color_mode == RANDOM_COLOR_MODE:
                self.__last_change_color_time = pyxel.frame_count
                self.__text_colors = [random.choice(self.__original_text_colors) for _ in range(len(self.text))]

    def draw(self, camera_x:int=0, camera_y:int=0):
        if self.__blinking and pyxel.frame_count % (self.__blinking_frames) >= self.__blinking_frames // 2:
            return

        # x = self.x
        y = self.y

        if "\n" in self.text:
            lines = self.text.split("\n")
            for i, line in enumerate(lines):
                if self.__font_size > 0:
                    self.__draw_line(line, y + i * (9 * self.__font_size), camera_x, camera_y)
                else:
                    self.__draw_line(line, y + i * 6, camera_x, camera_y)
            return
        
        self.__draw_line(self.text, y, camera_x, camera_y)
        
        # if self.__relative:
        #     x += camera_x
        #     y += camera_y

        # if self.__shadow:
        #     Text(self.text, self.__shadow_x, self.__shadow_y, self.__shadow_color, self.__font_size, self.__anchor, relative=self.__relative, underline=self.__underline, underline_color=self.__shadow_color, wavy=self.__wavy, wave_height=self.__wave_height, wave_speed=self.__wave_speed).draw(camera_x, camera_y)

        # if self.__font_size > 0:
        #     for char_index, char in enumerate(self.text):
        #         char_y = y + math.cos(pyxel.frame_count / self.__wave_speed + char_index * 0.3) * self.__wave_height if self.__wavy else y

        #         if char in characters_matrices:
        #             char_matrix = characters_matrices[char]
        #             char_width = len(char_matrix[0]) * self.__font_size

        #             x += random.uniform(-self.__glitch_intensity, self.__glitch_intensity)
        #             char_y += random.uniform(-self.__glitch_intensity, self.__glitch_intensity)
                    
        #             for row_index, row in enumerate(char_matrix):
        #                 for col_index, pixel in enumerate(row):
        #                     if pixel:
        #                         pyxel.rect(x + col_index * self.__font_size, char_y + row_index * self.__font_size + (1 * self.__font_size if char in "gjpqy" else 0), self.__font_size, self.__font_size, self.__text_colors[char_index % len(self.__text_colors)])
                    
        #             x += char_width + self.__font_size

        #     if self.__underline:
        #         pyxel.rect(self.x, y + self.__text_height - self.__font_size, self.__text_width, self.__font_size, self.__underline_color)
        # else:
        #     for char_index, char in enumerate(self.text):
        #         char_y = y + math.cos(pyxel.frame_count / self.__wave_speed + char_index * 0.3) * self.__wave_height if self.__wavy else y
        #         x += random.uniform(-self.__glitch_intensity, self.__glitch_intensity)
        #         char_y += random.uniform(-self.__glitch_intensity, self.__glitch_intensity)
        #         pyxel.text(x, char_y, char, self.__text_colors[char_index % len(self.__text_colors)])
        #         x += 4

class Button:

    def __init__(self, text:str, x:int, y:int, background_color:int, text_colors:list|int, hover_background_color:int, hover_text_colors:list|int, font_size:int=1, border:bool=False, border_color:int=0, color_mode:int=NORMAL_COLOR_MODE, color_speed:int=10, relative:bool=True, anchor:int=ANCHOR_TOP_LEFT, command=None):
        self.__x = x
        self.__y = y
        self.__width, self.__height = text_size(text, font_size)
        self.__width += 4 if border else 2
        self.__height += 4 if border else 2
        self.__background_color = background_color
        self.__hover_background_color = hover_background_color
        self.__border = border
        self.__border_color = border_color
        self.__relative = relative
        self.__command = command

        self.__x, self.__y = get_anchored_position(self.__x, self.__y, self.__width, self.__height, anchor)

        self.__text = Text(text, self.__x + 2 if border else self.__x + 1, self.__y + 2 if border else self.__y + 1, text_colors, font_size, color_mode=color_mode, color_speed=color_speed, relative=relative)
        self.__hover_text = Text(text, self.__x + 2 if border else self.__x + 1, self.__y + 2 if border else self.__y + 1, hover_text_colors, font_size, color_mode=color_mode, color_speed=color_speed, relative=relative)

    def is_hovered(self, camera_x:int=0, camera_y:int=0)-> bool:
        if self.__x <= pyxel.mouse_x < self.__x + self.__width and self.__y <= pyxel.mouse_y < self.__y + self.__height and self.__relative:
            return True
        if self.__x <= camera_x + pyxel.mouse_x < self.__x + self.__width and self.__y <= camera_y + pyxel.mouse_y < self.__y + self.__height and not self.__relative:
            return True
        
    def update(self, camera_x:int=0, camera_y:int=0):
        self.__text.update()
        self.__hover_text.update()
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and self.is_hovered(camera_x, camera_y) and self.__command:
            self.__command()

    def draw(self, camera_x:int=0, camera_y:int=0):
        x = camera_x + self.__x if self.__relative else self.__x
        y = camera_y + self.__y if self.__relative else self.__y
        if self.is_hovered(camera_x, camera_y):
            pyxel.rect(x, y, self.__width, self.__height, self.__hover_background_color)
            self.__hover_text.draw(camera_x, camera_y)
        else:
            pyxel.rect(x, y, self.__width, self.__height, self.__background_color)
            self.__text.draw(camera_x, camera_y)
        if self.__border:
            pyxel.rectb(x, y, self.__width, self.__height, self.__border_color)

class IconButton:

    def __init__(self, x:int, y:int, background_color:int, hover_background_color:int, sprite:Sprite, border:bool=False, border_color:int=0, relative:bool=True, anchor:int=ANCHOR_TOP_LEFT, command=None):
        self.__x = x + 1 if not border else x + 2
        self.__y = y + 1 if not border else y + 2
        self.__width = sprite.w + 2 if not border else sprite.w + 4
        self.__height = sprite.h + 2 if not border else sprite.h + 4
        self.__background_color = background_color
        self.__hover_background_color = hover_background_color
        self.__sprite = sprite
        self.__border = border
        self.__border_color = border_color
        self.__relative = relative
        self.__command = command

        self.__x, self.__y = get_anchored_position(self.__x, self.__y, self.__width, self.__height, anchor)

    def is_hovered(self, camera_x:int=0, camera_y:int=0)-> bool:
        if self.__x - 2 < pyxel.mouse_x < self.__x + self.__sprite.w + 1 and self.__y - 2 < pyxel.mouse_y < self.__y + self.__sprite.h + 1 and self.__relative:
            return True
        elif self.__x - 2 < camera_x + pyxel.mouse_x < self.__x + self.__sprite.w + 1 and self.__y - 2 < camera_y + pyxel.mouse_y < self.__y + self.__sprite.h + 1 and not self.__relative:
            return True
        
    def update(self, camera_x:int=0, camera_y:int=0):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and self.is_hovered(camera_x, camera_y) and self.__command:
            self.__command()

    def draw(self, camera_x:int=0, camera_y:int=0):
        x = camera_x + self.__x if self.__relative else self.__x
        y = camera_y + self.__y if self.__relative else self.__y

        if self.__border:
            pyxel.rectb(x - 2, y - 2, self.__sprite.w + 4, self.__sprite.h + 4, self.__border_color)
        if self.is_hovered(camera_x, camera_y):
            pyxel.rect(x - 1, y - 1, self.__sprite.w + 2, self.__sprite.h + 2, self.__hover_background_color)
        else:
            pyxel.rect(x - 1, y - 1, self.__sprite.w + 2, self.__sprite.h + 2, self.__background_color)
        pyxel.blt(x, y, self.__sprite.img, self.__sprite.u, self.__sprite.v, self.__sprite.w, self.__sprite.h, self.__sprite.colkey)

class Entry:

    def __init__(self, x:int, y:int, width:int, text_color:int, unfocused_color:int, focused_color:int, font_size:int=1, text_cursor_color:int=0, relative:bool=True, anchor:int=ANCHOR_TOP_LEFT):
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = text_size("A", font_size)[1]
        self.__font_size = font_size
        self.__unfocused_color = unfocused_color
        self.__focused_color = focused_color
        self.__focused = False
        self.__text_cursor_color = text_cursor_color
        self.__relative = relative

        self.__x, self.__y = get_anchored_position(self.__x, self.__y, self.__width, self.__height, anchor)

        self.__text = Text("", self.__x + 1, self.__y + 1, text_color, font_size, relative=relative)

    def is_hovered(self, camera_x:int=0, camera_y:int=0)-> bool:
        if self.__x <= pyxel.mouse_x < self.__x + self.__width and self.__y <= pyxel.mouse_y < self.__y + self.__height + 2 and self.__relative:
            return True
        elif self.__x <= camera_x + pyxel.mouse_x < self.__x + self.__width and self.__y <= camera_y + pyxel.mouse_y < self.__y + self.__height + 2 and not self.__relative:
            return True
        
    def update(self, camera_x:int=0, camera_y:int=0):
        self.__text.update()
        if self.is_hovered(camera_x, camera_y) and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.__focused = True
        elif pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.__focused = False

        if self.__focused:
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.__focused = False
            elif pyxel.btnp(pyxel.KEY_BACKSPACE):
                self.__text.text = self.__text.text[:-1]
            for k, v in keys_to_chars.items():
                if pyxel.btnp(pyxel.KEY_LSHIFT, hold=1, repeat=1) and pyxel.btnp(k):
                    self.__text.text += v.upper()
                elif pyxel.btnp(k):
                    self.__text.text += v
            if text_size(self.__text.text, self.__font_size)[0] > self.__width - 1:
                self.__text.text = self.__text.text[:-1]
                self.__focused = False

    def draw(self, camera_x:int=0, camera_y:int=0):
        x = camera_x + self.__x if self.__relative else self.__x
        y = camera_y + self.__y if self.__relative else self.__y
        pyxel.rect(x, y, self.__width, self.__height + 2, self.__focused_color if self.__focused else self.__unfocused_color)
        self.__text.draw(camera_x, camera_y)
        if self.__focused and pyxel.frame_count % (30 * 2) < 30:
            pyxel.rect(x + self.__font_size + 1 + text_size(self.__text.text, self.__font_size)[0], y + 1, self.__font_size, self.__height, self.__text_cursor_color)

class UIBar:

    def __init__(self, x:int, y:int, width:int, height:int, border_color:int, bar_color:int, starting_value:int, max_value:int, relative:bool=True, horizontal:bool=True, regen:bool=False, speed_regen:int=0.5, value_regen:int=1, anchor:int=ANCHOR_TOP_LEFT):
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__border_color = border_color
        self.__bar_color = bar_color

        self.__current_value = starting_value
        self.__max_value = max_value
        self.__relative = relative
        self.__horizontal = horizontal

        self.__regen = regen
        self.__speed_regen = speed_regen
        self.__regen_timer = 0
        self.__value_regen = value_regen
        self.__bar_width = 0
        self.__bar_height = 0

        self.__x, self.__y = get_anchored_position(self.__x, self.__y, self.__width + 2, self.__height + 2, anchor)

    def update(self):
        self.__regen_timer += 1
        if self.__current_value < 0:
            self.__current_value = 0
        if self.__current_value < self.__max_value and self.__regen and self.__regen_timer >= self.__speed_regen:
            self.__regen_timer = 0
            self.__current_value += self.__value_regen
        while self.__current_value > self.__max_value:
            self.__current_value -= 1
        self.__bar_width = self.__width * self.__current_value / self.__max_value
        self.__bar_height = self.__height * self.__current_value / self.__max_value

    def draw(self, camera_x:int=0, camera_y:int=0):
        if self.__relative:
            if self.__horizontal:
                pyxel.rect(camera_x + self.__x + 1, camera_y + self.__y + 1, self.__bar_width, self.__height, self.__bar_color)
                pyxel.rectb(camera_x + self.__x, camera_y + self.__y, self.__width + 2, self.__height + 2, self.__border_color)
            else:
                pyxel.rect(camera_x + self.__x + 1, camera_y + self.__y + self.__height - self.__bar_height + 1, self.__width, self.__bar_height, self.__bar_color)
                pyxel.rectb(camera_x + self.__x, camera_y + self.__y, self.__width + 2, self.__height + 2, self.__border_color)
        else:
            if self.__horizontal:
                pyxel.rect(self.__x + 1, self.__y + 1, self.__bar_width, self.__height, self.__bar_color)
                pyxel.rectb(self.__x, self.__y, self.__width + 2, self.__height + 2, self.__border_color)
            else:
                pyxel.rect(self.__x + 1, self.__y + self.__height - self.__bar_height + 1, self.__width, self.__bar_height, self.__bar_color)
                pyxel.rectb(self.__x, self.__y, self.__width + 2, self.__height + 2, self.__border_color)

class Slider:

    def __init__(self, x:int, y:int, width:int, height:int, corner_radius:int, slider_color:int, button_color:int, button_hover_color:int, min_value:int=0, max_value:int=100, relative:bool=True):
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__corner_radius = corner_radius
        self.__slider_color = slider_color
        self.__focused = False

        self.__button_x = x
        self.__button_y = y
        self.__button_size = height
        self.__button_color = button_color
        self.__button_hover_color = button_hover_color

        self.__min_value = min_value
        self.__max_value = max_value

        self.__relative = relative

    def get_value(self)-> int|float:
        return self.__min_value + (self.__button_x - self.__x) / self.__width * (self.__max_value - self.__min_value)

    def is_hovered(self, camera_x:int=0, camera_y:int=0)-> bool:
        if ((pyxel.mouse_x - self.__button_x)**2 + (pyxel.mouse_y - (self.__button_y + self.__button_size // 2))**2)**0.5 <= self.__button_size and self.__relative:
            return True
        elif ((camera_x + pyxel.mouse_x - self.__button_x)**2 + (camera_y + pyxel.mouse_y - (self.__button_y + self.__button_size // 2))**2)**0.5 <= self.__button_size and not self.__relative:
            return True

    def update(self, camera_x:int=0, camera_y:int=0):
        if self.is_hovered(camera_x, camera_y) and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.__focused = True

        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
            self.__focused = False

        if self.__focused and self.__relative:
            self.__button_x = pyxel.mouse_x
        elif self.__focused and not self.__relative:
            self.__button_x = camera_x + pyxel.mouse_x

        self.__button_x = clamp(self.__button_x, self.__x, self.__x + self.__width)

    def draw(self, camera_x:int=0, camera_y:int=0):
        if self.__relative:
            rounded_rect(self.__x + camera_x, self.__y + camera_y, self.__width, self.__height, self.__corner_radius, self.__slider_color)
            pyxel.circ(self.__button_x + camera_x, self.__button_y + self.__button_size // 2 + camera_y, self.__button_size, self.__button_hover_color if self.__focused or self.is_hovered(camera_x, camera_y) else self.__button_color)
        else:
            rounded_rect(self.__x, self.__y, self.__width, self.__height, self.__corner_radius, self.__slider_color)
            pyxel.circ(self.__button_x, self.__button_y + self.__button_size // 2, self.__button_size, self.__button_hover_color if self.__focused or self.is_hovered(camera_x, camera_y) else self.__button_color)

class Dialog:

    def __init__(self, lines:list, background_color:int, names_colors:list|int, text_colors:list|int, border:bool=False, border_color:int=0, sound:bool=False, channel:int=0, sound_number:int=0):
        self.lines = lines
        self.background_color = background_color
        self.names_colors = names_colors
        self.text_colors = text_colors
        self.border = border
        self.border_color = border_color
        self.sound = sound
        self.channel = channel
        self.sound_number = sound_number

class DialogManager:

    def __init__(self, relative_start_x:int, relative_start_y:int, relative_end_x:int, relative_end_y:int, width:int, height:int, char_speed:int=3, next_key:int=pyxel.KEY_SPACE):
        self.__start_x = relative_start_x
        self.__start_y = relative_start_y
        self.__end_x = relative_end_x
        self.__end_y = relative_end_y
        self.__x = relative_start_x
        self.__y = relative_start_y
        self.__width = width
        self.__height = height
        self.__background_color = 0
        self.__names_colors = 0
        self.__text_colors = []
        self.__border = False
        self.__border_color = 0
        self.__next_key = next_key

        self.__started = False
        self.__open = False
        self.__dialog = None

        self.__current_line = 0
        self.__char_index = 0
        self.__char_speed = char_speed
        self.__frame_count = 0

    def is_dialog(self)-> bool:
        return self.__started

    def start_dialog(self, dialog:Dialog):
        if not self.__started:
            self.__background_color = dialog.background_color
            self.__names_colors = dialog.names_colors
            self.__text_colors = dialog.text_colors
            self.__border = dialog.border
            self.__border_color = dialog.border_color

            self.__started = True
            self.__dialog = dialog
            self.__current_line = 0
            self.__char_index = 0
            self.__frame_count = 0

    def stop_dialog(self):
        self.__started = False
        self.__open = False
        self.__dialog = None

    def update(self):
        if self.__started:
            self.__x = lerp(self.__x, self.__end_x, 0.15)
            self.__y = lerp(self.__y, self.__end_y, 0.15)

            if abs(self.__x - self.__end_x) < 1 and abs(self.__y - self.__end_y) < 1:
                self.__open = True

            if self.__open:
                if self.__char_index < len(self.__dialog.lines[self.__current_line][1]):
                    if pyxel.btnp(self.__next_key):
                        self.__char_index = len(self.__dialog.lines[self.__current_line][1])
                        if self.__dialog.sound:
                            pyxel.play(self.__dialog.channel, self.__dialog.sound_number)
                    self.__frame_count += 1
                    if self.__frame_count % self.__char_speed == 0:
                        if self.__dialog.sound:
                            pyxel.play(self.__dialog.channel, self.__dialog.sound_number)
                        self.__char_index += 1
                else:
                    if pyxel.btnp(self.__next_key):
                        if self.__current_line < len(self.__dialog.lines) - 1:
                            self.__current_line += 1
                            self.__char_index = 0
                            self.__frame_count = 0
                        else:
                            self.__started = False
                            self.__open = False

        else:
            self.__x = lerp(self.__x, self.__start_x, 0.15)
            self.__y = lerp(self.__y, self.__start_y, 0.15)

    def draw(self, camera_x:int=0, camera_y:int=0):
        if abs(self.__x - self.__start_x) < 1 and abs(self.__y - self.__start_y) < 1:
            return

        pyxel.rect(camera_x + self.__x, camera_y + self.__y, self.__width, self.__height, self.__background_color)
        if pyxel.frame_count % (30 * 2) < 50:
            pyxel.text(camera_x + self.__x + self.__width - len(keys_to_representation.get(self.__next_key, "") * 4) - 1, 
                    camera_y + self.__y + self.__height - 7, 
                    keys_to_representation.get(self.__next_key, ""), 
                    self.__text_colors if isinstance(self.__text_colors, int) else self.__text_colors[0])
        if self.__border:
            pyxel.rectb(camera_x + self.__x, camera_y + self.__y, self.__width, self.__height, self.__border_color)
        if self.__open:
            Text(self.__dialog.lines[self.__current_line][0], camera_x + self.__x + 2, camera_y + self.__y + 2, self.__names_colors, 1).draw()
        if self.__dialog:
            visible_text = self.__dialog.lines[self.__current_line][1][:self.__char_index]
            Text(visible_text, camera_x + self.__x + 2, camera_y + self.__y + 14, self.__text_colors, 1).draw()

def text_size(text:str, font_size:int=1)-> tuple:
    lines = text.split("\n")
    if font_size == 0:
        return (max(len(line) * 4 for line in lines), 6 * len(lines))
    text_width = max(sum(len(characters_matrices[char][0]) * font_size + font_size for char in line) - font_size for line in lines)
    text_height = (9 * font_size + 1) * len(lines)

    return (text_width, text_height)

def corrupted_text(text:str, corruption_letters:list|str, corruption_chance:float=0.1)-> str:
    return "".join([random.choice(corruption_letters) if random.random() < corruption_chance else char for char in text])
