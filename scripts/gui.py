"""
@author : Léo Imbert
@created : 15/10/2024
@updated : 29/11/2025
"""

from draw import rounded_rect, rounded_rectb
from other import *
from vars import *
import random
import math

#? -------------------- GUIs -------------------- ?#

class Text:
    
    def __init__(self, text:str, x:int, y:int, text_colors:int|list, font:dict, font_size:int=1, anchor=TOP_LEFT, color=(HORIZONTAL, NORMAL_COLOR_MODE, 20), wave=None, shadow=None, outline_color=None, relative:bool=True):
        """
        color = (color direction, color mode, color frames)  
        wave = (amplitude, speed, character spacing)  
        shadow = (color, offset x, offset y)
        """
        self.text = text
        self.x, self.y = x, y
        self.text_colors = text_colors
        self.font_size = font_size
        self.font = font
        self.anchor = anchor
        self.color_dir = color[0]
        self.color_mode = color[1]
        self.color_frames = color[2]
        self.wave = wave
        self.shadow = shadow
        self.outline_color = outline_color
        self.relative = relative

        self.initialize()

    def initialize(self):
        self.y = get_anchored_position_y(self.y, text_height(self.text, self.font, self.font_size), self.anchor)
        self.text_colors = [self.text_colors] if isinstance(self.text_colors, int) else self.text_colors
        self.o_text_colors = [x for x in self.text_colors]
        self.__last_change_color_time = pyxel.frame_count

    def _draw_line(self, text:str, y:int, camera_x:int=0, camera_y:int=0):
        x = get_anchored_position_x(self.x, text_width(text, self.font, self.font_size), self.anchor)

        if self.relative:
            x += camera_x
            y += camera_y

        if self.outline_color != None:
            Text(text, x + self.font_size, y, self.outline_color, self.font, self.font_size, wave=self.wave).draw()
            Text(text, x - self.font_size, y, self.outline_color, self.font, self.font_size, wave=self.wave).draw()
            Text(text, x, y + self.font_size, self.outline_color, self.font, self.font_size, wave=self.wave).draw()
            Text(text, x, y - self.font_size, self.outline_color, self.font, self.font_size, wave=self.wave).draw()
        elif self.shadow:
            Text(text, x + self.shadow[1] * self.font_size, y + self.shadow[2] * self.font_size, self.shadow[0], self.font, self.font_size, wave=self.wave).draw()

        for char_index, char in enumerate(text):
            char_matrix = self.font[char]
            char_width = len(char_matrix[0]) * self.font_size
            char_height = len(char_matrix)
            char_y = y + math.cos(pyxel.frame_count / self.wave[1] + char_index * self.wave[2]) * self.wave[0] if self.wave else y
            
            for row_index, row in enumerate(char_matrix):
                for col_index, pixel in enumerate(row):
                    if pixel:

                        if self.color_dir == HORIZONTAL:
                            c = self.text_colors[char_index % len(self.text_colors)]
                        elif self.color_dir == VERTICAL:
                            c = self.text_colors[int(row_index * len(self.text_colors) / char_height)]

                        pyxel.rect(x + col_index * self.font_size, char_y + row_index * self.font_size, self.font_size, self.font_size, c)
            
            x += char_width + self.font_size

    def update(self):
        if self.color_mode != NORMAL_COLOR_MODE and pyxel.frame_count - self.__last_change_color_time >= self.color_frames:
            if self.color_mode == ROTATING_COLOR_MODE:
                self.__last_change_color_time = pyxel.frame_count
                self.text_colors = [self.text_colors[-1]] + self.text_colors[:-1]
            elif self.color_mode == RANDOM_COLOR_MODE:
                self.__last_change_color_time = pyxel.frame_count
                self.text_colors = [random.choice(self.o_text_colors) for _ in range(len(self.text))]

    def draw(self, camera_x:int=0, camera_y:int=0):
        if "\n" in self.text:
            lines = self.text.split("\n")
            y = self.y
            for line in lines:
                self._draw_line(line, y, camera_x, camera_y)
                y += text_height(line, self.font, self.font_size) + self.font_size
        else:
            self._draw_line(self.text, self.y, camera_x, camera_y)

class Button:

    def __init__(self, text:str, x:int, y:int, color:int, hover_color:int, text_colors:int|list, hover_text_colors:int|list, font:dict, font_size:int=1, corner_radius:int=4, width:int=0, height:int=0, anchor=TOP_LEFT, on_click=None, border=None, padding:int=2, relative:bool=True):
        """
        border = (border width, border color)
        """
        self.text = text
        self.x, self.y = x, y
        self.color, self.hover_color = color, hover_color
        self.text_colors, self.hover_text_colors = text_colors, hover_text_colors
        self.font, self.font_size = font, font_size
        self.corner_radius = corner_radius
        self.width, self.height = width, height
        self.anchor = anchor
        self.on_click = on_click
        self.border = border
        self.padding = padding
        self.relative = relative

        self.initialize()

    def initialize(self):
        tw, th = text_size(self.text, self.font, self.font_size)
        self.width, self.height = max(self.width, tw), max(self.height, th)
        if self.width == tw: self.width += 2 * self.padding
        if self.height == th: self.height += 2 * self.padding
        if self.border:
            self.width += self.border[0] * 2
            self.height += self.border[0] * 2
        self.width += self.corner_radius // 2
        self.height += self.corner_radius // 2
        self.x, self.y = get_anchored_position(self.x, self.y, self.width, self.height, self.anchor)
        self.text_obj = Text(self.text, self.x + self.width // 2, self.y + self.height // 2, self.text_colors, self.font, self.font_size, anchor=CENTER, relative=self.relative)
        self.hover_text_obj = Text(self.text, self.x + self.width // 2, self.y + self.height // 2, self.hover_text_colors, self.font, self.font_size, anchor=CENTER, relative=self.relative)

    def is_hovered(self, camera_x:int=0, camera_y:int=0)-> bool:
        mx = pyxel.mouse_x + (camera_x if not self.relative else 0)
        my = pyxel.mouse_y + (camera_y if not self.relative else 0)
        return (self.x <= mx < self.x + self.width and self.y <= my < self.y + self.height)

    def update(self, camera_x:int=0, camera_y:int=0):
        if self.is_hovered(camera_x, camera_y) and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and self.on_click:
            self.on_click()

    def draw(self, camera_x:int=0, camera_y:int=0):
        x = camera_x + self.x if self.relative else self.x
        y = camera_y + self.y if self.relative else self.y

        if self.is_hovered(camera_x, camera_y):
            rounded_rect(x, y, self.width, self.height, self.corner_radius, self.hover_color)
            self.hover_text_obj.draw(camera_x, camera_y)
        else:
            rounded_rect(x, y, self.width, self.height, self.corner_radius, self.color)
            self.text_obj.draw(camera_x, camera_y)

        if self.border:
            bw, bc = self.border
            x, y, w, h, c = x, y, self.width, self.height, self.corner_radius
            for _ in range(bw):
                rounded_rectb(x, y, w, h, c, bc)
                x += 1; y += 1; w -= 2; h -= 2; c = max(0, c - 1)

class Entry:

    def __init__(self, x:int, y:int, width:int, color:int, focused_color:int, text_color:int, font:dict, font_size:int=1, corner_radius:int=4, anchor=TOP_LEFT, border=None, padding:int=2, relative:bool=True):
        """
        border = (border width, border color)
        """
        self.x, self.y = x, y
        self.width, self.text_width, self.height, self.text_height = width, width, 0, 0
        self.color, self.focused_color = color, focused_color
        self.text_color = text_color
        self.font, self.font_size = font, font_size
        self.corner_radius = corner_radius
        self.anchor = anchor
        self.border = border
        self.padding = padding
        self.relative = relative
        self.focused = False

        self.initialize()

    def initialize(self):
        self.height = self.text_height = text_size("".join(self.font.keys()), self.font, self.font_size)[1]
        self.width += 2 * self.padding
        self.height += 2 * self.padding
        if self.border:
            self.width += self.border[0] * 2
            self.height += self.border[0] * 2
        self.width += self.corner_radius // 2
        self.height += self.corner_radius // 2
        self.x, self.y = get_anchored_position(self.x, self.y, self.width, self.height, self.anchor)
        tx = self.x + self.padding + self.corner_radius // 4
        if self.border:
            tx += self.border[0]
        self.text_obj = Text("", tx, self.y + self.height // 2, self.text_color, self.font, self.font_size, anchor=LEFT, relative=self.relative)

    def __set_text(self):
        self.text_obj.y = self.y + self.height // 2
        self.text_obj.initialize()

    def is_hovered(self, camera_x:int=0, camera_y:int=0)-> bool:
        mx = pyxel.mouse_x + (camera_x if not self.relative else 0)
        my = pyxel.mouse_y + (camera_y if not self.relative else 0)
        return (self.x <= mx < self.x + self.width and self.y <= my < self.y + self.height)

    def update(self, camera_x:int=0, camera_y:int=0):
        if self.is_hovered(camera_x, camera_y) and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.focused = True
        elif pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.focused = False

        if self.focused:
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.focused = False
            elif pyxel.btnp(pyxel.KEY_BACKSPACE):
                self.text_obj.text = self.text_obj.text[:-1]
                self.__set_text()
            for k, v in KEYS_TO_CHAR.items():
                if pyxel.btnp(pyxel.KEY_LSHIFT, hold=1, repeat=1) and pyxel.btnp(k):
                    self.text_obj.text += v.upper()
                    self.__set_text()
                elif pyxel.btnp(k):
                    self.text_obj.text += v
                    self.__set_text()
            if text_size(self.text_obj.text, self.font, self.font_size)[0] > self.text_width:
                self.text_obj.text = self.text_obj.text[:-1]
                self.focused = False

    def draw(self, camera_x:int=0, camera_y:int=0):
        x = camera_x + self.x if self.relative else self.x
        y = camera_y + self.y if self.relative else self.y

        c = self.color if not self.focused else self.focused_color
        rounded_rect(x, y, self.width, self.height, self.corner_radius, c)
        self.text_obj.draw(camera_x, camera_y)
        if self.focused and (pyxel.frame_count // 20) % 2:
            pyxel.rect(x + self.font_size + text_size(self.text_obj.text, self.font, self.font_size)[0] + self.padding + self.corner_radius // 4, y + self.height // 2 - (self.text_height - 2) // 2, self.font_size, self.text_height - 2, 0)
        if self.border:
            bw, bc = self.border
            x, y, w, h, c = x, y, self.width, self.height, self.corner_radius
            for _ in range(bw):
                rounded_rectb(x, y, w, h, c, bc)
                x += 1; y += 1; w -= 2; h -= 2; c = max(0, c - 1)

#? -------------------- FUNCTIONS -------------------- ?#

def text_size(text:str, font:dict, font_size:int=1)-> tuple:
    if not text:    return 0, 0
    lines = text.split("\n")

    width = max(sum(len(font[c][0]) for c in line) + len(line) - 1 for line in lines)

    height = sum(max(len(font[c]) for c in line) for line in lines) + len(lines) - 1

    return width * font_size, height * font_size

def text_width(text:str, font:dict, font_size:int=1)-> tuple:
    if not text:    return 0
    lines = text.split("\n")

    width = max(sum(len(font[c][0]) for c in line) + len(line) - 1 for line in lines)

    return width * font_size

def text_height(text:str, font:dict, font_size:int=1)-> tuple:
    if not text:    return 0
    lines = text.split("\n")

    height = sum(max(len(font[c]) for c in line) for line in lines) + len(lines) - 1

    return height * font_size

def wrap_text_width(text:str, max_width:int, font_size:int, font:dict)-> str:
    words = text.split(" ")
    output_lines = []
    current_line = ""

    for word in words:
        test_line = word if current_line == "" else current_line + " " + word
        w, _ = text_size(test_line, font, font_size)

        if w <= max_width:
            current_line = test_line
        else:
            output_lines.append(current_line)
            current_line = word

    output_lines.append(current_line)
    return "\n".join(output_lines)

#? -------------------- EXAMPLE -------------------- ?#

if __name__ == "__main__":
    pyxel.init(228, 128, title="Gui.py Example", fps=60)
    pyxel.mouse(True)

    t1 = Text(wrap_text_width("Bonjour je suis le meilleur joueur", 118, 1, FONT_BOLD), 11, 10, [1, 2, 1, 2], FONT_BOLD, anchor=TOP_LEFT, color=(VERTICAL, ROTATING_COLOR_MODE, 20))
    b1 = Button("Click", 114, 100, 0, 7, 7, 0, FONT_DEFAULT, corner_radius=4, anchor=TOP, on_click=lambda:print("goog"), border=(1, 7), relative=False)
    e1 = Entry(10, 100, 50, 7, 13, 0, FONT_DEFAULT)

    def update():
        t1.update()
        b1.update()
        e1.update()

        if pyxel.btnp(pyxel.KEY_SPACE):
            t1.text = "Bonjour"
            t1.x = 114
            t1.y = 64
            t1.anchor = CENTER
            t1.initialize()

    def draw():
        pyxel.cls(12)

        pyxel.rect(10, 10, 120, 40, 7)
        t1.draw()
        b1.draw()
        e1.draw()

    pyxel.run(update, draw)