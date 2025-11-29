import pyxel
import random
import math
from scripts.vars import *

pyxel.init(8, 8, fps=60)
pyxel.fullscreen(True)
pyxel.colors.from_list([0x000000, 0x1D2B53, 0x7E2553, 0x008751, 0xAB5236, 0x5F574F, 0xC2C3C7, 0xFFF1E8, 0xFF004D, 0xFFA300, 0xFFEC27, 0x00E436, 0x29ADFF, 0x83769C, 0xFF77A8, 0xFFCCAA])

def lerp(a, b, t):
    return a + (b - a) * t

# class Slider:

#     def __init__(self, x:int, y:int, width:int, height:int, corner_radius:int, slider_color:int, button_color:int, button_hover_color:int, min_value:int=0, max_value:int=100, relative:bool=True):
#         self.__x = x
#         self.__y = y
#         self.__width = width
#         self.__height = height
#         self.__corner_radius = corner_radius
#         self.__slider_color = slider_color
#         self.__focused = False

#         self.__button_x = x
#         self.__button_y = y
#         self.__button_size = height
#         self.__button_color = button_color
#         self.__button_hover_color = button_hover_color

#         self.__min_value = min_value
#         self.__max_value = max_value

#         self.__relative = relative

#     def get_value(self)-> int|float:
#         return self.__min_value + (self.__button_x - self.__x) / self.__width * (self.__max_value - self.__min_value)

#     def is_hovered(self, camera_x:int=0, camera_y:int=0)-> bool:
#         if ((pyxel.mouse_x - self.__button_x)**2 + (pyxel.mouse_y - (self.__button_y + self.__button_size // 2))**2)**0.5 <= self.__button_size and self.__relative:
#             return True
#         elif ((camera_x + pyxel.mouse_x - self.__button_x)**2 + (camera_y + pyxel.mouse_y - (self.__button_y + self.__button_size // 2))**2)**0.5 <= self.__button_size and not self.__relative:
#             return True

#     def update(self, camera_x:int=0, camera_y:int=0):
#         if self.is_hovered(camera_x, camera_y) and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
#             self.__focused = True

#         if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
#             self.__focused = False

#         if self.__focused and self.__relative:
#             self.__button_x = pyxel.mouse_x
#         elif self.__focused and not self.__relative:
#             self.__button_x = camera_x + pyxel.mouse_x

#         self.__button_x = clamp(self.__button_x, self.__x, self.__x + self.__width)

#     def draw(self, camera_x:int=0, camera_y:int=0):
#         if self.__relative:
#             rounded_rect(self.__x + camera_x, self.__y + camera_y, self.__width, self.__height, self.__corner_radius, self.__slider_color)
#             pyxel.circ(self.__button_x + camera_x, self.__button_y + self.__button_size // 2 + camera_y, self.__button_size, self.__button_hover_color if self.__focused or self.is_hovered(camera_x, camera_y) else self.__button_color)
#         else:
#             rounded_rect(self.__x, self.__y, self.__width, self.__height, self.__corner_radius, self.__slider_color)
#             pyxel.circ(self.__button_x, self.__button_y + self.__button_size // 2, self.__button_size, self.__button_hover_color if self.__focused or self.is_hovered(camera_x, camera_y) else self.__button_color)

# class Dialog:

#     def __init__(self, lines:list, background_color:int, names_colors:list|int, text_colors:list|int, border:bool=False, border_color:int=0, sound:bool=False, channel:int=0, sound_number:int=0):
#         self.lines = lines
#         self.background_color = background_color
#         self.names_colors = names_colors
#         self.text_colors = text_colors
#         self.border = border
#         self.border_color = border_color
#         self.sound = sound
#         self.channel = channel
#         self.sound_number = sound_number

# class DialogManager:

#     def __init__(self, relative_start_x:int, relative_start_y:int, relative_end_x:int, relative_end_y:int, width:int, height:int, char_speed:int=3, next_key:int=pyxel.KEY_SPACE):
#         self.__start_x = relative_start_x
#         self.__start_y = relative_start_y
#         self.__end_x = relative_end_x
#         self.__end_y = relative_end_y
#         self.__x = relative_start_x
#         self.__y = relative_start_y
#         self.__width = width
#         self.__height = height
#         self.__background_color = 0
#         self.__names_colors = 0
#         self.__text_colors = []
#         self.__border = False
#         self.__border_color = 0
#         self.__next_key = next_key

#         self.__started = False
#         self.__open = False
#         self.__dialog = None

#         self.__current_line = 0
#         self.__char_index = 0
#         self.__char_speed = char_speed
#         self.__frame_count = 0

#     def is_dialog(self)-> bool:
#         return self.__started

#     def start_dialog(self, dialog:Dialog):
#         if not self.__started:
#             self.__background_color = dialog.background_color
#             self.__names_colors = dialog.names_colors
#             self.__text_colors = dialog.text_colors
#             self.__border = dialog.border
#             self.__border_color = dialog.border_color

#             self.__started = True
#             self.__dialog = dialog
#             self.__current_line = 0
#             self.__char_index = 0
#             self.__frame_count = 0

#     def stop_dialog(self):
#         self.__started = False
#         self.__open = False
#         self.__dialog = None

#     def update(self):
#         if self.__started:
#             self.__x = lerp(self.__x, self.__end_x, 0.15)
#             self.__y = lerp(self.__y, self.__end_y, 0.15)

#             if abs(self.__x - self.__end_x) < 1 and abs(self.__y - self.__end_y) < 1:
#                 self.__open = True

#             if self.__open:
#                 if self.__char_index < len(self.__dialog.lines[self.__current_line][1]):
#                     if pyxel.btnp(self.__next_key):
#                         self.__char_index = len(self.__dialog.lines[self.__current_line][1])
#                         if self.__dialog.sound:
#                             pyxel.play(self.__dialog.channel, self.__dialog.sound_number)
#                     self.__frame_count += 1
#                     if self.__frame_count % self.__char_speed == 0:
#                         if self.__dialog.sound:
#                             pyxel.play(self.__dialog.channel, self.__dialog.sound_number)
#                         self.__char_index += 1
#                 else:
#                     if pyxel.btnp(self.__next_key):
#                         if self.__current_line < len(self.__dialog.lines) - 1:
#                             self.__current_line += 1
#                             self.__char_index = 0
#                             self.__frame_count = 0
#                         else:
#                             self.__started = False
#                             self.__open = False

#         else:
#             self.__x = lerp(self.__x, self.__start_x, 0.15)
#             self.__y = lerp(self.__y, self.__start_y, 0.15)

#     def draw(self, camera_x:int=0, camera_y:int=0):
#         if abs(self.__x - self.__start_x) < 1 and abs(self.__y - self.__start_y) < 1:
#             return

#         pyxel.rect(camera_x + self.__x, camera_y + self.__y, self.__width, self.__height, self.__background_color)
#         if pyxel.frame_count % (30 * 2) < 50:
#             pyxel.text(camera_x + self.__x + self.__width - len(KEYS_TO_NAME.get(self.__next_key, "") * 4) - 1, 
#                     camera_y + self.__y + self.__height - 7, 
#                     KEYS_TO_NAME.get(self.__next_key, ""), 
#                     self.__text_colors if isinstance(self.__text_colors, int) else self.__text_colors[0])
#         if self.__border:
#             pyxel.rectb(camera_x + self.__x, camera_y + self.__y, self.__width, self.__height, self.__border_color)
#         if self.__open:
#             Text(self.__dialog.lines[self.__current_line][0], camera_x + self.__x + 2, camera_y + self.__y + 2, self.__names_colors, 1).draw()
#         if self.__dialog:
#             visible_text = self.__dialog.lines[self.__current_line][1][:self.__char_index]
#             Text(visible_text, camera_x + self.__x + 2, camera_y + self.__y + 14, self.__text_colors, 1).draw()

class Drop:

    def __init__(self, x, y, length, target, sp_x=2, sp_y=4):
        self.x = x
        self.y = y
        self.len = int(length)
        self.target = target
        self.sp_x = sp_x
        self.sp_y = sp_y

    def update(self):
        self.x += self.sp_x
        self.y += self.sp_y

    def draw(self):
        for i in range(self.len, -1, -1):
            pyxel.pset(int(self.x - (i // 2)), int(self.y - i), 7)

class Ripple:

    def __init__(self, x, y, life):
        self.x = x
        self.y = y
        self.life = life
        self.t = 1
        self.width = 2
        self.height = 1

    def update(self):
        self.t += 0.5

    def draw(self):
        pyxel.ellib(self.x - (self.width / 2) * self.t, self.y - (self.height / 2) * self.t, self.width * self.t, self.height * self.t, 7)

class RainOverlay:

    def __init__(self, num_drops=50):
        self.drops = [
            Drop(
                x=-100 + random.uniform(0, 128),
                y=-1 * random.uniform(0, 300),
                length=3 + random.uniform(0, 10),
                target=80 + random.uniform(0, 68),
            )
            for _ in range(num_drops)
        ]
        self.ripples = []

    def update(self):
        for d in self.drops:
            d.update()

        for r in self.ripples:
            r.update()

        for i in range(len(self.drops) - 1, -1, -1):
            if self.drops[i].y >= self.drops[i].target:
                old = self.drops.pop(i)
                self.drops.append(
                    Drop(
                        x=-100 + random.uniform(0, 128),
                        y=-1 * random.uniform(0, 300),
                        length=3 + random.uniform(0, 10),
                        target=80 + random.uniform(0, 68),
                    )
                )
                self.ripples.append(Ripple(old.x, old.y, life=10 + random.uniform(0, 5)))

        for i in range(len(self.ripples) - 1, -1, -1):
            if self.ripples[i].t > self.ripples[i].life:
                self.ripples.pop(i)

    def draw(self):
        for d in self.drops:
            d.draw()
        for r in self.ripples:
            r.draw()

chars_list = list(FONT_DEFAULT.keys())
char = 0

def update():
    global char
    if pyxel.btnp(pyxel.KEY_RIGHT):
        char += 1
    if pyxel.btnp(pyxel.KEY_LEFT):
        char -= 1

def draw():
    pyxel.cls(0)

    pyxel.text(0, 0, chars_list[char], 7)

pyxel.run(update, draw)

