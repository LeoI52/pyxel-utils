from scripts.other import get_anchored_position, clamp
from scripts.draw import Sprite, rounded_rect
from scripts.vars import *
from scripts.gui import Text
import pyxel

pyxel.init(128, 128)
pyxel.mouse(True)

def lerp(a, b, t):
    return a + (b - a) * t

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

def update():
    pass

def draw():
    pyxel.cls(0)
    
pyxel.run(update, draw)