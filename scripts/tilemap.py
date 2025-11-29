"""
@author : Léo Imbert
@created : 07/11/2025
@updated : 29/11/2025
"""

from other import clamp
import random
import pyxel

#? -------------------- TILEMAP CLASS -------------------- ?#

class Tilemap:

    def __init__(self, id:int, x:int, y:int, w:int, h:int, colkey:int=None):
        self.id = id
        self.x = x
        self.y = y
        self.w, self.h = w, h
        self.colkey = colkey

    def collision_rect_tiles(self, x:int, y:int, w:int, h:int, tiles:list)-> bool:
        start_tile_x = (x - self.x) // 8
        start_tile_y = (y - self.y) // 8
        end_tile_x = (x + w - self.x - 1) // 8
        end_tile_y = (y + h - self.y - 1) // 8

        start_tile_x = clamp(start_tile_x, 0, self.w // 8 - 1)
        start_tile_y = clamp(start_tile_y, 0, self.h // 8 - 1)
        end_tile_x = clamp(end_tile_x, 0, self.w // 8 - 1)
        end_tile_y = clamp(end_tile_y, 0, self.h // 8 - 1)

        for tile_y in range(int(start_tile_y), int(end_tile_y) + 1):
            for tile_x in range(int(start_tile_x), int(end_tile_x) + 1):
                tile_id = pyxel.tilemaps[self.id].pget(tile_x, tile_y)

                if tile_id in tiles:
                    return True
        
        return False
    
    def tiles_in_rect(self, x:int, y:int, w:int, h:int, tiles:list):
        result = []

        start_tile_x = (x - self.x) // 8
        start_tile_y = (y - self.y) // 8
        end_tile_x = (x + w - self.x - 1) // 8
        end_tile_y = (y + h - self.y - 1) // 8

        start_tile_x = clamp(start_tile_x, 0, self.w // 8 - 1)
        start_tile_y = clamp(start_tile_y, 0, self.h // 8 - 1)
        end_tile_x = clamp(end_tile_x, 0, self.w // 8 - 1)
        end_tile_y = clamp(end_tile_y, 0, self.h // 8 - 1)

        for tile_y in range(int(start_tile_y), int(end_tile_y) + 1):
            for tile_x in range(int(start_tile_x), int(end_tile_x) + 1):
                tile_id = pyxel.tilemaps[self.id].pget(tile_x, tile_y)
                if tile_id in tiles:
                    result.append((int(tile_x), int(tile_y)))

        return result

    def replace_tiles(self, x:int, y:int, width:int, height:int, radius:int, tiles:list, replace_tile:tuple):
        start_tile_x = (x - radius - self.x) // 8
        start_tile_y = (y - radius - self.y) // 8
        end_tile_x = (x + width + radius - self.x - 1) // 8
        end_tile_y = (y + height + radius - self.y - 1) // 8

        start_tile_x = clamp(start_tile_x, 0, self.w // 8 - 1)
        start_tile_y = clamp(start_tile_y, 0, self.h // 8 - 1)
        end_tile_x = clamp(end_tile_x, 0, self.w // 8 - 1)
        end_tile_y = clamp(end_tile_y, 0, self.h // 8 - 1)

        for tile_y in range(int(start_tile_y), int(end_tile_y) + 1):
            for tile_x in range(int(start_tile_x), int(end_tile_x) + 1):
                tile_id = pyxel.tilemaps[self.id].pget(tile_x, tile_y)

                if tile_id in tiles:
                    pyxel.tilemaps[self.id].pset(tile_x, tile_y, replace_tile)

    def draw(self):
        pyxel.bltm(self.x, self.y, self.id, 0, 0, self.w, self.h, self.colkey)

#? -------------------- FUNCTIONS -------------------- ?#

def place_random_tiles(o_tiles:list, o_tilemap:int, percentage:float, tiles:list, tilemap:int, offset_x:int=0, offset_y:int=0, replacable_tiles:list=[(0,0)], seed:int=None):
    if seed:    random.seed(seed)

    src_tilemap = pyxel.tilemaps[o_tilemap]
    end_tilemap = pyxel.tilemaps[tilemap]

    for y in range(src_tilemap.height):
        for x in range(src_tilemap.width):
            if src_tilemap.pget(x, y) in o_tiles and random.random() < percentage:
                if 0 <= x + offset_x < end_tilemap.width and 0 <= y + offset_y < end_tilemap.height:

                    if (offset_x != 0 or offset_y != 0) and end_tilemap.pget(x + offset_x, y + offset_y) not in replacable_tiles:
                        continue

                    end_tilemap.pset(x + offset_x, y + offset_y, random.choice(tiles))

