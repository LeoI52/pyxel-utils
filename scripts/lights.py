"""
@author : Léo Imbert
@created : 15/10/2024
@updated : 17/08/2025
"""

import random
import pyxel

class CircleLight:

    def __init__(self, x:int, y:int, radius:int, lights_substitution_colors:dict, state_change_interval:int=30, turn_on_chance:float=1, turn_off_chance:float=0):
        self.x = x
        self.y = y
        self.__radius = radius
        self.__lights_substitution_colors = lights_substitution_colors
        self.__points = self.__generate_points_list()
        self.on = True
        self.turn_on_chance = turn_on_chance
        self.turn_off_chance = turn_off_chance
        self.__start_frame = pyxel.frame_count
        self.state_change_interval = state_change_interval

    def __generate_points_list(self)-> list:
        return [(x, y) for x in range(-self.__radius, self.__radius + 1) for y in range(-self.__radius, self.__radius + 1) if x ** 2 + y ** 2 <= self.__radius ** 2]

    def draw(self):
        if pyxel.frame_count - self.__start_frame >= self.state_change_interval:
            self.__start_frame = pyxel.frame_count

            if self.on and random.random() <= self.turn_off_chance:
                self.on = False
            elif not self.on and random.random() <= self.turn_on_chance:
                self.on = True

        if not self.on:
            return
        
        for x, y in self.__points:
            current_color = pyxel.pget(self.x + x, self.y + y)
            if current_color in self.__lights_substitution_colors:
                pyxel.pset(self.x + x, self.y + y, self.__lights_substitution_colors[current_color])