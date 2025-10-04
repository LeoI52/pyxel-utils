"""
@author : Léo Imbert
@created : 28/09/2025
@updated : 04/10/2025

TODO

- Square if shift pressed
- Circle if shift pressed
- Outside Editor Check Redo

"""

#? ---------- IMPORTATIONS ---------- ?#

import pyxel
import os

#? ---------- CONSTANTS ---------- ?#

EDITOR_X, EDITOR_Y, EDITOR_SIZE = 25, 16, 128
TILEMAP_TILE_SIZE = 8

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

TILEMAP_ICON = [[1]*16,[1]+[0]*14+[1],[1]+[0]*14+[1],[1,0,0,1,1,1,1,0,0,1,1,1,1,0,0,1],[1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1],[1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1],[1,0,0,1,1,1,1,0,0,1,1,1,1,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,1,1,1,1,0,0,1,1,1,1,0,0,1],[1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1],[1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1],[1,0,0,1,1,1,1,0,0,1,1,1,1,0,0,1],[1]+[0]*14+[1],[1]+[0]*14+[1],[1]*16]
SPRITE_ICON = [[1]*16,[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,1,1,1,1,1,1,0,0,0,0,1],[1,0,0,1,1,1,1,1,1,1,1,1,1,0,0,1],[1,0,0,1,1,1,1,1,1,1,1,1,1,0,0,1],[1,0,0,0,0,1,1,1,1,1,1,0,0,0,0,1],[1,0,0,0,0,1,1,1,1,1,1,0,0,0,0,1],[1,0,0,0,1,1,1,1,1,1,1,1,0,0,0,1],[1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1],[1,0,1,1,0,1,1,1,1,1,1,0,1,1,0,1],[1,0,0,0,0,1,1,1,1,1,1,0,0,0,0,1],[1,0,0,0,0,1,1,1,1,1,1,0,0,0,0,1],[1,0,0,1,1,1,1,0,0,1,1,1,1,0,0,1],[1,0,0,1,1,1,1,0,0,1,1,1,1,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1]*16]
AUTOTILE_ICON = [[1]*16,[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,1,1,1,1,1,1,1,1,1,1,0,0,1],[1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1],[1,0,0,1,0,1,1,1,1,1,1,0,1,0,0,1],[1,0,0,1,0,1,1,1,1,1,1,0,1,0,0,1],[1,0,0,1,0,1,1,1,1,1,1,0,1,0,0,1],[1,0,0,1,0,1,1,1,1,1,1,0,1,0,0,1],[1,0,0,1,0,1,1,1,1,1,1,0,1,0,0,1],[1,0,0,1,0,1,1,1,1,1,1,0,1,0,0,1],[1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1],[1,0,0,1,1,1,1,1,1,1,1,1,1,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1]*16]
ANIMATION_ICON = [[1]*16,[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,1,1,0,0,0,1,1,0,0,0,0,1],[1,0,0,1,0,0,1,0,1,0,0,1,0,0,0,1],[1,0,0,1,0,0,1,0,1,0,0,1,0,0,0,1],[1,0,0,0,1,1,0,0,0,1,1,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,1,1,1,1,1,1,1,1,1,0,0,0,1],[1,0,1,1,1,1,1,1,1,1,1,1,0,1,0,1],[1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1],[1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1],[1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1],[1,0,1,1,1,1,1,1,1,1,1,1,0,1,0,1],[1,0,0,1,1,1,1,1,1,1,1,1,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1]*16]

SPRITE_EDITOR = 0
TILEMAP_EDITOR = 1
AUTOTILE_EDITOR = 2
ANIMATION_EDITOR = 3

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
    pyxel.KEY_P:PEN_TOOL,
    pyxel.KEY_M:MIRROR_TOOL,
    pyxel.KEY_L:LINE_TOOL,
    pyxel.KEY_R:FILLED_RECT_TOOL,
    pyxel.KEY_E:FILLED_ELLI_TOOL,
    pyxel.KEY_B:BUCKET_TOOL,
    pyxel.KEY_O:SWAP_TOOL,
}

PREVIOUS_ICON = [[1,1,1,1,1,1,1,1],[1,0,0,0,1,0,0,1],[1,0,0,1,0,0,0,1],[1,0,1,0,0,1,0,1],[1,0,1,0,0,1,0,1],[1,0,0,1,0,0,0,1],[1,0,0,0,1,0,0,1],[1,1,1,1,1,1,1,1]]
PLAY_ICON = [[1,1,1,1,1,1,1,1],[1,0,0,0,0,0,0,1],[1,0,1,0,0,1,0,1],[1,0,1,0,0,1,0,1],[1,0,1,0,0,1,0,1],[1,0,1,0,0,1,0,1],[1,0,0,0,0,0,0,1],[1,1,1,1,1,1,1,1]]
NEXT_ICON = [[1,1,1,1,1,1,1,1],[1,0,0,1,0,0,0,1],[1,0,0,0,1,0,0,1],[1,0,1,0,0,1,0,1],[1,0,1,0,0,1,0,1],[1,0,0,0,1,0,0,1],[1,0,0,1,0,0,0,1],[1,1,1,1,1,1,1,1]]

#? ---------- UTILITY FUNCTIONS ---------- ?#

def collision_point_rect(x1:int, y1:int, x2:int, y2:int, w2:int, h2:int)-> bool:
    return x2 <= x1 < x2 + w2 and y2 <= y1 < y2 + h2

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

    def update(self, current_id:int):
        if collision_point_rect(pyxel.mouse_x, pyxel.mouse_y, self.x, self.y, self.w, self.h) and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            return self.id
        self.selected = current_id == self.id
        return None

    def draw(self):
        for y in range(len(self.icon)):
            for x in range(len(self.icon[y])):
                if self.icon[y][x] == 1:
                    c = self.colors_len + 1 if self.selected else self.colors_len + 2
                    pyxel.rect(self.x + x, self.y + y, 1, 1, c)

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

class Selector:

    def __init__(self, x:int, y:int, label:str, values:list, colors_len:int, start_index:int=0):
        self.x, self.y = x, y
        self.label = label
        self.values = values
        self.colors_len = colors_len
        self.index = start_index

        self.btn_w = 8
        self.btn_h = 8

    @property
    def value(self):
        return self.values[self.index]
    
    @value.setter
    def value(self, new_value:int):
        self.index = self.values.index(new_value)

    def update(self):
        mx, my = pyxel.mouse_x, pyxel.mouse_y
        label_w = len(self.label) * 4
        value_str = str(self.value)
        value_w = len(value_str) * 4
        minus_x = self.x + label_w
        plus_x = minus_x + self.btn_w + value_w + 4

        if (minus_x <= mx < minus_x + self.btn_w and self.y <= my < self.y + self.btn_h and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)):
            if self.index > 0:
                self.index -= 1

        if (plus_x <= mx < plus_x + self.btn_w and self.y <= my < self.y + self.btn_h and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)):
            if self.index < len(self.values) - 1:
                self.index += 1

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

class Entry:

    def __init__(self, x:int, y:int, label:str, colors_len:int, max_length:int=10, default_value:str=""):
        self.x, self.y = x, y
        self.label = label
        self.colors_len = colors_len
        self.max_length = max_length
        self.text = default_value
        self.active = False
        self.cursor_visible = True
        self.cursor_timer = 0
        
        self.entry_w = max_length * 4 + 4
        self.entry_h = 8

    @property
    def value(self):
        return self.text
    
    @value.setter
    def value(self, new_value:str):
        self.text = new_value[:self.max_length]

    def update(self):
        mx, my = pyxel.mouse_x, pyxel.mouse_y
        label_w = len(self.label) * 4
        entry_x = self.x + label_w
        
        if (entry_x <= mx < entry_x + self.entry_w and 
            self.y <= my < self.y + self.entry_h and 
            pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)):
            self.active = True
        elif pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.KEY_RETURN):
            self.active = False
        
        if self.active:
            if pyxel.btnp(pyxel.KEY_BACKSPACE) and len(self.text) > 0:
                self.text = self.text[:-1]
            
            for key in range(pyxel.KEY_A, pyxel.KEY_Z + 1):
                if pyxel.btnp(key):
                    char = chr(ord('a') + (key - pyxel.KEY_A))
                    if pyxel.btn(pyxel.KEY_SHIFT):
                        char = char.upper()
                    if len(self.text) < self.max_length:
                        self.text += char
            
            for key in range(pyxel.KEY_0, pyxel.KEY_9 + 1):
                if pyxel.btnp(key):
                    if len(self.text) < self.max_length:
                        self.text += chr(ord('0') + (key - pyxel.KEY_0))

            if pyxel.btnp(pyxel.KEY_COMMA) and len(self.text) < self.max_length:
                self.text += ","
            
            if pyxel.btnp(pyxel.KEY_SPACE) and len(self.text) < self.max_length:
                self.text += " "
        
        self.cursor_timer += 1
        if self.cursor_timer >= 30:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0

    def draw(self):
        label_w = len(self.label) * 4
        entry_x = self.x + label_w
        
        pyxel.text(self.x, self.y + 2, self.label, self.colors_len + 1)
        
        box_color = self.colors_len + 2 if not self.active else self.colors_len + 1
        pyxel.rect(entry_x, self.y, self.entry_w, self.entry_h, self.colors_len)
        pyxel.rectb(entry_x, self.y, self.entry_w, self.entry_h, box_color)
        
        if self.text:
            pyxel.text(entry_x + 2, self.y + 2, self.text, self.colors_len + 1)
        
        if self.active and self.cursor_visible:
            cursor_x = entry_x + 2 + len(self.text) * 4
            pyxel.line(cursor_x, self.y + 1, cursor_x, self.y + 6, self.colors_len + 1)

#? ---------- EDITOR ---------- ?#

class Editor:

    def __init__(self, pyxres_path:str, color_palette:list, fullscreen:bool=True):
        #? ASSERTS
        assert len(color_palette) <= 32, "The color palette cannot be longer than 32 colors"

        #? Pyxel Init
        pyxel.init(258, 160, title="Editor", fps=60)
        pyxel.mouse(True)
        pyxel.fullscreen(fullscreen)
        if os.path.isfile(pyxres_path):
            pyxel.load(pyxres_path)
        pyxel.colors.from_list(color_palette + [0x2B335F, 0xEEEEEE, 0x29ADFF])

        #? CONSTANTS
        self.PYXRES_PATH = pyxres_path
        self.COLORS_LEN = len(color_palette)
        self.ZOOMS = [8, 16, 32, 64, 128]

        #? Main Variables
        self.current_editor = SPRITE_EDITOR
        self.editor_buttons = [IconButton(5, 16, SPRITE_EDITOR, SPRITE_ICON, self.COLORS_LEN),
                               IconButton(5, 32, TILEMAP_EDITOR, TILEMAP_ICON, self.COLORS_LEN),
                               IconButton(5, 48, AUTOTILE_EDITOR, AUTOTILE_ICON, self.COLORS_LEN),
                               IconButton(5, 64, ANIMATION_EDITOR, ANIMATION_ICON, self.COLORS_LEN)]
        self.current_tool = SELECT_TOOL
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
        
        #? Sprite Editor Variables
        self.s_image = 0
        self.s_zoom = 16
        self.s_color = 0
        self.s_history = []
        self.s_grid = False
        self.s_grid_size = 8
        self.s_clipboard = None
        self.s_selection = None
        self.s_drag_start = None
        self.s_offset_x = self.s_offset_y = 0
        self.s_tile_size = EDITOR_SIZE // self.s_zoom
        self.s_color_buttons = self.place_s_color_buttons(color_palette)
        self.s_image_selector = Selector(25, 148, "Image:", [0, 1, 2], self.COLORS_LEN)
        self.s_zoom_selector = Selector(101, 148, "Zoom:", self.ZOOMS[::-1], self.COLORS_LEN, 3)
        self.s_grid_selector = Selector(169, 148, "Grid size:", [1, 2, 4, 8], self.COLORS_LEN, 3)

        #? Tilemap Editor Variables
        self.t_tilemap = 0
        self.t_grid = False
        self.t_history = []
        self.t_layer = "None"
        self.t_grid_size = 8
        self.t_clipboard = None
        self.t_selection = None
        self.t_drag_start = None
        self.t_tile_selected = (0, 0)
        self.t_tile_offset_x = self.t_tile_offset_y = 0
        self.t_image = pyxel.tilemaps[self.t_tilemap].imgsrc
        self.t_tilemap_offset_x = self.t_tilemap_offset_y = 0
        self.t_grid_selector = Selector(169, 4, "Grid size:", [1, 2, 4, 8], self.COLORS_LEN, 3)
        self.t_tilemap_selector = Selector(25, 148, "Tilemap:", list(range(8)), self.COLORS_LEN)
        self.t_image_selector = Selector(169, 148, "Image:", [0, 1, 2], self.COLORS_LEN, self.t_image)
        self.t_layer_selector = Selector(93, 148, "Layer:", ["None"] + list(range(8)), self.COLORS_LEN)

        #? Autotile Editor Variables
        self.a_image = 0
        self.a_tiles_y_0 = []
        self.a_tiles_y_1 = []
        self.a_tiles_y_2 = []
        self.a_buttons_0 = self.place_a_buttons()
        self.a_buttons_1 = self.place_a_buttons()
        self.a_buttons_2 = self.place_a_buttons()
        self.a_image_selector = Selector(25, 2, "Image:", [0, 1, 2], self.COLORS_LEN)

        #? Animation Editor Variables
        self.n_frame = 0
        self.n_frame_timer = 0
        self.n_is_playing = False
        self.n_play_button = IconButton(135, 148, 1, PLAY_ICON, self.COLORS_LEN)
        self.n_next_button = IconButton(145, 148, 2, NEXT_ICON, self.COLORS_LEN)
        self.n_colkey_entry = Entry(169, 64, "Colkey:", self.COLORS_LEN, 2, "0")
        self.n_start_uv_entry = Entry(169, 32, "Start (u,v):", self.COLORS_LEN, 7)
        self.n_prev_button = IconButton(125, 148, 0, PREVIOUS_ICON, self.COLORS_LEN)
        self.n_sprite_wh_entry = Entry(169, 48, "Sprite (w,h):", self.COLORS_LEN, 5)
        self.n_frames_entry = Entry(169, 80, "Total frames:", self.COLORS_LEN, 2, "1")
        self.n_image_selector = Selector(169, 16, "Image:", [0, 1, 2], self.COLORS_LEN)
        self.n_speed_entry = Entry(169, 96, "Frame duration:", self.COLORS_LEN, 4, "10")

        #? Pyxel Run
        pyxel.run(self.update, self.draw)

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

    #? ---------- AUTOTILE METHODS ---------- ?#

    def get_neighbors(self, tilemap_id:int, tile_y:int, x:int, y:int):
        n = 0
        if y > 0 and pyxel.tilemaps[tilemap_id].pget(x, y - 1)[1] == tile_y:
            n += 1
        if x < 255 and pyxel.tilemaps[tilemap_id].pget(x + 1, y)[1] == tile_y:
            n += 2
        if y < 255 and pyxel.tilemaps[tilemap_id].pget(x, y + 1)[1] == tile_y:
            n += 4
        if x > 0 and pyxel.tilemaps[tilemap_id].pget(x - 1, y)[1] == tile_y:
            n += 8

        if n == 15:
            if y > 0 and x > 0 and pyxel.tilemaps[tilemap_id].pget(x - 1, y - 1)[1] == tile_y:
                n += 1
            if y > 0 and x < 255 and pyxel.tilemaps[tilemap_id].pget(x + 1, y - 1)[1] == tile_y:
                n += 2
            if y < 255 and x < 255 and pyxel.tilemaps[tilemap_id].pget(x + 1, y + 1)[1] == tile_y:
                n += 4
            if y < 255 and x > 0 and pyxel.tilemaps[tilemap_id].pget(x - 1, y + 1)[1] == tile_y:
                n += 8

        return n
    
    def place_tiles(self):
        new_tiles = [[(0, 0) for _ in range(255)] for _ in range(255)]

        for y in range(255):
            for x in range(255):
                tile_x, tile_y  = pyxel.tilemaps[self.t_tilemap].pget(x, y)

                if tile_y in eval(f"self.a_tiles_y_{self.t_image}"):
                    neighbors = self.get_neighbors(self.t_tilemap, tile_y, x, y)
                    new_tiles[y][x] = (neighbors, tile_y)
                else:
                    new_tiles[y][x] = (tile_x, tile_y)

        for y in range(255):
            for x in range(255):
                pyxel.tilemaps[self.t_tilemap].pset(x, y, new_tiles[y][x])

    #? ---------- SPRITE EDITOR ---------- ?#

    def place_s_color_buttons(self, color_palette:list):
        l = []
        c = x = y = 0
        while c < len(color_palette):
            l.append(ColorButton(169 + x * 8, 80 + y * 8, c, self.COLORS_LEN))
            x = (x + 1) % 8
            if x == 0:
                y += 1
            c += 1
        return l

    def push_sprite_history(self):
        snapshot = [[pyxel.images[self.s_image].pget(x, y) for x in range(256)] for y in range(256)]
        self.s_history.append((self.s_image, snapshot))
        if len(self.s_history) > 40:
            self.s_history.pop(0)

    def undo_sprite(self):
        if self.s_history:
            image, snapshot = self.s_history.pop()
            for y in range(256):
                for x in range(256):
                    pyxel.images[image].pset(x, y, snapshot[y][x])

    def flood_fill_sprite(self, x:int, y:int, old_color:int, new_color:int):
        if old_color == new_color:
            return set()

        pixels = set()
        x0, y0 = self.s_offset_x, self.s_offset_y
        x1, y1 = self.s_offset_x + self.s_zoom, self.s_offset_y + self.s_zoom

        stack = [(x, y)]
        while stack:
            cx, cy = stack.pop()
            if (x0 <= cx < x1 and y0 <= cy < y1 and pyxel.images[self.s_image].pget(cx, cy) == old_color) and (cx, cy) not in pixels:
                pixels.add((cx, cy))
                stack.extend([(cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)])
        return pixels

    def swap_fill_sprite(self, old_color:int, new_color:int):
        if old_color == new_color:
            return set()
    
        pixels = set()
        x0, y0 = self.s_offset_x, self.s_offset_y
        x1, y1 = self.s_offset_x + self.s_zoom, self.s_offset_y + self.s_zoom

        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if pyxel.images[self.s_image].pget(x, y) == old_color:
                    pixels.add((x, y))
        return pixels

    def commit_pixels(self, pixels:set):
        x0, y0 = self.s_offset_x, self.s_offset_y
        x1, y1 = self.s_offset_x + self.s_zoom - 1, self.s_offset_y + self.s_zoom - 1
        for (x, y) in pixels:
            if x0 <= x <= x1 and y0 <= y <= y1:
                pyxel.images[self.s_image].pset(x, y, self.s_color)

    def draw_preview_pixels(self, pixels:set):
        for (x, y) in pixels:
            if x < self.s_offset_x or x >= self.s_offset_x + self.s_zoom or y < self.s_offset_y or y >= self.s_offset_y + self.s_zoom:
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
                color = pyxel.images[self.s_image].pget(abs_x, abs_y)
                self.s_clipboard.append((x - min_x, y - min_y, color))

    def cut_sprite(self):
        if not self.s_selection or self.current_tool != SELECT_TOOL:
            return
        
        self.copy_sprite()
        
        x0, y0, x1, y1 = self.s_selection
        min_x, min_y = min(x0, x1), min(y0, y1)
        max_x, max_y = max(x0, x1), max(y0, y1)
        
        self.push_sprite_history()
        
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                abs_x = x + self.s_offset_x
                abs_y = y + self.s_offset_y
                pyxel.images[self.s_image].pset(abs_x, abs_y, 0)

    def paste_sprite(self):
        if not self.s_clipboard or not self.s_selection or self.current_tool != SELECT_TOOL:
            return
        
        x0, y0, x1, y1 = self.s_selection
        min_x, min_y = min(x0, x1), min(y0, y1)
        
        self.push_sprite_history()
        
        for rel_x, rel_y, color in self.s_clipboard:
            abs_x = min_x + rel_x + self.s_offset_x
            abs_y = min_y + rel_y + self.s_offset_y
            
            if 0 <= abs_x < 256 and 0 <= abs_y < 256:
                pyxel.images[self.s_image].pset(abs_x, abs_y, color)

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
                row.append(pyxel.images[self.s_image].pget(abs_x, abs_y))
            temp_buffer.append(row)
        
        self.push_sprite_history()
        
        for y in range(height):
            for x in range(width):
                new_x = min_x + y
                new_y = min_y + (width - 1 - x)
                
                if new_x <= max_x and new_y <= max_y:
                    abs_x = new_x + self.s_offset_x
                    abs_y = new_y + self.s_offset_y
                    if 0 <= abs_x < 256 and 0 <= abs_y < 256:
                        pyxel.images[self.s_image].pset(abs_x, abs_y, temp_buffer[y][x])

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
                row.append(pyxel.images[self.s_image].pget(abs_x, abs_y))
            temp_buffer.append(row)
        
        self.push_sprite_history()

        for y in range(max_y - min_y + 1):
            for x in range(width):
                new_x = min_x + (width - 1 - x)
                abs_x = new_x + self.s_offset_x
                abs_y = (min_y + y) + self.s_offset_y
                if 0 <= abs_x < 256 and 0 <= abs_y < 256:
                    pyxel.images[self.s_image].pset(abs_x, abs_y, temp_buffer[y][x])

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
                row.append(pyxel.images[self.s_image].pget(abs_x, abs_y))
            temp_buffer.append(row)
        
        self.push_sprite_history()
        
        for y in range(height):
            for x in range(max_x - min_x + 1):
                new_y = min_y + (height - 1 - y)
                abs_x = (min_x + x) + self.s_offset_x
                abs_y = new_y + self.s_offset_y
                if 0 <= abs_x < 256 and 0 <= abs_y < 256:
                    pyxel.images[self.s_image].pset(abs_x, abs_y, temp_buffer[y][x])
   
    def update_sprite_editor(self):
        #? Shortcuts
        if pyxel.btn(pyxel.KEY_CTRL) or pyxel.btn(pyxel.KEY_GUI):
            if pyxel.btnp(pyxel.KEY_Z):
                self.undo_sprite()
            elif pyxel.btnp(pyxel.KEY_C):
                self.copy_sprite()
            elif pyxel.btnp(pyxel.KEY_X):
                self.cut_sprite()
            elif pyxel.btnp(pyxel.KEY_V):
                self.paste_sprite()

        if pyxel.btnp(pyxel.KEY_R):
            self.rotate_sprite_selection()
        if pyxel.btnp(pyxel.KEY_H):
            self.flip_sprite_selection_horizontal()
        if pyxel.btnp(pyxel.KEY_V) and not (pyxel.btn(pyxel.KEY_CTRL) or pyxel.btn(pyxel.KEY_GUI)):
            self.flip_sprite_selection_vertical()

        self.s_color = (self.s_color + pyxel.mouse_wheel * -1) % self.COLORS_LEN

        if pyxel.btnp(pyxel.KEY_G): self.s_grid = not self.s_grid

        for key in TOOLS_SHORTCUTS.keys():
            if pyxel.btnp(key):
                self.current_tool = TOOLS_SHORTCUTS[key]

        #? Editor
        if collision_point_rect(pyxel.mouse_x, pyxel.mouse_y, EDITOR_X, EDITOR_Y, EDITOR_SIZE, EDITOR_SIZE):
            mx = (pyxel.mouse_x - EDITOR_X) // self.s_tile_size + self.s_offset_x
            my = (pyxel.mouse_y - EDITOR_Y) // self.s_tile_size + self.s_offset_y

            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.push_sprite_history()

                if self.current_tool in [FILLED_RECT_TOOL, RECT_TOOL, FILLED_ELLI_TOOL, ELLI_TOOL, LINE_TOOL]:
                    self.s_drag_start = (mx, my)
                elif self.current_tool == BUCKET_TOOL:
                    self.commit_pixels(self.flood_fill_sprite(mx, my, pyxel.images[self.s_image].pget(mx, my), self.s_color))
                elif self.current_tool == SWAP_TOOL:
                    self.commit_pixels(self.swap_fill_sprite(pyxel.images[self.s_image].pget(mx, my), self.s_color))
                elif self.current_tool == SELECT_TOOL:
                    x = (pyxel.mouse_x - EDITOR_X) // self.s_tile_size
                    y = (pyxel.mouse_y - EDITOR_Y) // self.s_tile_size
                    self.s_selection = [x, y, x, y]

            if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
                if self.current_tool == PEN_TOOL:
                    pyxel.images[self.s_image].pset(mx, my, self.s_color)
                elif self.current_tool == MIRROR_TOOL:
                    pyxel.images[self.s_image].pset(mx, my, self.s_color)
                    axis_x = self.s_offset_x + self.s_zoom // 2
                    mx_mirror = axis_x - (mx - axis_x) - 1
                    if 0 <= mx_mirror < 256:
                        pyxel.images[self.s_image].pset(mx_mirror, my, self.s_color)
                elif self.current_tool == SELECT_TOOL:
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
                self.current_color = pyxel.images[self.s_image].pget(mx, my)

        else:
            self.s_drag_start = None

        #? Movement
        if pyxel.btnp(pyxel.KEY_RIGHT, repeat=10):
            self.s_offset_x += self.s_zoom // 2
        if pyxel.btnp(pyxel.KEY_LEFT, repeat=10):
            self.s_offset_x -= self.s_zoom // 2
        if pyxel.btnp(pyxel.KEY_DOWN, repeat=10):
            self.s_offset_y += self.s_zoom // 2
        if pyxel.btnp(pyxel.KEY_UP, repeat=10):
            self.s_offset_y -= self.s_zoom // 2
        self.s_offset_x = max(0, min(256 - self.s_zoom, self.s_offset_x))
        self.s_offset_y = max(0, min(256 - self.s_zoom, self.s_offset_y))

        #? Selectors
        self.s_image_selector.update()
        self.s_image = self.s_image_selector.value
        self.s_zoom_selector.update()
        if self.s_zoom != self.s_zoom_selector.value:
            self.s_selection = None
            self.s_zoom = self.s_zoom_selector.value
            self.s_tile_size = EDITOR_SIZE // self.s_zoom
        self.s_grid_selector.update()
        self.s_grid_size = self.s_grid_selector.value

        #? Color Buttons
        for color_button in self.s_color_buttons:
            c = color_button.update(self.s_color)
            self.s_color = c if c is not None else self.s_color

        #? Tool Buttons
        for tool_button in self.tool_buttons:
            c = tool_button.update(self.current_tool)
            self.current_tool = c if c is not None else self.current_tool

    def draw_sprite_editor(self):
        pyxel.cls(0)

        #? Borders
        pyxel.rect(0, 0, 258, 16, self.COLORS_LEN)
        pyxel.rect(0, 16, 25, 128, self.COLORS_LEN)
        pyxel.rect(0, 144, 258, 16, self.COLORS_LEN)
        pyxel.rect(153, 16, 105, 128, self.COLORS_LEN)

        #? Selectors
        self.s_image_selector.draw()
        self.s_zoom_selector.draw()
        self.s_grid_selector.draw()
        pyxel.text(169, 140, f"Grid:On", self.COLORS_LEN + 1) if self.s_grid else pyxel.text(169, 140, f"Grid:Off", self.COLORS_LEN + 2)

        #? Color Buttons
        for color_button in self.s_color_buttons:
            color_button.draw()

        #? Tool Buttons
        for tool_button in self.tool_buttons:
            tool_button.draw()

        #? Editor
        for y in range(self.s_zoom):
            for x in range(self.s_zoom):
                c = pyxel.images[self.s_image].pget(self.s_offset_x + x, self.s_offset_y + y)
                pyxel.rect(EDITOR_X + x * self.s_tile_size, EDITOR_Y + y * self.s_tile_size, self.s_tile_size, self.s_tile_size, c)

        #? Grid
        if self.s_grid:
            for y in range(16, 144, self.s_grid_size * self.s_tile_size):
                pyxel.rect(25, y - 1, 128, 1, self.COLORS_LEN)
            for x in range(25, 153, self.s_grid_size * self.s_tile_size):
                pyxel.rect(x - 1, 16, 1, 128, self.COLORS_LEN)

        #? Preview
        if self.s_selection and self.current_tool == SELECT_TOOL:
            x0, y0, x1, y1 = self.s_selection
            min_x, max_x = min(x0, x1), max(x0, x1)
            min_y, max_y = min(y0, y1), max(y0, y1)

            pyxel.rectb(EDITOR_X + min_x * self.s_tile_size, EDITOR_Y + min_y * self.s_tile_size, (max_x - min_x + 1) * self.s_tile_size, (max_y - min_y + 1) * self.s_tile_size, self.COLORS_LEN + 1)

        if collision_point_rect(pyxel.mouse_x, pyxel.mouse_y, EDITOR_X, EDITOR_Y, EDITOR_SIZE, EDITOR_SIZE):
            mx = (pyxel.mouse_x - EDITOR_X) // self.s_tile_size + self.s_offset_x
            my = (pyxel.mouse_y - EDITOR_Y) // self.s_tile_size + self.s_offset_y
            pixels = set()

            pyxel.text(25, 8, f"({mx},{my})", self.COLORS_LEN + 1)

            if self.current_tool == BUCKET_TOOL:
                pixels = self.flood_fill_sprite(mx, my, pyxel.images[self.s_image].pget(mx, my), self.s_color)
            elif self.current_tool == SWAP_TOOL:
                pixels = self.swap_fill_sprite(pyxel.images[self.s_image].pget(mx, my), self.s_color)

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

    #? ---------- TILEMAP EDITOR ---------- ?#

    def push_tilemap_history(self):
        snapshot = [[pyxel.tilemaps[self.t_tilemap].pget(x, y) for x in range(256)] for y in range(256)]
        self.t_history.append((self.t_tilemap, snapshot))
        if len(self.t_history) > 40:
            self.t_history.pop(0)

    def undo_tilemap(self):
        if self.t_history:
            tilemap, snapshot = self.t_history.pop()
            for y in range(256):
                for x in range(256):
                    pyxel.tilemaps[tilemap].pset(x, y, snapshot[y][x])

    def flood_fill_tilemap(self, x:int, y:int, old_tile:tuple, new_tile:tuple):
        if old_tile == new_tile:
            return set()

        pixels = set()
        x0, y0 = self.t_tilemap_offset_x, self.t_tilemap_offset_y
        x1, y1 = self.t_tilemap_offset_x + 16, self.t_tilemap_offset_y + 16

        stack = [(x, y)]
        while stack:
            cx, cy = stack.pop()
            if (x0 <= cx < x1 and y0 <= cy < y1 and pyxel.tilemaps[self.t_tilemap].pget(cx, cy) == old_tile) and (cx, cy) not in pixels:
                pixels.add((cx, cy))
                stack.extend([(cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)])
        return pixels

    def swap_fill_tilemap(self, old_tile:tuple, new_tile:tuple):
        if old_tile == new_tile:
            return set()
    
        pixels = set()
        x0, y0 = self.t_tilemap_offset_x, self.t_tilemap_offset_y
        x1, y1 = self.t_tilemap_offset_x + 16, self.t_tilemap_offset_y + 16

        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if pyxel.tilemaps[self.t_tilemap].pget(x, y) == old_tile:
                    pixels.add((x, y))
        return pixels

    def commit_tiles(self, tiles:set):
        x0, y0 = self.t_tilemap_offset_x, self.t_tilemap_offset_y
        x1, y1 = self.t_tilemap_offset_x + 16 - 1, self.t_tilemap_offset_y + 16 - 1
        tx, ty = (self.t_tile_selected[0] + self.t_tile_offset_x // 8, self.t_tile_selected[1] + self.t_tile_offset_y // 8)
        for (x, y) in tiles:
            if x0 <= x <= x1 and y0 <= y <= y1:
                pyxel.tilemaps[self.t_tilemap].pset(x, y, (tx, ty))

    def draw_preview_tiles(self, tiles:set):
        tx, ty = (self.t_tile_selected[0] + self.t_tile_offset_x // 8, self.t_tile_selected[1] + self.t_tile_offset_y // 8)
        for (x, y) in tiles:
            if x < self.t_tilemap_offset_x or x >= self.t_tilemap_offset_x + 16 or y < self.t_tilemap_offset_y or y >= self.t_tilemap_offset_y + 16:
                continue
            sx = EDITOR_X + (x - self.t_tilemap_offset_x) * TILEMAP_TILE_SIZE
            sy = EDITOR_Y + (y - self.t_tilemap_offset_y) * TILEMAP_TILE_SIZE
            pyxel.blt(sx, sy, self.t_image, tx * 8, ty * 8, TILEMAP_TILE_SIZE, TILEMAP_TILE_SIZE)

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
                tile = pyxel.tilemaps[self.t_tilemap].pget(abs_x, abs_y)
                self.t_clipboard.append((x - min_x, y - min_y, tile))

    def cut_tilemap(self):
        if not self.t_selection or self.current_tool != SELECT_TOOL:
            return
        
        self.copy_tilemap()
        
        x0, y0, x1, y1 = self.t_selection
        min_x, min_y = min(x0, x1), min(y0, y1)
        max_x, max_y = max(x0, x1), max(y0, y1)
        
        self.push_tilemap_history()
        
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                abs_x = x + self.t_tilemap_offset_x
                abs_y = y + self.t_tilemap_offset_y
                pyxel.tilemaps[self.t_tilemap].pset(abs_x, abs_y, (0, 0))

    def paste_tilemap(self):
        if not self.t_clipboard or not self.t_selection or self.current_tool != SELECT_TOOL:
            return
        
        x0, y0, x1, y1 = self.t_selection
        min_x, min_y = min(x0, x1), min(y0, y1)
        
        self.push_tilemap_history()
        
        for rel_x, rel_y, tile in self.t_clipboard:
            abs_x = min_x + rel_x + self.t_tilemap_offset_x
            abs_y = min_y + rel_y + self.t_tilemap_offset_y
            
            if 0 <= abs_x < 256 and 0 <= abs_y < 256:
                pyxel.tilemaps[self.t_tilemap].pset(abs_x, abs_y, tile)

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
                row.append(pyxel.tilemaps[self.t_tilemap].pget(abs_x, abs_y))
            temp_buffer.append(row)
        
        self.push_tilemap_history()
        
        for y in range(height):
            for x in range(width):
                new_x = min_x + y
                new_y = min_y + (width - 1 - x)
                
                if new_x <= max_x and new_y <= max_y:
                    abs_x = new_x + self.t_tilemap_offset_x
                    abs_y = new_y + self.t_tilemap_offset_y
                    if 0 <= abs_x < 256 and 0 <= abs_y < 256:
                        pyxel.tilemaps[self.t_tilemap].pset(abs_x, abs_y, temp_buffer[y][x])

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
                row.append(pyxel.tilemaps[self.t_tilemap].pget(abs_x, abs_y))
            temp_buffer.append(row)
        
        self.push_tilemap_history()

        for y in range(max_y - min_y + 1):
            for x in range(width):
                new_x = min_x + (width - 1 - x)
                abs_x = new_x + self.t_tilemap_offset_x
                abs_y = (min_y + y) + self.t_tilemap_offset_y
                if 0 <= abs_x < 256 and 0 <= abs_y < 256:
                    pyxel.tilemaps[self.t_tilemap].pset(abs_x, abs_y, temp_buffer[y][x])

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
                row.append(pyxel.tilemaps[self.t_tilemap].pget(abs_x, abs_y))
            temp_buffer.append(row)
        
        self.push_tilemap_history()
        
        for y in range(height):
            for x in range(max_x - min_x + 1):
                new_y = min_y + (height - 1 - y)
                abs_x = (min_x + x) + self.t_tilemap_offset_x
                abs_y = new_y + self.t_tilemap_offset_y
                if 0 <= abs_x < 256 and 0 <= abs_y < 256:
                    pyxel.tilemaps[self.t_tilemap].pset(abs_x, abs_y, temp_buffer[y][x])

    def update_tilemap_editor(self):
        #? Shortcuts
        if pyxel.btn(pyxel.KEY_CTRL) or pyxel.btn(pyxel.KEY_GUI):
            if pyxel.btnp(pyxel.KEY_Z):
                self.undo_tilemap()
            elif pyxel.btnp(pyxel.KEY_C):
                self.copy_tilemap()
            elif pyxel.btnp(pyxel.KEY_X):
                self.cut_tilemap()
            elif pyxel.btnp(pyxel.KEY_V):
                self.paste_tilemap()
            elif pyxel.btnp(pyxel.KEY_T):
                self.place_tiles()

        if pyxel.btnp(pyxel.KEY_R):
            self.rotate_tilemap_selection()
        if pyxel.btnp(pyxel.KEY_H):
            self.flip_tilemap_selection_horizontal()
        if pyxel.btnp(pyxel.KEY_V) and not (pyxel.btn(pyxel.KEY_CTRL) or pyxel.btn(pyxel.KEY_GUI)):
            self.flip_tilemap_selection_vertical()  

        if pyxel.btnp(pyxel.KEY_G): self.t_grid = not self.t_grid

        for key in TOOLS_SHORTCUTS.keys():
            if pyxel.btnp(key):
                self.current_tool = TOOLS_SHORTCUTS[key]

        #? Editor
        if collision_point_rect(pyxel.mouse_x, pyxel.mouse_y, EDITOR_X, EDITOR_Y, EDITOR_SIZE, EDITOR_SIZE):
            mx = (pyxel.mouse_x - EDITOR_X) // TILEMAP_TILE_SIZE + self.t_tilemap_offset_x 
            my = (pyxel.mouse_y - EDITOR_Y) // TILEMAP_TILE_SIZE + self.t_tilemap_offset_y 
            tx, ty = (self.t_tile_selected[0] + self.t_tile_offset_x // 8, self.t_tile_selected[1] + self.t_tile_offset_y // 8)

            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.push_tilemap_history()

                if self.current_tool in [FILLED_RECT_TOOL, RECT_TOOL, FILLED_ELLI_TOOL, ELLI_TOOL, LINE_TOOL]:
                    self.t_drag_start = (mx, my)
                if self.current_tool == BUCKET_TOOL:
                    self.commit_tiles(self.flood_fill_tilemap(mx, my, pyxel.tilemaps[self.t_tilemap].pget(mx, my), (tx, ty)))
                elif self.current_tool == SWAP_TOOL:
                    self.commit_tiles(self.swap_fill_tilemap(pyxel.tilemaps[self.t_tilemap].pget(mx, my), (tx, ty)))
                elif self.current_tool == SELECT_TOOL:
                    x = (pyxel.mouse_x - EDITOR_X) // TILEMAP_TILE_SIZE
                    y = (pyxel.mouse_y - EDITOR_Y) // TILEMAP_TILE_SIZE
                    self.t_selection = [x, y, x, y]

            if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
                if self.current_tool == PEN_TOOL:
                    pyxel.tilemaps[self.t_tilemap].pset(mx, my, (tx, ty))
                elif self.current_tool == MIRROR_TOOL:
                    pyxel.tilemaps[self.t_tilemap].pset(mx, my, (tx, ty))
                    axis_x = self.t_tilemap_offset_x + 8
                    mx_mirror = axis_x - (mx - axis_x) - 1
                    if 0 <= mx_mirror < 256:
                        pyxel.tilemaps[self.t_tilemap].pset(mx_mirror, my, (tx, ty))
                elif self.current_tool == SELECT_TOOL:
                    x = (pyxel.mouse_x - EDITOR_X) // TILEMAP_TILE_SIZE
                    y = (pyxel.mouse_y - EDITOR_Y) // TILEMAP_TILE_SIZE
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

        #? Tiles Picker
        if collision_point_rect(pyxel.mouse_x, pyxel.mouse_y, 169, 80, 64, 64):
            mx = (pyxel.mouse_x - 169) // 8
            my = (pyxel.mouse_y - 80) // 8

            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.t_tile_selected = (mx, my)

        #? Movement
        if pyxel.btn(pyxel.KEY_LSHIFT):
            if pyxel.btnp(pyxel.KEY_RIGHT, repeat=10):
                self.t_tile_offset_x += 8
            if pyxel.btnp(pyxel.KEY_LEFT, repeat=10):
                self.t_tile_offset_x -= 8
            if pyxel.btnp(pyxel.KEY_DOWN, repeat=10):
                self.t_tile_offset_y += 8
            if pyxel.btnp(pyxel.KEY_UP, repeat=10):
                self.t_tile_offset_y -= 8
        else:
            if pyxel.btnp(pyxel.KEY_RIGHT, repeat=10):
                self.t_tilemap_offset_x += 8
            if pyxel.btnp(pyxel.KEY_LEFT, repeat=10):
                self.t_tilemap_offset_x -= 8
            if pyxel.btnp(pyxel.KEY_DOWN, repeat=10):
                self.t_tilemap_offset_y += 8
            if pyxel.btnp(pyxel.KEY_UP, repeat=10):
                self.t_tilemap_offset_y -= 8
        self.t_tilemap_offset_x = max(0, min(256 - 16, self.t_tilemap_offset_x))
        self.t_tilemap_offset_y = max(0, min(256 - 16, self.t_tilemap_offset_y))
        self.t_tile_offset_x = max(0, min(256 - 64, self.t_tile_offset_x))
        self.t_tile_offset_y = max(0, min(256 - 64, self.t_tile_offset_y))

        #? Selectors
        self.t_tilemap_selector.update()
        if self.t_tilemap != self.t_tilemap_selector.value:
            self.t_tilemap = self.t_tilemap_selector.value
            imgsrc = pyxel.tilemaps[self.t_tilemap].imgsrc
            self.t_image = imgsrc if isinstance(imgsrc, int) else pyxel.images.to_list().index(imgsrc)
            self.t_image_selector.value = self.t_image
        self.t_image_selector.update()
        if self.t_image != self.t_image_selector.value:
            self.t_image = self.t_image_selector.value
            pyxel.tilemaps[self.t_tilemap].imgsrc = self.t_image
        self.t_layer_selector.update()
        self.t_layer = self.t_layer_selector.value
        self.t_grid_selector.update()
        self.t_grid_size = self.t_grid_selector.value

        #? Tool Buttons
        for tool_button in self.tool_buttons:
            c = tool_button.update(self.current_tool)
            self.current_tool = c if c is not None else self.current_tool

    def draw_tilemap_editor(self):
        pyxel.cls(0)

        #? Borders
        pyxel.rect(0, 0, 258, 16, self.COLORS_LEN)
        pyxel.rect(0, 16, 25, 128, self.COLORS_LEN)
        pyxel.rect(0, 144, 258, 16, self.COLORS_LEN)
        pyxel.rect(153, 16, 105, 128, self.COLORS_LEN)

        #? Selectors
        self.t_tilemap_selector.draw()
        self.t_image_selector.draw()
        self.t_layer_selector.draw()
        self.t_grid_selector.draw()

        #? Tool Buttons
        for tool_button in self.tool_buttons:
            tool_button.draw()

        #? Editor
        if self.t_layer != "None":
            pyxel.bltm(EDITOR_X, EDITOR_Y, self.t_layer, self.t_tilemap_offset_x * 8, self.t_tilemap_offset_y * 8, EDITOR_SIZE, EDITOR_SIZE)
            pyxel.bltm(EDITOR_X, EDITOR_Y, self.t_tilemap, self.t_tilemap_offset_x * 8, self.t_tilemap_offset_y * 8, EDITOR_SIZE, EDITOR_SIZE, 0)
        else:
            pyxel.bltm(EDITOR_X, EDITOR_Y, self.t_tilemap, self.t_tilemap_offset_x * 8, self.t_tilemap_offset_y * 8, EDITOR_SIZE, EDITOR_SIZE)

        #? Grid
        if self.t_grid:
            for y in range(16, 144, self.t_grid_size * TILEMAP_TILE_SIZE):
                pyxel.rect(25, y - 1, 128, 1, self.COLORS_LEN)
            for x in range(25, 153, self.t_grid_size * TILEMAP_TILE_SIZE):
                pyxel.rect(x - 1, 16, 1, 128, self.COLORS_LEN)

        #? Preview
        if self.t_selection and self.current_tool == SELECT_TOOL:
            x0, y0, x1, y1 = self.t_selection
            min_x, max_x = min(x0, x1), max(x0, x1)
            min_y, max_y = min(y0, y1), max(y0, y1)

            pyxel.rectb(EDITOR_X + min_x * TILEMAP_TILE_SIZE, EDITOR_Y + min_y * TILEMAP_TILE_SIZE, (max_x - min_x + 1) * TILEMAP_TILE_SIZE, (max_y - min_y + 1) * TILEMAP_TILE_SIZE, self.COLORS_LEN + 1)

        if collision_point_rect(pyxel.mouse_x, pyxel.mouse_y, EDITOR_X, EDITOR_Y, EDITOR_SIZE, EDITOR_SIZE):
            mx = (pyxel.mouse_x - EDITOR_X) // TILEMAP_TILE_SIZE + self.t_tilemap_offset_x
            my = (pyxel.mouse_y - EDITOR_Y) // TILEMAP_TILE_SIZE + self.t_tilemap_offset_y
            tx, ty = (self.t_tile_selected[0] + self.t_tile_offset_x // 8, self.t_tile_selected[1] + self.t_tile_offset_y // 8)
            tiles = set()

            pyxel.text(25, 8, f"({mx},{my})", self.COLORS_LEN + 1)

            if self.current_tool == BUCKET_TOOL:
                tiles = self.flood_fill_tilemap(mx, my, pyxel.tilemaps[self.t_tilemap].pget(mx, my), (tx, ty))
            elif self.current_tool == SWAP_TOOL:
                tiles = self.swap_fill_tilemap(pyxel.tilemaps[self.t_tilemap].pget(mx, my), (tx, ty))

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

        #? Tiles Picker
        pyxel.blt(169, 80, self.t_image, self.t_tile_offset_x, self.t_tile_offset_y, 64, 64)
        pyxel.rectb(169 + self.t_tile_selected[0] * 8, 80 + self.t_tile_selected[1] * 8, 8, 8, self.COLORS_LEN + 1)
        if collision_point_rect(pyxel.mouse_x, pyxel.mouse_y, 169, 80, 64, 64):
            tx = (pyxel.mouse_x - 169) // 8 + self.t_tile_offset_x // 8
            ty = (pyxel.mouse_y - 80) // 8 + self.t_tile_offset_y // 8
            pyxel.text(169, 72, f"({tx},{ty})", self.COLORS_LEN + 1)

    #? ---------- AUTOTILE EDITOR ---------- ?#

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
        for button in eval(f"self.a_buttons_{self.a_image}"):
            button.update()

        exec(f"self.a_tiles_y_{self.a_image} = [b.id for b in self.a_buttons_{self.a_image} if b.selected]")

        #? Selectors
        self.a_image_selector.update()
        self.a_image = self.a_image_selector.value

    def draw_autotile_editor(self):
        pyxel.cls(self.COLORS_LEN)

        #? Selectors
        self.a_image_selector.draw()

        #? Buttons
        for button in eval(f"self.a_buttons_{self.a_image}"):
            button.draw()

        #? Tilesets
        x, y = 0, 0
        for i in range(len(eval(f"self.a_tiles_y_{self.a_image}"))):
            self.draw_tileset(25 + x, 22 + y, self.a_image, eval(f"self.a_tiles_y_{self.a_image}[{i}]"))
            x = (x + 46) % 230
            if x == 0:
                y += 36

    #? ---------- ANIMATION EDITOR ---------- ?#

    def update_animation_editor(self):
        #? Entries
        self.n_start_uv_entry.update()
        self.n_sprite_wh_entry.update()
        self.n_colkey_entry.update()
        self.n_frames_entry.update()
        self.n_speed_entry.update()

        #? Selectors
        self.n_image_selector.update()

        #? Buttons
        if self.n_play_button.update(5) is not None:
            self.n_is_playing = not self.n_is_playing
        
        if self.n_prev_button.update(5) is not None:
            if self.n_frame > 0:
                self.n_frame -= 1
                self.n_is_playing = False
        
        if self.n_next_button.update(5) is not None:
            try:
                total_frames = int(self.n_frames_entry.value)
                if self.n_frame < total_frames - 1:
                    self.n_frame += 1
                    self.n_is_playing = False
            except:
                pass

        #? Retrieving
        u = v = w = h = c = t = s = None

        try:
            u, v = map(int, self.n_start_uv_entry.value.split(","))
            w, h = map(int, self.n_sprite_wh_entry.value.split(","))
            c = int(self.n_colkey_entry.value)
            t = int(self.n_frames_entry.value)
            s = int(self.n_speed_entry.value)
            
            if self.n_is_playing and t > 0:
                self.n_frame_timer += 1
                if self.n_frame_timer >= s:
                    self.n_frame_timer = 0
                    self.n_frame = (self.n_frame + 1) % t
            
        except:
            pass

        self.n_animation = (u, v, w, h, c, t, s)

    def draw_animation_editor(self):
        pyxel.cls(self.COLORS_LEN)

        #? Entries
        self.n_start_uv_entry.draw()
        self.n_sprite_wh_entry.draw()
        self.n_colkey_entry.draw()
        self.n_frames_entry.draw()
        self.n_speed_entry.draw()

        #? Selectors
        self.n_image_selector.draw()

        #? Buttons
        self.n_prev_button.draw()
        self.n_play_button.draw()
        self.n_next_button.draw()

        #? Draw current frame
        u, v, w, h, c, t, s = self.n_animation
        if all(x is not None for x in [u, v, w, h, t, s]) and t > 0:
            frame_u = u + (self.n_frame * w)
            
            scale_x = EDITOR_SIZE / w
            scale_y = EDITOR_SIZE / h
            scale = min(scale_x, scale_y)
            
            scaled_w = int(w * scale)
            scaled_h = int(h * scale)
            
            center_x = EDITOR_X + (EDITOR_SIZE - scaled_w) // 2
            center_y = EDITOR_Y + (EDITOR_SIZE - scaled_h) // 2
            
            for py in range(h):
                for px in range(w):
                    pixel_color = pyxel.images[self.n_image_selector.value].pget(frame_u + px, v + py)
                    if pixel_color != c:
                        draw_x = center_x + int(px * scale)
                        draw_y = center_y + int(py * scale)
                        pyxel.rect(draw_x, draw_y, int(scale), int(scale), pixel_color)
            
            frame_text = f"Frame: {self.n_frame + 1}/{t}"
            pyxel.text(EDITOR_X + 2, 148, frame_text, self.COLORS_LEN + 1)

    #? ---------- MAIN ---------- ?#
    
    def update(self):
        if (pyxel.btn(pyxel.KEY_CTRL) or pyxel.btn(pyxel.KEY_GUI)) and pyxel.btnp(pyxel.KEY_S):
            pyxel.save(self.PYXRES_PATH)

        for editor_button in self.editor_buttons:
            c = editor_button.update(self.current_editor)
            self.current_editor = c if c is not None else self.current_editor

        if self.current_editor == SPRITE_EDITOR:       self.update_sprite_editor()
        elif self.current_editor == TILEMAP_EDITOR:    self.update_tilemap_editor()
        elif self.current_editor == AUTOTILE_EDITOR:   self.update_autotile_editor()
        elif self.current_editor == ANIMATION_EDITOR:  self.update_animation_editor()

    def draw(self):
        if self.current_editor == SPRITE_EDITOR:       self.draw_sprite_editor()
        elif self.current_editor == TILEMAP_EDITOR:    self.draw_tilemap_editor()
        elif self.current_editor == AUTOTILE_EDITOR:   self.draw_autotile_editor()
        elif self.current_editor == ANIMATION_EDITOR:  self.draw_animation_editor()

        for editor_button in self.editor_buttons:
            editor_button.draw()

if __name__ == "__main__":
    EXTENDED_PICO8_COLORS = [0x000000, 0x1D2B53, 0x7E2553, 0x008751, 0xAB5236, 0x5F574F, 0xC2C3C7, 0xFFF1E8, 0xFF004D, 0xFFA300, 0xFFEC27, 0x00E436, 0x29ADFF, 0x83769C, 0xFF77A8, 0xFFCCAA, 0x1A1C2C, 0x5D275D, 0x008080, 0x1B6535, 0x73464D, 0x9D9D9D, 0xFFFFFF, 0xFF6C24, 0xFFD93F, 0xB2D732, 0x3CA370, 0x0066CC, 0x45283C, 0xA288AE, 0xF3B4B4, 0xD4A373]
    Editor("assets_rooms.pyxres", EXTENDED_PICO8_COLORS)