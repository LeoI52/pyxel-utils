"""
@author : Léo Imbert
@created : 07/11/2025
@updated : 07/11/2025
"""

import random
import pyxel

def place_random_tiles(o_tiles:list, o_tilemap:int, chance:int, tiles:list, tilemap:int, offset_x:int=0, offset_y:int=0):
    for y in range(pyxel.tilemaps[o_tilemap].height):
        for x in range(pyxel.tilemaps[o_tilemap].width):
            if pyxel.tilemaps[o_tilemap].pget(x, y) in o_tiles:
                if random.random() < chance:
                    pyxel.tilemaps[tilemap].pset(x + offset_x, y + offset_y, random.choice(tiles))

if __name__ == "__main__":
    pass