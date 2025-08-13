"""
@author : Léo Imbert
@created : 15/10/2024
@updated : 13/08/2025
"""

from .vars import *
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

def get_anchored_position(x:int, y:int, w:int, h:int, anchor:int)-> tuple:
    if anchor in [ANCHOR_TOP_RIGHT, ANCHOR_BOTTOM_RIGHT, ANCHOR_RIGHT]:
        x -= w
    if anchor in [ANCHOR_BOTTOM_LEFT, ANCHOR_BOTTOM_RIGHT, ANCHOR_BOTTOM]:
        y -= h
    if anchor in [ANCHOR_TOP, ANCHOR_BOTTOM, ANCHOR_CENTER]:
        x -= w // 2
    if anchor in [ANCHOR_LEFT, ANCHOR_RIGHT, ANCHOR_CENTER]:
        y -= h // 2
        
    return x, y

def clamp(value:int|float, min_value:int|float, max_value:int|float)-> int|float:
    return max(min_value, min(value, max_value))
