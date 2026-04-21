"""
@author : Léo Imbert
@created : 15/10/2024
@updated : 21/04/2026
"""

#? -------------------- IMPORTATIONS -------------------- ?#

from vars import *

#? -------------------- POSITION -------------------- ?#

def get_anchored_position(x:int, y:int, width:int, height:int, anchor:int)-> tuple:
    if anchor in [TOP_RIGHT, BOTTOM_RIGHT, RIGHT]:
        x -= width
    if anchor in [BOTTOM_LEFT, BOTTOM_RIGHT, BOTTOM]:
        y -= height
    if anchor in [TOP, BOTTOM, CENTER]:
        x -= width // 2
    if anchor in [LEFT, RIGHT, CENTER]:
        y -= height // 2
        
    return x, y

def get_anchored_position_x(x:int, width:int, anchor:int)-> int:
    if anchor in [TOP_RIGHT, BOTTOM_RIGHT, RIGHT]:
        x -= width
    if anchor in [TOP, BOTTOM, CENTER]:
        x -= width // 2

    return x

def get_anchored_position_y(y:int, height:int, anchor:int)-> int:
    if anchor in [BOTTOM_LEFT, BOTTOM_RIGHT, BOTTOM]:
        y -= height
    if anchor in [LEFT, RIGHT, CENTER]:
        y -= height // 2

    return y
