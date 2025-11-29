"""
@author : Léo Imbert
@created : 15/10/2024
@updated : 29/11/2025
"""

from vars import *
import json
import os

class SavingSystem:

    def __init__(self):
        self.__data = {}

    def add_data(self, key:str, value):
        self.__data[key] = value

    def get_data(self, key:str):
        return self.__data.get(key)
    
    def save(self, filename:str="save.json"):
        with open(filename, "w") as file:
            json.dump(self.__data, file, indent=4)

    def load(self, filename:str="save.json"):
        if os.path.isfile(filename):
            try:
                with open(filename, "r") as file:
                    self.__data = json.load(file)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Failed to load {filename}: {e}")

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