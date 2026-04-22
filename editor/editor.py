"""
@author : Léo Imbert
@created : 28/09/2025
@updated : 21/04/2026
"""

#? ---------- IMPORTATIONS ---------- ?#

import pyxel
import json
import os

#? ---------- CONSTANTS ---------- ?#

DEFAULT_PYXEL_COLORS = [0x000000, 0x2B335F, 0x7E2072, 0x19959C, 0x8B4852, 0x395C98, 0xA9C1FF, 0xEEEEEE, 0xD4186C, 0xD38441, 0xE9C35B, 0x70C6A9, 0x7696DE, 0xA3A3A3, 0xFF9798, 0xEDC7B0]

MOUSE_ICON = [[0,2],[2,1,2],[2,1,1,2],[2,1,1,1,2],[2,1,1,1,1,2],[2,1,1,2,2],[0,2,2,1,2]]

EMPTY_ICON = [
    [1]*16,
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1]*16]

SPRITE_ICON = [[1]*16,[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,1,1,1,1,1,1,0,0,0,0,1],[1,0,0,1,1,1,1,1,1,1,1,1,1,0,0,1],[1,0,0,1,1,1,1,1,1,1,1,1,1,0,0,1],[1,0,0,0,0,1,1,1,1,1,1,0,0,0,0,1],[1,0,0,0,0,1,1,1,1,1,1,0,0,0,0,1],[1,0,0,0,1,1,1,1,1,1,1,1,0,0,0,1],[1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1],[1,0,1,1,0,1,1,1,1,1,1,0,1,1,0,1],[1,0,0,0,0,1,1,1,1,1,1,0,0,0,0,1],[1,0,0,0,0,1,1,1,1,1,1,0,0,0,0,1],[1,0,0,1,1,1,1,0,0,1,1,1,1,0,0,1],[1,0,0,1,1,1,1,0,0,1,1,1,1,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1]*16]
TILEMAP_ICON = [[1]*16,[1]+[0]*14+[1],[1]+[0]*14+[1],[1,0,0,1,1,1,1,0,0,1,1,1,1,0,0,1],[1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1],[1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1],[1,0,0,1,1,1,1,0,0,1,1,1,1,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,1,1,1,1,0,0,1,1,1,1,0,0,1],[1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1],[1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1],[1,0,0,1,1,1,1,0,0,1,1,1,1,0,0,1],[1]+[0]*14+[1],[1]+[0]*14+[1],[1]*16]
AUTOTILE_ICON = [[1]*16,[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,1,1,1,1,1,1,1,1,1,1,0,0,1],[1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1],[1,0,0,1,0,1,1,1,1,1,1,0,1,0,0,1],[1,0,0,1,0,1,1,1,1,1,1,0,1,0,0,1],[1,0,0,1,0,1,1,1,1,1,1,0,1,0,0,1],[1,0,0,1,0,1,1,1,1,1,1,0,1,0,0,1],[1,0,0,1,0,1,1,1,1,1,1,0,1,0,0,1],[1,0,0,1,0,1,1,1,1,1,1,0,1,0,0,1],[1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1],[1,0,0,1,1,1,1,1,1,1,1,1,1,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1]*16]

SPRITE_EDITOR = 0
TILEMAP_EDITOR = 1
AUTOTILE_EDITOR = 2

SELECT_ICON = [[1]*16,[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,1,1,0,1,1,0,0,1,1,0,1,1,0,1],[1,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1],[1,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1],[1,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1],[1,0,1,1,0,1,1,0,0,1,1,0,1,1,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1]*16]
PEN_ICON = [[1]*16,[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,1],[1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,1],[1,0,0,0,0,0,0,0,1,0,0,0,0,1,0,1],[1,0,0,0,0,0,0,1,0,0,0,0,0,1,0,1],[1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,1],[1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1],[1,0,0,0,1,1,0,0,0,0,1,0,0,0,0,1],[1,0,0,1,0,0,1,0,0,1,0,0,0,0,0,1],[1,0,1,0,0,0,0,1,1,0,0,0,0,0,0,1],[1,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1],[1,0,1,1,0,0,1,0,0,0,0,0,0,0,0,1],[1,0,1,1,1,1,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1]*16]
MIRROR_ICON = [[1]*16,[1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1],[1,0,0,0,1,1,0,0,0,0,1,1,0,0,0,1],[1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1],[1,0,1,1,0,0,0,0,0,0,0,0,1,1,0,1],[1,0,1,0,0,0,0,1,1,0,0,0,0,1,0,1],[1,0,1,0,1,0,0,0,0,0,0,1,0,1,0,1],[1,0,1,0,0,0,0,1,1,0,0,0,0,1,0,1],[1,0,1,0,0,0,0,1,1,0,0,0,0,1,0,1],[1,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1],[1,0,1,0,0,0,0,1,1,0,0,0,0,1,0,1],[1,0,1,1,0,0,0,0,0,0,0,0,1,1,0,1],[1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1],[1,0,0,0,1,1,0,0,0,0,1,1,0,0,0,1],[1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1],[1]*16]
LINE_ICON = [[1]*16,[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,1],[1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1],[1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,1],[1,0,0,0,0,0,0,0,1,1,1,0,0,0,0,1],[1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,1],[1,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1],[1,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1],[1,0,0,0,1,1,1,0,0,0,0,0,0,0,0,1],[1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,1],[1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1]*16]
FILLED_RECT_ICON = [[1]*16,[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0]+[1]*10+[0,0,1],[1,0,0]+[1]*10+[0,0,1],[1,0,0]+[1]*10+[0,0,1],[1,0,0]+[1]*10+[0,0,1],[1,0,0]+[1]*10+[0,0,1],[1,0,0]+[1]*10+[0,0,1],[1,0,0]+[1]*10+[0,0,1],[1,0,0]+[1]*10+[0,0,1],[1,0,0]+[1]*10+[0,0,1],[1,0,0]+[1]*10+[0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1]*16]
RECT_ICON = [[1]*16,[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,1,1]+[1]*6+[1,1,0,0,1],[1,0,0,1,0]+[0]*6+[0,1,0,0,1],[1,0,0,1,0]+[0]*6+[0,1,0,0,1],[1,0,0,1,0]+[0]*6+[0,1,0,0,1],[1,0,0,1,0]+[0]*6+[0,1,0,0,1],[1,0,0,1,0]+[0]*6+[0,1,0,0,1],[1,0,0,1,0]+[0]*6+[0,1,0,0,1],[1,0,0,1,0]+[0]*6+[0,1,0,0,1],[1,0,0,1,0]+[0]*6+[0,1,0,0,1],[1,0,0,1,1]+[1]*6+[1,1,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1]*16]
FILLED_ELLI_ICON = [[1]*16,[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,1,1,1,1,1,1,0,0,0,0,1],[1,0,0,0,1,1,1,1,1,1,1,1,0,0,0,1],[1,0,0,1,1,1,1,1,1,1,1,1,1,0,0,1],[1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1],[1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1],[1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1],[1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1],[1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1],[1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1],[1,0,0,1,1,1,1,1,1,1,1,1,1,0,0,1],[1,0,0,0,1,1,1,1,1,1,1,1,0,0,0,1],[1,0,0,0,0,1,1,1,1,1,1,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1]*16]
ELLI_ICON = [[1]*16,[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,1,1,1,1,1,1,0,0,0,0,1],[1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1],[1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1],[1,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1],[1,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1],[1,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1],[1,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1],[1,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1],[1,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1],[1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1],[1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1],[1,0,0,0,0,1,1,1,1,1,1,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1]*16]
BUCKET_ICON = [[1]*16,[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1],[1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1],[1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1],[1,0,0,1,0,1,1,1,0,0,0,0,0,0,0,1],[1,0,0,1,1,0,1,0,1,1,0,0,0,0,0,1],[1,0,0,1,0,0,1,0,0,1,1,1,0,0,0,1],[1,0,1,1,0,0,1,0,0,0,1,1,1,0,0,1],[1,0,1,1,1,0,0,0,0,0,0,1,1,0,0,1],[1,0,0,1,1,1,0,0,0,0,1,1,1,0,0,1],[1,0,0,0,1,1,1,1,1,1,0,1,1,0,0,1],[1,0,0,0,0,1,1,1,1,0,0,1,0,0,0,1],[1,0,0,0,0,0,1,1,0,0,0,1,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1]*16]
SWAP_ICON = [[1]*16,[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,1],[1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1],[1,0,0,0,1,0,0,0,0,0,1,1,1,0,0,1],[1,0,1,0,1,0,1,0,0,1,1,1,1,1,0,1],[1,0,1,1,1,1,1,0,0,1,0,1,0,1,0,1],[1,0,0,1,1,1,0,0,0,0,0,1,0,0,0,1],[1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1],[1,0,0,0,0,1,1,1,1,1,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1]*16]

SELECT_TOOL = 0
PEN_TOOL = 1
MIRROR_TOOL = 2
LINE_TOOL = 3
FILLED_RECT_TOOL = 4
RECT_TOOL = 5
FILLED_ELLI_TOOL = 6
ELLI_TOOL = 7
BUCKET_TOOL = 8
SWAP_TOOL = 9

TOOLS_SHORTCUTS = {
    pyxel.KEY_S:SELECT_TOOL,
    pyxel.KEY_P:PEN_TOOL,
    pyxel.KEY_M:MIRROR_TOOL,
    pyxel.KEY_L:LINE_TOOL,
    pyxel.KEY_R:FILLED_RECT_TOOL,
    pyxel.KEY_E:FILLED_ELLI_TOOL,
    pyxel.KEY_B:BUCKET_TOOL,
    pyxel.KEY_O:SWAP_TOOL,
}

#? ---------- SPRITE CONSTANTS ---------- ?#

EDITOR_X, EDITOR_Y, EDITOR_SIZE = 25, 16, 128
COLOR_PICKER_X, COLOR_PICKER_Y = EDITOR_X + EDITOR_SIZE + 16, EDITOR_Y + 58
SPRITE_ZOOMS = [8, 16, 32, 64, 128]

#? ---------- TILEMAP CONSTANTS ---------- ?#

TILEMAP_TILE_SIZE = 8
TILES_PICKER_X, TILES_PICKER_Y, TILES_PICKER_SIZE = EDITOR_X + EDITOR_SIZE + 16, EDITOR_Y + EDITOR_SIZE - 64, 64
TILEMAP_ZOOMS = [16, 32, 64]

#? ---------- UTILITY CLASSES ---------- ?#

class ColorButton:
    
    def __init__(self, x:int, y:int, color_id:int, colors_len:int):
        self.x, self.y = x, y
        self.w, self.h = 8, 8
        self.color_id = color_id
        self.colors_len = colors_len
        self.selected = False

    def update(self, current_color:int):
        if self.x <= pyxel.mouse_x < self.x + self.w and self.y <= pyxel.mouse_y < self.y + self.h and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            return self.color_id
        self.selected = current_color == self.color_id
        return None
    
    def draw(self):
        pyxel.rect(self.x, self.y, self.w, self.h, self.color_id)
        if self.selected:
            pyxel.rectb(self.x, self.y, self.w, self.h, self.colors_len + 1)

class IconButton:

    def __init__(self, x:int, y:int, id:int, icon:list, colors_len:int):
        self.x, self.y = x, y
        self.w, self.h = len(icon[0]), len(icon)
        self.id = id
        self.icon = icon
        self.colors_len = colors_len
        self.selected = False

    def update(self, current_id:int=0):
        if collision_point_rect(pyxel.mouse_x, pyxel.mouse_y, self.x, self.y, self.w, self.h) and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            return self.id
        
        self.selected = current_id == self.id
        return None

    def draw(self):
        for y in range(len(self.icon)):
            for x in range(len(self.icon[y])):
                c = self.icon[y][x]
                if c:
                    c = self.colors_len + 1 if self.selected else self.colors_len + 2
                    pyxel.rect(self.x + x, self.y + y, 1, 1, c)

class Selector:

    def __init__(self, x:int, y:int, label:str, values:list, colors_len:int, start_index:int=0):
        self.x, self.y = x, y
        self.label = label
        self.values = values
        self.colors_len = colors_len
        self.__index = start_index

        self.btn_w = 8
        self.btn_h = 8

    @property
    def index(self):
        return self.__index

    @index.setter
    def index(self, new_index:int):
        if new_index >= 0 and new_index < len(self.values):
            self.__index = new_index

    @property
    def value(self):
        return self.values[self.__index]
    
    @value.setter
    def value(self, new_value:int):
        self.__index = self.values.index(new_value)

    def update(self):
        mx, my = pyxel.mouse_x, pyxel.mouse_y
        label_w = len(self.label) * 4
        value_str = str(self.value)
        value_w = len(value_str) * 4
        minus_x = self.x + label_w
        plus_x = minus_x + self.btn_w + value_w + 4

        if (minus_x <= mx < minus_x + self.btn_w and self.y <= my < self.y + self.btn_h and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)):
            if pyxel.btn(pyxel.KEY_LSHIFT):
                self.__index = max(0, self.__index - 10)
            else:
                self.__index = max(0, self.__index - 1)
            return True

        if (plus_x <= mx < plus_x + self.btn_w and self.y <= my < self.y + self.btn_h and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)):
            if pyxel.btn(pyxel.KEY_LSHIFT):
                self.__index = min(len(self.values) - 1, self.__index + 10)
            else:
                self.__index = min(len(self.values) - 1, self.__index + 1)
            return True
            
        return False

    def draw(self):
        label_w = len(self.label) * 4
        value_str = str(self.value)
        value_w = len(value_str) * 4

        minus_x = self.x + label_w
        value_x = minus_x + self.btn_w + 2
        plus_x = value_x + value_w + 2

        pyxel.text(self.x, self.y + 2, self.label, self.colors_len + 1)

        pyxel.rect(minus_x, self.y, self.btn_w, self.btn_h, self.colors_len + 2)
        pyxel.text(minus_x + 2, self.y + 2, "-", self.colors_len + 1)

        pyxel.text(value_x, self.y + 2, value_str, self.colors_len + 1)

        pyxel.rect(plus_x, self.y, self.btn_w, self.btn_h, self.colors_len + 2)
        pyxel.text(plus_x + 2, self.y + 2, "+", self.colors_len + 1)

class Button:

    def __init__(self, x:int, y:int, id:int, colors_len:int):
        self.x, self.y = x, y
        self.w, self.h = 8, 8
        self.id = id
        self.colors_len = colors_len
        self.selected = False

    def update(self):
        if self.x <= pyxel.mouse_x < self.x + self.w and self.y <= pyxel.mouse_y < self.y + self.h and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.selected = not self.selected
    
    def draw(self):
        x = 0 if not self.selected else 2
        pyxel.rect(self.x, self.y, self.w, self.h, self.colors_len + x)
        pyxel.text(self.x + 1, self.y + 2, str(self.id), self.colors_len + 1)

#? ---------- UTILITY FUNCTIONS ---------- ?#

def collision_point_rect(x1:int, y1:int, x2:int, y2:int, w2:int, h2:int)-> bool:
    return x2 <= x1 < x2 + w2 and y2 <= y1 < y2 + h2

#? ---------- EDITOR ---------- ?#

class Editor:

    def __init__(self, pyxres_path:str, palette:list, fullscreen:bool=True):
        #? Pyxel Init
        pyxel.init(258, 160, title="Editor", fps=60, quit_key=pyxel.KEY_NONE)
        pyxel.fullscreen(fullscreen)
        pyxel.colors.clear()
        pyxel.colors.extend(palette + [0x2B335F, 0xEEEEEE, 0x4A90E2])

        #? Pyxres Config
        self.load(pyxres_path)

        #? CONSTANTS
        self.COLORS_LEN = len(palette)

        if self.COLORS_LEN > 40:    raise NotImplementedError("Can not have more than 40 colors")

        #? Main Variables
        self.current_tab = SPRITE_EDITOR
        self.current_tool = SELECT_TOOL
        self.tab_buttons = [IconButton(0, 16, SPRITE_EDITOR, SPRITE_ICON, self.COLORS_LEN),
                            IconButton(0, 32, TILEMAP_EDITOR, TILEMAP_ICON, self.COLORS_LEN),
                            IconButton(0, 48, AUTOTILE_EDITOR, AUTOTILE_ICON, self.COLORS_LEN),]
        self.tool_buttons = [IconButton(169, 16, SELECT_TOOL, SELECT_ICON, self.COLORS_LEN),
                             IconButton(185, 16, PEN_TOOL, PEN_ICON, self.COLORS_LEN),
                             IconButton(201, 16, MIRROR_TOOL, MIRROR_ICON, self.COLORS_LEN),
                             IconButton(217, 16, LINE_TOOL, LINE_ICON, self.COLORS_LEN),
                             IconButton(169, 32, FILLED_RECT_TOOL, FILLED_RECT_ICON, self.COLORS_LEN),
                             IconButton(185, 32, RECT_TOOL, RECT_ICON, self.COLORS_LEN),
                             IconButton(201, 32, FILLED_ELLI_TOOL, FILLED_ELLI_ICON, self.COLORS_LEN),
                             IconButton(217, 32, ELLI_TOOL, ELLI_ICON, self.COLORS_LEN),
                             IconButton(169, 48, BUCKET_TOOL, BUCKET_ICON, self.COLORS_LEN),
                             IconButton(185, 48, SWAP_TOOL, SWAP_ICON, self.COLORS_LEN)]

        #? Sprite Variables
        self.s_color = 0
        self.s_grid = False
        self.s_history = []
        self.s_selection = None
        self.s_clipboard = None
        self.s_drag_start = None
        self.s_tile_size = EDITOR_SIZE // 16
        self.s_offset_x = self.s_offset_y = 0
        self.s_color_buttons = self.place_s_color_buttons()
        self.s_zoom_selector = Selector(101, 148, "Zoom:", SPRITE_ZOOMS[::-1], self.COLORS_LEN, 3)
        self.s_grid_selector = Selector(89, 4, "Grid size:", [1, 2, 4, 8, 16], self.COLORS_LEN, 3)
        self.s_image_selector = Selector(25, 148, "Image:", [x for x in range(self.NUMBER_IMAGES)], self.COLORS_LEN)

        #? Tilemap Variables
        self.t_grid = False
        self.t_history = []
        self.t_clipboard = None
        self.t_selection = None
        self.t_drag_start = None
        self.t_tile_selected = (0, 0)
        self.t_tile_offset_x = self.t_tile_offset_y = 0
        self.t_tilemap_offset_x = self.t_tilemap_offset_y = 0
        self.t_grid_selector = Selector(89, 4, "Grid size:", [1, 2, 4, 8], self.COLORS_LEN, 3)
        self.t_zoom_selector = Selector(169, 4, "Zoom:", TILEMAP_ZOOMS[::-1], self.COLORS_LEN, 2)
        self.t_tilemap_selector = Selector(25, 148, "Tilemap:", [x for x in range(self.NUMBER_TILEMAPS)], self.COLORS_LEN)
        self.t_layer_selector = Selector(93, 148, "Layer:", ["None"] + [x for x in range(self.NUMBER_TILEMAPS)], self.COLORS_LEN)
        self.t_image_selector = Selector(169, 148, "Image:", [x for x in range(self.NUMBER_IMAGES)], self.COLORS_LEN, pyxel.tilemaps[0].imgsrc)

        #? Autotile Editor Variables
        self.a_tiles_y = {x:[] for x in range(self.NUMBER_IMAGES)}
        self.a_buttons = {x:self.place_a_buttons() for x in range(self.NUMBER_IMAGES)}
        self.a_image_selector = Selector(20, 2, "Image:", [x for x in range(self.NUMBER_IMAGES)], self.COLORS_LEN)

        #? Pyxel Run
        pyxel.run(self.update, self.draw)

    #? ---------- PYXRES ---------- ?#

    def load(self, pyxres_path:str):
        if os.path.isfile(pyxres_path):
            pyxel.load(pyxres_path)
        else:
            pyxel.images.clear()
            pyxel.images.extend([pyxel.Image(256, 256) for _ in range(2)])
            pyxel.tilemaps.clear()
            pyxel.tilemaps.extend([pyxel.Tilemap(256, 256, 0) for _ in range(4)])
            pyxel.sounds.clear()
            pyxel.sounds.extend([pyxel.Sound() for _ in range(64)])
            for i in range(64):
                pyxel.sounds[i].set_tones("T")
                pyxel.sounds[i].set_volumes("7")
                pyxel.sounds[i].set_effects("N")
                pyxel.sounds[i].speed = 1

        self.PYXRES_PATH = pyxres_path
        self.NUMBER_IMAGES = len(pyxel.images)
        self.NUMBER_TILEMAPS = len(pyxel.tilemaps)
        self.NUMBER_SOUNDS = len(pyxel.sounds)

    def save(self):
        pyxel.save(self.PYXRES_PATH)

    #? ---------- DRAW METHODS ---------- ?#

    def rect(self, min_x:int, min_y:int, max_x:int, max_y:int, filled:bool=True):
        rect = set()
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                if filled or (y in [min_y, max_y] or x in [min_x, max_x]):
                    rect.add((x, y))
        return rect

    def elli(self, min_x:int, min_y:int, max_x:int, max_y:int, filled:bool=True):
        elli = set()
        width = max_x - min_x
        height = max_y - min_y
        if width == 0 or height == 0:
            return self.rect(min_x, min_y, max_x, max_y, not filled)

        rx = width / 2.0
        ry = height / 2.0
        cx = (min_x + max_x) / 2.0
        cy = (min_y + max_y) / 2.0

        for yy in range(min_y, max_y + 1):
            for xx in range(min_x, max_x + 1):
                dx = xx - cx
                dy = yy - cy
                val = (dx*dx) / (rx*rx + 1e-9) + (dy*dy) / (ry*ry + 1e-9)
                if filled:
                    if val <= 1.0 + 1e-9:
                        elli.add((xx, yy))
                else:
                    if val <= 1.0 + 1e-9:
                        outside_neighbor = False
                        for nx, ny in ((xx+1,yy),(xx-1,yy),(xx,yy+1),(xx,yy-1)):
                            if nx < min_x or nx > max_x or ny < min_y or ny > max_y:
                                outside_neighbor = True
                                break
                            ndx = nx - cx
                            ndy = ny - cy
                            nval = (ndx*ndx) / (rx*rx + 1e-9) + (ndy*ndy) / (ry*ry + 1e-9)
                            if nval > 1.0 + 1e-9:
                                outside_neighbor = True
                                break
                        if outside_neighbor:
                            elli.add((xx, yy))
        return elli

    def line(self, x0:int, y0:int, x1:int, y1:int):
        line = set()
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy

        while True:
            line.add((x0, y0))
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

        return line

    #? ---------- SPRITE EDITOR ---------- ?#

    def place_s_color_buttons(self):
        l = []
        c = x = y = 0
        while c < self.COLORS_LEN:
            l.append(ColorButton(COLOR_PICKER_X + x * 8, COLOR_PICKER_Y + y * 8, c, self.COLORS_LEN))
            x = (x + 1) % 8
            if x == 0:
                y += 1
            c += 1
        return l

    def push_sprite_history(self):
        snapshot = [[pyxel.images[self.s_image_selector.value].pget(x, y) for x in range(pyxel.images[self.s_image_selector.value].width)] for y in range(pyxel.images[self.s_image_selector.value].height)]
        self.s_history.append((self.s_image_selector.value, snapshot))
        if len(self.s_history) > 40:
            self.s_history.pop(0)

    def undo_sprite(self):
        if self.s_history:
            image, snapshot = self.s_history.pop()
            for y in range(pyxel.images[self.s_image_selector.value].height):
                for x in range(pyxel.images[self.s_image_selector.value].width):
                    pyxel.images[image].pset(x, y, snapshot[y][x])

    def flood_fill_sprite(self, x:int, y:int, old_color:int, new_color:int):
        if old_color == new_color:
            return set()

        pixels = set()
        x0, y0 = self.s_offset_x, self.s_offset_y
        x1, y1 = self.s_offset_x + self.s_zoom_selector.value, self.s_offset_y + self.s_zoom_selector.value

        stack = [(x, y)]
        while stack:
            cx, cy = stack.pop()
            if (x0 <= cx < x1 and y0 <= cy < y1 and pyxel.images[self.s_image_selector.value].pget(cx, cy) == old_color) and (cx, cy) not in pixels:
                pixels.add((cx, cy))
                stack.extend([(cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)])
        return pixels

    def swap_fill_sprite(self, old_color:int, new_color:int):
        if old_color == new_color:
            return set()
    
        pixels = set()
        x0, y0 = self.s_offset_x, self.s_offset_y
        x1, y1 = self.s_offset_x + self.s_zoom_selector.value, self.s_offset_y + self.s_zoom_selector.value

        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if pyxel.images[self.s_image_selector.value].pget(x, y) == old_color:
                    pixels.add((x, y))
        return pixels

    def commit_pixels(self, pixels:set):
        x0, y0 = self.s_offset_x, self.s_offset_y
        x1, y1 = self.s_offset_x + self.s_zoom_selector.value - 1, self.s_offset_y + self.s_zoom_selector.value - 1
        for (x, y) in pixels:
            if x0 <= x <= x1 and y0 <= y <= y1:
                pyxel.images[self.s_image_selector.value].pset(x, y, self.s_color)

    def draw_preview_pixels(self, pixels:set):
        for (x, y) in pixels:
            if x < self.s_offset_x or x >= self.s_offset_x + self.s_zoom_selector.value or y < self.s_offset_y or y >= self.s_offset_y + self.s_zoom_selector.value:
                continue
            sx = EDITOR_X + (x - self.s_offset_x) * self.s_tile_size
            sy = EDITOR_Y + (y - self.s_offset_y) * self.s_tile_size
            pyxel.rect(sx, sy, self.s_tile_size, self.s_tile_size, self.s_color)

    def copy_sprite(self):
        if not self.s_selection or self.current_tool != SELECT_TOOL:
            return
        
        x0, y0, x1, y1 = self.s_selection
        min_x, min_y = min(x0, x1), min(y0, y1)
        max_x, max_y = max(x0, x1), max(y0, y1)
        
        self.s_clipboard = []
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                abs_x = x + self.s_offset_x
                abs_y = y + self.s_offset_y
                color = pyxel.images[self.s_image_selector.value].pget(abs_x, abs_y)
                self.s_clipboard.append((x - min_x, y - min_y, color))

    def cut_sprite(self):
        if not self.s_selection or self.current_tool != SELECT_TOOL:
            return
        
        self.copy_sprite()
        
        x0, y0, x1, y1 = self.s_selection
        min_x, min_y = min(x0, x1), min(y0, y1)
        max_x, max_y = max(x0, x1), max(y0, y1)
        
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                abs_x = x + self.s_offset_x
                abs_y = y + self.s_offset_y
                pyxel.images[self.s_image_selector.value].pset(abs_x, abs_y, 0)

    def paste_sprite(self):
        if not self.s_clipboard or not self.s_selection or self.current_tool != SELECT_TOOL:
            return
        
        x0, y0, x1, y1 = self.s_selection
        min_x, min_y = min(x0, x1), min(y0, y1)
        
        for rel_x, rel_y, color in self.s_clipboard:
            abs_x = min_x + rel_x + self.s_offset_x
            abs_y = min_y + rel_y + self.s_offset_y
            
            if 0 <= abs_x < pyxel.images[self.s_image_selector.value].width and 0 <= abs_y < pyxel.images[self.s_image_selector.value].height:
                pyxel.images[self.s_image_selector.value].pset(abs_x, abs_y, color)

    def rotate_sprite_selection(self):
        if not self.s_selection or self.current_tool != SELECT_TOOL:
            return
        
        x0, y0, x1, y1 = self.s_selection
        min_x, min_y = min(x0, x1), min(y0, y1)
        max_x, max_y = max(x0, x1), max(y0, y1)
        
        width = max_x - min_x + 1
        height = max_y - min_y + 1

        if width != height:
            return
        
        temp_buffer = []
        for y in range(min_y, max_y + 1):
            row = []
            for x in range(min_x, max_x + 1):
                abs_x = x + self.s_offset_x
                abs_y = y + self.s_offset_y
                row.append(pyxel.images[self.s_image_selector.value].pget(abs_x, abs_y))
            temp_buffer.append(row)
        
        for y in range(height):
            for x in range(width):
                new_x = min_x + y
                new_y = min_y + (width - 1 - x)
                
                if new_x <= max_x and new_y <= max_y:
                    abs_x = new_x + self.s_offset_x
                    abs_y = new_y + self.s_offset_y
                    if 0 <= abs_x < pyxel.images[self.s_image_selector.value].width and 0 <= abs_y < pyxel.images[self.s_image_selector.value].height:
                        pyxel.images[self.s_image_selector.value].pset(abs_x, abs_y, temp_buffer[y][x])

    def flip_sprite_selection_horizontal(self):
        if not self.s_selection or self.current_tool != SELECT_TOOL:
            return
        
        x0, y0, x1, y1 = self.s_selection
        min_x, min_y = min(x0, x1), min(y0, y1)
        max_x, max_y = max(x0, x1), max(y0, y1)
        
        width = max_x - min_x + 1
        
        temp_buffer = []
        for y in range(min_y, max_y + 1):
            row = []
            for x in range(min_x, max_x + 1):
                abs_x = x + self.s_offset_x
                abs_y = y + self.s_offset_y
                row.append(pyxel.images[self.s_image_selector.value].pget(abs_x, abs_y))
            temp_buffer.append(row)

        for y in range(max_y - min_y + 1):
            for x in range(width):
                new_x = min_x + (width - 1 - x)
                abs_x = new_x + self.s_offset_x
                abs_y = (min_y + y) + self.s_offset_y
                if 0 <= abs_x < pyxel.images[self.s_image_selector.value].width and 0 <= abs_y < pyxel.images[self.s_image_selector.value].height:
                    pyxel.images[self.s_image_selector.value].pset(abs_x, abs_y, temp_buffer[y][x])

    def flip_sprite_selection_vertical(self):
        if not self.s_selection or self.current_tool != SELECT_TOOL:
            return
        
        x0, y0, x1, y1 = self.s_selection
        min_x, min_y = min(x0, x1), min(y0, y1)
        max_x, max_y = max(x0, x1), max(y0, y1)
        
        height = max_y - min_y + 1
        
        temp_buffer = []
        for y in range(min_y, max_y + 1):
            row = []
            for x in range(min_x, max_x + 1):
                abs_x = x + self.s_offset_x
                abs_y = y + self.s_offset_y
                row.append(pyxel.images[self.s_image_selector.value].pget(abs_x, abs_y))
            temp_buffer.append(row)
        
        for y in range(height):
            for x in range(max_x - min_x + 1):
                new_y = min_y + (height - 1 - y)
                abs_x = (min_x + x) + self.s_offset_x
                abs_y = new_y + self.s_offset_y
                if 0 <= abs_x < pyxel.images[self.s_image_selector.value].width and 0 <= abs_y < pyxel.images[self.s_image_selector.value].height:
                    pyxel.images[self.s_image_selector.value].pset(abs_x, abs_y, temp_buffer[y][x])

    def update_sprite_editor(self):
        #? Grid
        if pyxel.btnp(pyxel.KEY_G): self.s_grid = not self.s_grid

        #? Scroll Wheel
        if pyxel.mouse_wheel < 0:
            self.s_selection = None
            self.s_zoom_selector.index += 1
            self.s_tile_size = EDITOR_SIZE // self.s_zoom_selector.value
        elif pyxel.mouse_wheel > 0:
            self.s_selection = None
            self.s_zoom_selector.index -= 1
            self.s_tile_size = EDITOR_SIZE // self.s_zoom_selector.value

        #? Selection Shortcuts
        if pyxel.btn(pyxel.KEY_CTRL) or pyxel.btn(pyxel.KEY_GUI):
            if pyxel.btnp(pyxel.KEY_R):
                self.push_sprite_history()
                self.rotate_sprite_selection()
            elif pyxel.btnp(pyxel.KEY_H):
                self.push_sprite_history()
                self.flip_sprite_selection_horizontal()
            elif pyxel.btnp(pyxel.KEY_F):
                self.push_sprite_history()
                self.flip_sprite_selection_vertical()
            elif pyxel.btnp(pyxel.KEY_C):
                self.copy_sprite()
            elif pyxel.btnp(pyxel.KEY_X):
                self.push_sprite_history()
                self.cut_sprite()
            elif pyxel.btnp(pyxel.KEY_V):
                self.push_sprite_history()
                self.paste_sprite()
            elif pyxel.btnp(pyxel.KEY_Z):
                self.undo_sprite()

        #? Tools Shortcut
        for key in TOOLS_SHORTCUTS.keys():
            if pyxel.btnp(key) and not (pyxel.btn(pyxel.KEY_CTRL) or pyxel.btn(pyxel.KEY_GUI)):
                self.current_tool = TOOLS_SHORTCUTS[key]

        #? Editor
        if collision_point_rect(pyxel.mouse_x, pyxel.mouse_y, EDITOR_X, EDITOR_Y, EDITOR_SIZE, EDITOR_SIZE):
            mx = (pyxel.mouse_x - EDITOR_X) // self.s_tile_size + self.s_offset_x
            my = (pyxel.mouse_y - EDITOR_Y) // self.s_tile_size + self.s_offset_y

            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):

                if self.current_tool in [FILLED_RECT_TOOL, RECT_TOOL, FILLED_ELLI_TOOL, ELLI_TOOL, LINE_TOOL]:
                    self.s_drag_start = (mx, my)
                elif self.current_tool == BUCKET_TOOL:
                    self.push_sprite_history()
                    self.commit_pixels(self.flood_fill_sprite(mx, my, pyxel.images[self.s_image_selector.value].pget(mx, my), self.s_color))
                elif self.current_tool == SWAP_TOOL:
                    self.push_sprite_history()
                    self.commit_pixels(self.swap_fill_sprite(pyxel.images[self.s_image_selector.value].pget(mx, my), self.s_color))
                elif self.current_tool == SELECT_TOOL:
                    x = (pyxel.mouse_x - EDITOR_X) // self.s_tile_size
                    y = (pyxel.mouse_y - EDITOR_Y) // self.s_tile_size
                    self.s_selection = [x, y, x, y]

            if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
                if self.current_tool == PEN_TOOL:
                    pyxel.images[self.s_image_selector.value].pset(mx, my, self.s_color)
                elif self.current_tool == MIRROR_TOOL:
                    pyxel.images[self.s_image_selector.value].pset(mx, my, self.s_color)
                    axis_x = self.s_offset_x + self.s_zoom_selector.value // 2
                    mx_mirror = axis_x - (mx - axis_x) - 1
                    if 0 <= mx_mirror < pyxel.images[self.s_image_selector.value].width:
                        pyxel.images[self.s_image_selector.value].pset(mx_mirror, my, self.s_color)
                elif self.current_tool == SELECT_TOOL and self.s_selection:
                    x = (pyxel.mouse_x - EDITOR_X) // self.s_tile_size
                    y = (pyxel.mouse_y - EDITOR_Y) // self.s_tile_size
                    self.s_selection[2] = x
                    self.s_selection[3] = y

            if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) and self.s_drag_start:
                x0, y0 = self.s_drag_start
                max_x, max_y = max(x0, mx), max(y0, my)
                min_x, min_y = min(x0, mx), min(y0, my)

                self.push_sprite_history()

                if self.current_tool == FILLED_RECT_TOOL:
                    self.commit_pixels(self.rect(min_x, min_y, max_x, max_y))
                elif self.current_tool == RECT_TOOL:
                    self.commit_pixels(self.rect(min_x, min_y, max_x, max_y, False))
                elif self.current_tool == FILLED_ELLI_TOOL:
                    self.commit_pixels(self.elli(min_x, min_y, max_x, max_y))
                elif self.current_tool == ELLI_TOOL:
                    self.commit_pixels(self.elli(min_x, min_y, max_x, max_y, False))
                elif self.current_tool == LINE_TOOL:
                    self.commit_pixels(self.line(x0, y0, mx, my))

                self.s_drag_start = None

            if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
                self.s_color = pyxel.images[self.s_image_selector.value].pget(mx, my)

        else:
            self.s_drag_start = None

        #? Movement
        if pyxel.btnp(pyxel.KEY_RIGHT, repeat=5):
            self.s_offset_x += self.s_zoom_selector.value // 2
        if pyxel.btnp(pyxel.KEY_LEFT, repeat=5):
            self.s_offset_x -= self.s_zoom_selector.value // 2
        if pyxel.btnp(pyxel.KEY_DOWN, repeat=5):
            self.s_offset_y += self.s_zoom_selector.value // 2
        if pyxel.btnp(pyxel.KEY_UP, repeat=5):
            self.s_offset_y -= self.s_zoom_selector.value // 2
        self.s_offset_x = max(0, min(pyxel.images[self.s_image_selector.value].width - self.s_zoom_selector.value, self.s_offset_x))
        self.s_offset_y = max(0, min(pyxel.images[self.s_image_selector.value].height - self.s_zoom_selector.value, self.s_offset_y))

        #? Selectors
        self.s_image_selector.update()
        self.s_grid_selector.update()
        z = self.s_zoom_selector.update()

        if z:
            self.s_selection = None
            self.s_tile_size = EDITOR_SIZE // self.s_zoom_selector.value

        #? Color Buttons
        for color_button in self.s_color_buttons:
            c = color_button.update(self.s_color)
            self.s_color = c if c is not None else self.s_color

        #? Tool Buttons
        for tool_button in self.tool_buttons:
            c = tool_button.update(self.current_tool)
            self.current_tool = c if c is not None else self.current_tool

    def draw_sprite_editor(self):
        #? Selectors
        self.s_image_selector.draw()
        self.s_zoom_selector.draw()
        self.s_grid_selector.draw()

        #? Color Buttons
        for color_button in self.s_color_buttons:
            color_button.draw()

        #? Tool Buttons
        for tool_button in self.tool_buttons:
            tool_button.draw()

        #? Color Number
        tx = (pyxel.mouse_x - COLOR_PICKER_X) // 8
        ty = (pyxel.mouse_y - COLOR_PICKER_Y) // 8
        if collision_point_rect(pyxel.mouse_x, pyxel.mouse_y, COLOR_PICKER_X, COLOR_PICKER_Y, 64, 32) and tx + ty * 8 < self.COLORS_LEN:
            pyxel.text(COLOR_PICKER_X, COLOR_PICKER_Y - 8, f"{tx + ty * 8}", self.COLORS_LEN + 1)
        else:
            pyxel.text(COLOR_PICKER_X, COLOR_PICKER_Y - 8, f"{self.s_color}", self.COLORS_LEN + 1)

        #? Keybinds
        pyxel.text(COLOR_PICKER_X, EDITOR_Y + EDITOR_SIZE - 18, "G : toggle grid\nR : rotate\nH : flip horizontal\nF : flip vertical\nC / X / V / Z", self.COLORS_LEN + 1)

        #? Editor
        for y in range(self.s_zoom_selector.value):
            for x in range(self.s_zoom_selector.value):
                c = pyxel.images[self.s_image_selector.value].pget(self.s_offset_x + x, self.s_offset_y + y)
                pyxel.rect(EDITOR_X + x * self.s_tile_size, EDITOR_Y + y * self.s_tile_size, self.s_tile_size, self.s_tile_size, c)
            
        #? Draw Preview
        if collision_point_rect(pyxel.mouse_x, pyxel.mouse_y, EDITOR_X, EDITOR_Y, EDITOR_SIZE, EDITOR_SIZE):
            mx = (pyxel.mouse_x - EDITOR_X) // self.s_tile_size + self.s_offset_x
            my = (pyxel.mouse_y - EDITOR_Y) // self.s_tile_size + self.s_offset_y
            pixels = set()

            pyxel.text(EDITOR_X + 1, 8, f"({mx},{my})", self.COLORS_LEN + 1)

            if self.current_tool == BUCKET_TOOL:
                pixels = self.flood_fill_sprite(mx, my, pyxel.images[self.s_image_selector.value].pget(mx, my), self.s_color)
            elif self.current_tool == SWAP_TOOL:
                pixels = self.swap_fill_sprite(pyxel.images[self.s_image_selector.value].pget(mx, my), self.s_color)

            if self.s_drag_start:
                x0, y0 = self.s_drag_start
                min_x, max_x = min(x0, mx), max(x0, mx)
                min_y, max_y = min(y0, my), max(y0, my)

                if self.current_tool == FILLED_RECT_TOOL:
                    pixels = self.rect(min_x, min_y, max_x, max_y)
                elif self.current_tool == RECT_TOOL:
                    pixels = self.rect(min_x, min_y, max_x, max_y, False)
                elif self.current_tool == FILLED_ELLI_TOOL:
                    pixels = self.elli(min_x, min_y, max_x, max_y)
                elif self.current_tool == ELLI_TOOL:
                    pixels = self.elli(min_x, min_y, max_x, max_y, False)
                elif self.current_tool == LINE_TOOL:
                    pixels = self.line(x0, y0, mx, my)

            self.draw_preview_pixels(pixels)

        #? Grid
        if self.s_grid:
            for y in range(EDITOR_Y, EDITOR_Y + EDITOR_SIZE, self.s_grid_selector.value * self.s_tile_size):
                pyxel.rect(EDITOR_X, y, EDITOR_SIZE, 1, self.COLORS_LEN)
            for x in range(EDITOR_X, EDITOR_X + EDITOR_SIZE, self.s_grid_selector.value * self.s_tile_size):
                pyxel.rect(x, EDITOR_Y, 1, EDITOR_SIZE, self.COLORS_LEN)
            pyxel.rect(EDITOR_X, EDITOR_Y + EDITOR_SIZE - 1, EDITOR_SIZE, 1, self.COLORS_LEN)
            pyxel.rect(EDITOR_X + EDITOR_SIZE - 1, EDITOR_Y, 1, EDITOR_SIZE, self.COLORS_LEN)

        #? Selection Preview
        if self.s_selection and self.current_tool == SELECT_TOOL:
            x0, y0, x1, y1 = self.s_selection
            min_x, max_x = min(x0, x1), max(x0, x1)
            min_y, max_y = min(y0, y1), max(y0, y1)

            pyxel.rectb(EDITOR_X + min_x * self.s_tile_size, EDITOR_Y + min_y * self.s_tile_size, (max_x - min_x + 1) * self.s_tile_size, (max_y - min_y + 1) * self.s_tile_size, self.COLORS_LEN + 1)

    #? ---------- TILEMAP EDITOR ---------- ?#

    def push_tilemap_history(self):
        snapshot = [[pyxel.tilemaps[self.t_tilemap_selector.value].pget(x, y) for x in range(pyxel.tilemaps[self.t_tilemap_selector.value].width)] for y in range(pyxel.tilemaps[self.t_tilemap_selector.value].height)]
        self.t_history.append((self.t_tilemap_selector.value, snapshot))
        if len(self.t_history) > 40:
            self.t_history.pop(0)

    def undo_tilemap(self):
        if self.t_history:
            tilemap, snapshot = self.t_history.pop()
            for y in range(pyxel.tilemaps[self.t_tilemap_selector.value].height):
                for x in range(pyxel.tilemaps[self.t_tilemap_selector.value].width):
                    pyxel.tilemaps[tilemap].pset(x, y, snapshot[y][x])

    def flood_fill_tilemap(self, x:int, y:int, old_tile:tuple, new_tile:tuple):
        if old_tile == new_tile:
            return set()

        pixels = set()
        x0, y0 = self.t_tilemap_offset_x, self.t_tilemap_offset_y
        x1, y1 = self.t_tilemap_offset_x + self.t_zoom_selector.value, self.t_tilemap_offset_y + self.t_zoom_selector.value

        stack = [(x, y)]
        while stack:
            cx, cy = stack.pop()
            if (x0 <= cx < x1 and y0 <= cy < y1 and pyxel.tilemaps[self.t_tilemap_selector.value].pget(cx, cy) == old_tile) and (cx, cy) not in pixels:
                pixels.add((cx, cy))
                stack.extend([(cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)])
        return pixels

    def swap_fill_tilemap(self, old_tile:tuple, new_tile:tuple):
        if old_tile == new_tile:
            return set()
    
        pixels = set()
        x0, y0 = self.t_tilemap_offset_x, self.t_tilemap_offset_y
        x1, y1 = self.t_tilemap_offset_x + self.t_zoom_selector.value, self.t_tilemap_offset_y + self.t_zoom_selector.value

        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if pyxel.tilemaps[self.t_tilemap_selector.value].pget(x, y) == old_tile:
                    pixels.add((x, y))
        return pixels

    def commit_tiles(self, tiles:set):
        x0, y0 = self.t_tilemap_offset_x, self.t_tilemap_offset_y
        x1, y1 = self.t_tilemap_offset_x + self.t_zoom_selector.value - 1, self.t_tilemap_offset_y + self.t_zoom_selector.value - 1
        tx, ty = (self.t_tile_selected[0] + self.t_tile_offset_x // 8, self.t_tile_selected[1] + self.t_tile_offset_y // 8)
        for (x, y) in tiles:
            if x0 <= x <= x1 and y0 <= y <= y1:
                pyxel.tilemaps[self.t_tilemap_selector.value].pset(x, y, (tx, ty))

    def draw_preview_tiles(self, tiles:set):
        factor = self.t_zoom_selector.value // 16
        tx, ty = (self.t_tile_selected[0] + self.t_tile_offset_x // 8, self.t_tile_selected[1] + self.t_tile_offset_y // 8)
        for (x, y) in tiles:
            if x < self.t_tilemap_offset_x or x >= self.t_tilemap_offset_x + self.t_zoom_selector.value or y < self.t_tilemap_offset_y or y >= self.t_tilemap_offset_y + self.t_zoom_selector.value:
                continue
            sx = EDITOR_X + (x - self.t_tilemap_offset_x) * (TILEMAP_TILE_SIZE // factor)
            sy = EDITOR_Y + (y - self.t_tilemap_offset_y) * (TILEMAP_TILE_SIZE // factor)
            pyxel.blt(sx, sy, self.t_image_selector.value, tx * 8, ty * 8, (TILEMAP_TILE_SIZE // factor), (TILEMAP_TILE_SIZE // factor))

    def copy_tilemap(self):
        if not self.t_selection or self.current_tool != SELECT_TOOL:
            return
        
        x0, y0, x1, y1 = self.t_selection
        min_x, min_y = min(x0, x1), min(y0, y1)
        max_x, max_y = max(x0, x1), max(y0, y1)
        
        self.t_clipboard = []
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                abs_x = x + self.t_tilemap_offset_x
                abs_y = y + self.t_tilemap_offset_y
                tile = pyxel.tilemaps[self.t_tilemap_selector.value].pget(abs_x, abs_y)
                self.t_clipboard.append((x - min_x, y - min_y, tile))

    def cut_tilemap(self):
        if not self.t_selection or self.current_tool != SELECT_TOOL:
            return
        
        self.copy_tilemap()
        
        x0, y0, x1, y1 = self.t_selection
        min_x, min_y = min(x0, x1), min(y0, y1)
        max_x, max_y = max(x0, x1), max(y0, y1)
        
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                abs_x = x + self.t_tilemap_offset_x
                abs_y = y + self.t_tilemap_offset_y
                pyxel.tilemaps[self.t_tilemap_selector.value].pset(abs_x, abs_y, (0, 0))

    def paste_tilemap(self):
        if not self.t_clipboard or not self.t_selection or self.current_tool != SELECT_TOOL:
            return
        
        x0, y0, x1, y1 = self.t_selection
        min_x, min_y = min(x0, x1), min(y0, y1)
        
        for rel_x, rel_y, tile in self.t_clipboard:
            abs_x = min_x + rel_x + self.t_tilemap_offset_x
            abs_y = min_y + rel_y + self.t_tilemap_offset_y
            
            if 0 <= abs_x < pyxel.tilemaps[self.t_tilemap_selector.value].width and 0 <= abs_y < pyxel.tilemaps[self.t_tilemap_selector.value].height:
                pyxel.tilemaps[self.t_tilemap_selector.value].pset(abs_x, abs_y, tile)

    def rotate_tilemap_selection(self):
        if not self.t_selection or self.current_tool != SELECT_TOOL:
            return
        
        x0, y0, x1, y1 = self.t_selection
        min_x, min_y = min(x0, x1), min(y0, y1)
        max_x, max_y = max(x0, x1), max(y0, y1)
        
        width = max_x - min_x + 1
        height = max_y - min_y + 1

        if width != height:
            return
        
        temp_buffer = []
        for y in range(min_y, max_y + 1):
            row = []
            for x in range(min_x, max_x + 1):
                abs_x = x + self.t_tilemap_offset_x
                abs_y = y + self.t_tilemap_offset_y
                row.append(pyxel.tilemaps[self.t_tilemap_selector.value].pget(abs_x, abs_y))
            temp_buffer.append(row)
        
        for y in range(height):
            for x in range(width):
                new_x = min_x + y
                new_y = min_y + (width - 1 - x)
                
                if new_x <= max_x and new_y <= max_y:
                    abs_x = new_x + self.t_tilemap_offset_x
                    abs_y = new_y + self.t_tilemap_offset_y
                    if 0 <= abs_x < pyxel.tilemaps[self.t_tilemap_selector.value].width and 0 <= abs_y < pyxel.tilemaps[self.t_tilemap_selector.value].height:
                        pyxel.tilemaps[self.t_tilemap_selector.value].pset(abs_x, abs_y, temp_buffer[y][x])

    def flip_tilemap_selection_horizontal(self):
        if not self.t_selection or self.current_tool != SELECT_TOOL:
            return
        
        x0, y0, x1, y1 = self.t_selection
        min_x, min_y = min(x0, x1), min(y0, y1)
        max_x, max_y = max(x0, x1), max(y0, y1)
        
        width = max_x - min_x + 1
        
        temp_buffer = []
        for y in range(min_y, max_y + 1):
            row = []
            for x in range(min_x, max_x + 1):
                abs_x = x + self.t_tilemap_offset_x
                abs_y = y + self.t_tilemap_offset_y
                row.append(pyxel.tilemaps[self.t_tilemap_selector.value].pget(abs_x, abs_y))
            temp_buffer.append(row)

        for y in range(max_y - min_y + 1):
            for x in range(width):
                new_x = min_x + (width - 1 - x)
                abs_x = new_x + self.t_tilemap_offset_x
                abs_y = (min_y + y) + self.t_tilemap_offset_y
                if 0 <= abs_x < pyxel.tilemaps[self.t_tilemap_selector.value].width and 0 <= abs_y < pyxel.tilemaps[self.t_tilemap_selector.value].height:
                    pyxel.tilemaps[self.t_tilemap_selector.value].pset(abs_x, abs_y, temp_buffer[y][x])

    def flip_tilemap_selection_vertical(self):
        if not self.t_selection or self.current_tool != SELECT_TOOL:
            return
        
        x0, y0, x1, y1 = self.t_selection
        min_x, min_y = min(x0, x1), min(y0, y1)
        max_x, max_y = max(x0, x1), max(y0, y1)
        
        height = max_y - min_y + 1
        
        temp_buffer = []
        for y in range(min_y, max_y + 1):
            row = []
            for x in range(min_x, max_x + 1):
                abs_x = x + self.t_tilemap_offset_x
                abs_y = y + self.t_tilemap_offset_y
                row.append(pyxel.tilemaps[self.t_tilemap_selector.value].pget(abs_x, abs_y))
            temp_buffer.append(row)
        
        for y in range(height):
            for x in range(max_x - min_x + 1):
                new_y = min_y + (height - 1 - y)
                abs_x = (min_x + x) + self.t_tilemap_offset_x
                abs_y = new_y + self.t_tilemap_offset_y
                if 0 <= abs_x < pyxel.tilemaps[self.t_tilemap_selector.value].width and 0 <= abs_y < pyxel.tilemaps[self.t_tilemap_selector.value].height:
                    pyxel.tilemaps[self.t_tilemap_selector.value].pset(abs_x, abs_y, temp_buffer[y][x])

    def update_tilemap_editor(self):
        #? Zoom var
        factor = self.t_zoom_selector.value // 16

        #? Grid
        if pyxel.btnp(pyxel.KEY_G): self.t_grid = not self.t_grid

        #? Selection Shortcuts
        if pyxel.btn(pyxel.KEY_CTRL) or pyxel.btn(pyxel.KEY_GUI):
            if pyxel.btnp(pyxel.KEY_R):
                self.push_tilemap_history()
                self.rotate_tilemap_selection()
            elif pyxel.btnp(pyxel.KEY_H):
                self.push_tilemap_history()
                self.flip_tilemap_selection_horizontal()
            elif pyxel.btnp(pyxel.KEY_F):
                self.push_tilemap_history()
                self.flip_tilemap_selection_vertical()
            elif pyxel.btnp(pyxel.KEY_C):
                self.copy_tilemap()
            elif pyxel.btnp(pyxel.KEY_X):
                self.push_tilemap_history()
                self.cut_tilemap()
            elif pyxel.btnp(pyxel.KEY_V):
                self.push_tilemap_history()
                self.paste_tilemap()
            elif pyxel.btnp(pyxel.KEY_Z):
                self.undo_tilemap()
            elif pyxel.btnp(pyxel.KEY_T):
                self.place_tiles()

        #? Tools Shortcut
        for key in TOOLS_SHORTCUTS.keys():
            if pyxel.btnp(key) and not (pyxel.btn(pyxel.KEY_CTRL) or pyxel.btn(pyxel.KEY_GUI)):
                self.current_tool = TOOLS_SHORTCUTS[key]

        #? Editor
        if collision_point_rect(pyxel.mouse_x, pyxel.mouse_y, EDITOR_X, EDITOR_Y, EDITOR_SIZE, EDITOR_SIZE):
            mx = (pyxel.mouse_x - EDITOR_X) // (TILEMAP_TILE_SIZE // factor) + self.t_tilemap_offset_x 
            my = (pyxel.mouse_y - EDITOR_Y) // (TILEMAP_TILE_SIZE // factor) + self.t_tilemap_offset_y 
            tx, ty = (self.t_tile_selected[0] + self.t_tile_offset_x // 8, self.t_tile_selected[1] + self.t_tile_offset_y // 8)

            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):

                if self.current_tool in [FILLED_RECT_TOOL, RECT_TOOL, FILLED_ELLI_TOOL, ELLI_TOOL, LINE_TOOL]:
                    self.t_drag_start = (mx, my)
                elif self.current_tool == BUCKET_TOOL:
                    self.push_tilemap_history()
                    self.commit_tiles(self.flood_fill_tilemap(mx, my, pyxel.tilemaps[self.t_tilemap_selector.value].pget(mx, my), (tx, ty)))
                elif self.current_tool == SWAP_TOOL:
                    self.push_tilemap_history()
                    self.commit_tiles(self.swap_fill_tilemap(pyxel.tilemaps[self.t_tilemap_selector.value].pget(mx, my), (tx, ty)))
                elif self.current_tool == SELECT_TOOL:
                    x = (pyxel.mouse_x - EDITOR_X) // (TILEMAP_TILE_SIZE // factor)
                    y = (pyxel.mouse_y - EDITOR_Y) // (TILEMAP_TILE_SIZE // factor)
                    self.t_selection = [x, y, x, y]

            if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
                if self.current_tool == PEN_TOOL:
                    pyxel.tilemaps[self.t_tilemap_selector.value].pset(mx, my, (tx, ty))
                elif self.current_tool == MIRROR_TOOL:
                    pyxel.tilemaps[self.t_tilemap_selector.value].pset(mx, my, (tx, ty))
                    axis_x = self.t_tilemap_offset_x + self.t_zoom_selector.value // 2
                    mx_mirror = axis_x - (mx - axis_x) - 1
                    if 0 <= mx_mirror < pyxel.tilemaps[self.t_tilemap_selector.value].width:
                        pyxel.tilemaps[self.t_tilemap_selector.value].pset(mx_mirror, my, (tx, ty))
                elif self.current_tool == SELECT_TOOL and self.t_selection:
                    x = (pyxel.mouse_x - EDITOR_X) // (TILEMAP_TILE_SIZE // factor)
                    y = (pyxel.mouse_y - EDITOR_Y) // (TILEMAP_TILE_SIZE // factor)
                    self.t_selection[2] = x
                    self.t_selection[3] = y

            if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) and self.t_drag_start:
                x0, y0 = self.t_drag_start
                max_x, max_y = max(x0, mx), max(y0, my)
                min_x, min_y = min(x0, mx), min(y0, my)

                self.push_tilemap_history()

                if self.current_tool == FILLED_RECT_TOOL:
                    self.commit_tiles(self.rect(min_x, min_y, max_x, max_y))
                elif self.current_tool == RECT_TOOL:
                    self.commit_tiles(self.rect(min_x, min_y, max_x, max_y, False))
                elif self.current_tool == FILLED_ELLI_TOOL:
                    self.commit_tiles(self.elli(min_x, min_y, max_x, max_y))
                elif self.current_tool == ELLI_TOOL:
                    self.commit_tiles(self.elli(min_x, min_y, max_x, max_y, False))
                elif self.current_tool == LINE_TOOL:
                    self.commit_tiles(self.line(x0, y0, mx, my))

                self.t_drag_start = None

            if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
                tx, ty = pyxel.tilemaps[self.t_tilemap_selector.value].pget(mx, my)
                self.t_tile_offset_x = tx * 8
                self.t_tile_offset_y = ty * 8
                self.t_tile_selected = (0, 0)
        else:
            self.t_drag_start = None

        #? Tiles Picker
        if collision_point_rect(pyxel.mouse_x, pyxel.mouse_y, TILES_PICKER_X, TILES_PICKER_Y, TILES_PICKER_SIZE, TILES_PICKER_SIZE):
            mx = (pyxel.mouse_x - TILES_PICKER_X) // 8
            my = (pyxel.mouse_y - TILES_PICKER_Y) // 8

            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.t_tile_selected = (mx, my)

        #? Movement
        if pyxel.btn(pyxel.KEY_LSHIFT):
            if pyxel.btnp(pyxel.KEY_RIGHT, repeat=5):
                self.t_tile_offset_x += 8
            if pyxel.btnp(pyxel.KEY_LEFT, repeat=5):
                self.t_tile_offset_x -= 8
            if pyxel.btnp(pyxel.KEY_DOWN, repeat=5):
                self.t_tile_offset_y += 8
            if pyxel.btnp(pyxel.KEY_UP, repeat=5):
                self.t_tile_offset_y -= 8
        else:
            if pyxel.btnp(pyxel.KEY_RIGHT, repeat=5):
                self.t_tilemap_offset_x += 8
            if pyxel.btnp(pyxel.KEY_LEFT, repeat=5):
                self.t_tilemap_offset_x -= 8
            if pyxel.btnp(pyxel.KEY_DOWN, repeat=5):
                self.t_tilemap_offset_y += 8
            if pyxel.btnp(pyxel.KEY_UP, repeat=5):
                self.t_tilemap_offset_y -= 8
        self.t_tilemap_offset_x = max(0, min(pyxel.tilemaps[self.t_tilemap_selector.value].width - self.t_zoom_selector.value, self.t_tilemap_offset_x))
        self.t_tilemap_offset_y = max(0, min(pyxel.tilemaps[self.t_tilemap_selector.value].height - self.t_zoom_selector.value, self.t_tilemap_offset_y))
        self.t_tile_offset_x = max(0, min(pyxel.images[self.t_image_selector.value].width - 64, self.t_tile_offset_x))
        self.t_tile_offset_y = max(0, min(pyxel.images[self.t_image_selector.value].height - 64, self.t_tile_offset_y))

        #? Selectors
        t = self.t_tilemap_selector.update()
        if t:
            imgsrc = pyxel.tilemaps[self.t_tilemap_selector.value].imgsrc
            self.t_image_selector.value = imgsrc if isinstance(imgsrc, int) else pyxel.images.to_list().index(imgsrc)
        t = self.t_image_selector.update()
        if t:
            pyxel.tilemaps[self.t_tilemap_selector.value].imgsrc = self.t_image_selector.value
        self.t_layer_selector.update()
        self.t_grid_selector.update()
        self.t_zoom_selector.update()

        #? Tool Buttons
        for tool_button in self.tool_buttons:
            c = tool_button.update(self.current_tool)
            self.current_tool = c if c is not None else self.current_tool

    def draw_tilemap_editor(self):
        #? Zoom var
        factor = self.t_zoom_selector.value // 16

        #? Selectors
        self.t_tilemap_selector.draw()
        self.t_image_selector.draw()
        self.t_layer_selector.draw()
        self.t_grid_selector.draw()
        self.t_zoom_selector.draw()

        #? Editor
        o = 192 if factor == 4 else 64 if factor == 2 else 0
        if self.t_layer_selector.value != "None":
            pyxel.bltm(EDITOR_X - o, EDITOR_Y - o, self.t_layer_selector.value, self.t_tilemap_offset_x * 8, self.t_tilemap_offset_y * 8, EDITOR_SIZE * factor, EDITOR_SIZE * factor, scale=1/factor)
            pyxel.bltm(EDITOR_X - o, EDITOR_Y - o, self.t_tilemap_selector.value, self.t_tilemap_offset_x * 8, self.t_tilemap_offset_y * 8, EDITOR_SIZE * factor, EDITOR_SIZE * factor, 0, scale=1/factor)
        else:
            pyxel.bltm(EDITOR_X - o, EDITOR_Y - o, self.t_tilemap_selector.value, self.t_tilemap_offset_x * 8, self.t_tilemap_offset_y * 8, EDITOR_SIZE * factor, EDITOR_SIZE * factor, scale=1/factor)

        #? Draw Preview
        if collision_point_rect(pyxel.mouse_x, pyxel.mouse_y, EDITOR_X, EDITOR_Y, EDITOR_SIZE, EDITOR_SIZE):
            mx = (pyxel.mouse_x - EDITOR_X) // (TILEMAP_TILE_SIZE // factor) + self.t_tilemap_offset_x
            my = (pyxel.mouse_y - EDITOR_Y) // (TILEMAP_TILE_SIZE // factor) + self.t_tilemap_offset_y
            tx, ty = (self.t_tile_selected[0] + self.t_tile_offset_x // 8, self.t_tile_selected[1] + self.t_tile_offset_y // 8)
            tiles = set()

            pyxel.text(EDITOR_X + 1, 8, f"({mx},{my})", self.COLORS_LEN + 1)

            if self.current_tool == BUCKET_TOOL:
                tiles = self.flood_fill_tilemap(mx, my, pyxel.tilemaps[self.t_tilemap_selector.value].pget(mx, my), (tx, ty))
            elif self.current_tool == SWAP_TOOL:
                tiles = self.swap_fill_tilemap(pyxel.tilemaps[self.t_tilemap_selector.value].pget(mx, my), (tx, ty))

            if self.t_drag_start:
                x0, y0 = self.t_drag_start
                min_x, max_x = min(x0, mx), max(x0, mx)
                min_y, max_y = min(y0, my), max(y0, my)

                if self.current_tool == FILLED_RECT_TOOL:
                    tiles = self.rect(min_x, min_y, max_x, max_y)
                elif self.current_tool == RECT_TOOL:
                    tiles = self.rect(min_x, min_y, max_x, max_y, False)
                elif self.current_tool == FILLED_ELLI_TOOL:
                    tiles = self.elli(min_x, min_y, max_x, max_y)
                elif self.current_tool == ELLI_TOOL:
                    tiles = self.elli(min_x, min_y, max_x, max_y, False)
                elif self.current_tool == LINE_TOOL:
                    tiles = self.line(x0, y0, mx, my)

            self.draw_preview_tiles(tiles)

        #? Grid
        if self.t_grid:
            for y in range(EDITOR_Y, EDITOR_Y + EDITOR_SIZE, self.t_grid_selector.value * (TILEMAP_TILE_SIZE // factor)):
                pyxel.rect(EDITOR_X, y, EDITOR_SIZE, 1, self.COLORS_LEN)
            for x in range(EDITOR_X, EDITOR_X + EDITOR_SIZE, self.t_grid_selector.value * (TILEMAP_TILE_SIZE // factor)):
                pyxel.rect(x, EDITOR_Y, 1, EDITOR_SIZE, self.COLORS_LEN)
            pyxel.rect(EDITOR_X, EDITOR_Y + EDITOR_SIZE - 1, EDITOR_SIZE, 1, self.COLORS_LEN)
            pyxel.rect(EDITOR_X + EDITOR_SIZE - 1, EDITOR_Y, 1, EDITOR_SIZE, self.COLORS_LEN)

        #? Selection Preview
        if self.t_selection and self.current_tool == SELECT_TOOL:
            x0, y0, x1, y1 = self.t_selection
            min_x, max_x = min(x0, x1), max(x0, x1)
            min_y, max_y = min(y0, y1), max(y0, y1)

            pyxel.rectb(EDITOR_X + min_x * (TILEMAP_TILE_SIZE // factor), EDITOR_Y + min_y * (TILEMAP_TILE_SIZE // factor), (max_x - min_x + 1) * (TILEMAP_TILE_SIZE // factor), (max_y - min_y + 1) * (TILEMAP_TILE_SIZE // factor), self.COLORS_LEN + 1)

        #? Tool Buttons
        for tool_button in self.tool_buttons:
            tool_button.draw()

        #? Tiles Picker
        pyxel.blt(TILES_PICKER_X, TILES_PICKER_Y, self.t_image_selector.value, self.t_tile_offset_x, self.t_tile_offset_y, 64, 64)
        pyxel.rectb(TILES_PICKER_X + self.t_tile_selected[0] * 8, TILES_PICKER_Y + self.t_tile_selected[1] * 8, 8, 8, self.COLORS_LEN + 1)
        if collision_point_rect(pyxel.mouse_x, pyxel.mouse_y, TILES_PICKER_X, TILES_PICKER_Y, TILES_PICKER_SIZE, TILES_PICKER_SIZE):
            tx = (pyxel.mouse_x - TILES_PICKER_X) // 8 + self.t_tile_offset_x // 8
            ty = (pyxel.mouse_y - TILES_PICKER_Y) // 8 + self.t_tile_offset_y // 8
            pyxel.text(TILES_PICKER_X, TILES_PICKER_Y - 8, f"({tx},{ty})", self.COLORS_LEN + 1)
        else:
            pyxel.text(TILES_PICKER_X, TILES_PICKER_Y - 8, f"({self.t_tile_offset_x // 8 + self.t_tile_selected[0]},{self.t_tile_offset_y // 8 + self.t_tile_selected[1]})", self.COLORS_LEN + 1)

    #? ---------- AUTOTILE EDITOR ---------- ?#

    def get_neighbors(self, tilemap_id:int, tiles_y:list, x:int, y:int):
        n = 0
        if y > 0 and pyxel.tilemaps[tilemap_id].pget(x, y - 1)[1] in tiles_y:
            n += 1
        if x < pyxel.tilemaps[self.t_tilemap_selector.value].width and pyxel.tilemaps[tilemap_id].pget(x + 1, y)[1] in tiles_y:
            n += 2
        if y < pyxel.tilemaps[self.t_tilemap_selector.value].height and pyxel.tilemaps[tilemap_id].pget(x, y + 1)[1] in tiles_y:
            n += 4
        if x > 0 and pyxel.tilemaps[tilemap_id].pget(x - 1, y)[1] in tiles_y:
            n += 8

        if n == 15:
            if y > 0 and x > 0 and pyxel.tilemaps[tilemap_id].pget(x - 1, y - 1)[1] in tiles_y:
                n += 1
            if y > 0 and x < pyxel.tilemaps[self.t_tilemap_selector.value].width and pyxel.tilemaps[tilemap_id].pget(x + 1, y - 1)[1] in tiles_y:
                n += 2
            if y < pyxel.tilemaps[self.t_tilemap_selector.value].height and x < pyxel.tilemaps[self.t_tilemap_selector.value].width and pyxel.tilemaps[tilemap_id].pget(x + 1, y + 1)[1] in tiles_y:
                n += 4
            if y < pyxel.tilemaps[self.t_tilemap_selector.value].height and x > 0 and pyxel.tilemaps[tilemap_id].pget(x - 1, y + 1)[1] in tiles_y:
                n += 8

        return n
    
    def place_tiles(self):
        new_tiles = [[(0, 0) for _ in range(pyxel.tilemaps[self.t_tilemap_selector.value].width)] for _ in range(pyxel.tilemaps[self.t_tilemap_selector.value].height)]

        for y in range(pyxel.tilemaps[self.t_tilemap_selector.value].height):
            for x in range(pyxel.tilemaps[self.t_tilemap_selector.value].width):
                tile_x, tile_y  = pyxel.tilemaps[self.t_tilemap_selector.value].pget(x, y)
                tiles_y = self.a_tiles_y[self.t_image_selector.value]

                if tile_y in tiles_y:
                    neighbors = self.get_neighbors(self.t_tilemap_selector.value, tiles_y, x, y)
                    new_tiles[y][x] = (neighbors, tile_y)
                else:
                    new_tiles[y][x] = (tile_x, tile_y)

        for y in range(pyxel.tilemaps[self.t_tilemap_selector.value].height):
            for x in range(pyxel.tilemaps[self.t_tilemap_selector.value].width):
                pyxel.tilemaps[self.t_tilemap_selector.value].pset(x, y, new_tiles[y][x])

    def place_a_buttons(self):
        l = []
        c = 0
        for y in [2, 12]:
            for x in range(16):
                l.append(Button(80 + x * 10, y, c, self.COLORS_LEN))
                c += 1
        return l

    def draw_tileset(self, x:int, y:int, image:int, tile_y:int):
        pyxel.blt(x, y + 8, image, 0, tile_y * 8, 8, 8)

        pyxel.blt(x + 10, y, image, 6 * 8, tile_y * 8, 8, 8)
        pyxel.blt(x + 18, y, image, 14 * 8, tile_y * 8, 8, 8)
        pyxel.blt(x + 26, y, image, 12 * 8, tile_y * 8, 8, 8)
        pyxel.blt(x + 10, y + 8, image, 7 * 8, tile_y * 8, 8, 8)
        pyxel.blt(x + 18, y + 8, image, 30 * 8, tile_y * 8, 8, 8)
        pyxel.blt(x + 26, y + 8, image, 13 * 8, tile_y * 8, 8, 8)
        pyxel.blt(x + 10, y + 16, image, 3 * 8, tile_y * 8, 8, 8)
        pyxel.blt(x + 18, y + 16, image, 11 * 8, tile_y * 8, 8, 8)
        pyxel.blt(x + 26, y + 16, image, 9 * 8, tile_y * 8, 8, 8)

        pyxel.blt(x + 36, y, image, 4 * 8, tile_y * 8, 8, 8)
        pyxel.blt(x + 36, y + 8, image, 5 * 8, tile_y * 8, 8, 8)
        pyxel.blt(x + 36, y + 16, image, 1 * 8, tile_y * 8, 8, 8)

        pyxel.blt(x + 10, y + 26, image, 2 * 8, tile_y * 8, 8, 8)
        pyxel.blt(x + 18, y + 26, image, 10 * 8, tile_y * 8, 8, 8)
        pyxel.blt(x + 26, y + 26, image, 8 * 8, tile_y * 8, 8, 8)

    def update_autotile_editor(self):
        #? Buttons
        for button in self.a_buttons[self.a_image_selector.value]:
            button.update()

        self.a_tiles_y[self.a_image_selector.value] = [b.id for b in self.a_buttons[self.a_image_selector.value] if b.selected]

        #? Selectors
        self.a_image_selector.update()

    def draw_autotile_editor(self):
        #? Selectors
        self.a_image_selector.draw()

        #? Buttons
        for button in self.a_buttons[self.a_image_selector.value]:
            button.draw()

        #? Tilesets
        x, y = 0, 0
        for i in range(len(self.a_tiles_y[self.a_image_selector.value])):
            self.draw_tileset(16 + x, 22 + y, self.a_image_selector.value, self.a_tiles_y[self.a_image_selector.value][i])
            x = (x + 46) % 230
            if x == 0:
                y += 36

    #? ---------- MAIN FUNCTIONS ---------- ?#

    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self.save()
            pyxel.quit()

        if pyxel.btnp(pyxel.KEY_S) and (pyxel.btn(pyxel.KEY_CTRL) or pyxel.btn(pyxel.KEY_GUI)):
            self.save()

        for tab_button in self.tab_buttons:
            c = tab_button.update(self.current_tab)
            self.current_tab = c if c is not None else self.current_tab

        if self.current_tab == SPRITE_EDITOR:         self.update_sprite_editor()
        elif self.current_tab == TILEMAP_EDITOR:      self.update_tilemap_editor()
        elif self.current_tab == AUTOTILE_EDITOR:     self.update_autotile_editor()

    def draw(self):
        pyxel.cls(self.COLORS_LEN)

        for tab_button in self.tab_buttons:
            tab_button.draw()

        if self.current_tab == SPRITE_EDITOR:         self.draw_sprite_editor()
        elif self.current_tab == TILEMAP_EDITOR:      self.draw_tilemap_editor()
        elif self.current_tab == AUTOTILE_EDITOR:     self.draw_autotile_editor()

        for y in range(len(MOUSE_ICON)):
            for x in range(len(MOUSE_ICON[y])):
                if MOUSE_ICON[y][x] != 0:
                    pyxel.rect(pyxel.mouse_x + x, pyxel.mouse_y + y, 1, 1, self.COLORS_LEN + MOUSE_ICON[y][x])

#? ---------- MAIN ---------- ?#

if __name__ == "__main__":
    PALETTE =[0x000000, 0x1D2B53, 0x7E2553, 0x008751, 0xAB5236, 0x5F574F, 0xC2C3C7, 0xFFF1E8, 0xFF004D, 0xFFA300, 0xFFEC27, 0x00E436, 0x29ADFF, 0x83769C, 0xFF77A8, 0xFFCCAA, 0x1A1C2C, 0x5D275D, 0x008080, 0x1B6535, 0x73464D, 0x9D9D9D, 0xFFFFFF, 0xFF6C24, 0xFFD93F, 0xB2D732, 0x3CA370, 0x0066CC, 0x45283C, 0xA288AE, 0xF3B4B4, 0xD4A373, 0xFF00FF]
    Editor("assets.pyxres", PALETTE)