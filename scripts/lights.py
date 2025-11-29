"""
@author : Léo Imbert
@created : 15/10/2024
@updated : 29/11/2025
"""

from collisions import collision_rect_rect
import random
import pyxel

#? -------------------- LIGHTS -------------------- ?#

class TriangleLight:

    def __init__(self, x1:int, y1:int, x2:int, y2:int, x3:int, y3:int, lights_substitution_colors:dict, turn_time:int=30, turn_on_chance:float=1, turn_off_chance:float=0):
        self.__vertices = [(x1, y1), (x2, y2), (x3, y3)]
        self.lights_substitution_colors = lights_substitution_colors
        self.__points = self.__generate_points_list()
        self.on = True
        self.turn_on_chance = turn_on_chance
        self.turn_off_chance = turn_off_chance
        self.__start_frame = pyxel.frame_count
        self.turn_time = turn_time

    def __is_point_in_triangle(self, px:int, py:int)-> bool:
        (x1, y1), (x2, y2), (x3, y3) = self.__vertices

        def triangle_area(x1, y1, x2, y2, x3, y3):
            return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)
        
        total_area = triangle_area(x1, y1, x2, y2, x3, y3)

        a1 = triangle_area(px, py, x2, y2, x3, y3)
        a2 = triangle_area(x1, y1, px, py, x3, y3)
        a3 = triangle_area(x1, y1, x2, y2, px, py)

        return abs(total_area - (a1 + a2 + a3)) < 1e-6

    def __generate_points_list(self)-> list:
        (x1, y1), (x2, y2), (x3, y3) = self.__vertices
        
        min_x = min(x1, x2, x3)
        max_x = max(x1, x2, x3)
        min_y = min(y1, y2, y3)
        max_y = max(y1, y2, y3)

        return [(x, y) for x in range(min_x, max_x + 1) for y in range(min_y, max_y + 1) if self.__is_point_in_triangle(x, y)]

    def draw(self, camera_x:int=0, camera_y:int=0):
        if pyxel.frame_count - self.__start_frame >= self.turn_time:
            self.__start_frame = pyxel.frame_count

            if self.on and random.random() <= self.turn_off_chance:
                self.on = False
            elif not self.on and random.random() <= self.turn_on_chance:
                self.on = True

        if not self.on:
            return
        
        (x1, y1), (x2, y2), (x3, y3) = self.__vertices
        min_x = min(x1, x2, x3)
        min_y = min(y1, y2, y3)
        w = max(x1, x2, x3) - min_x
        h = max(y1, y2, y3) - min_y
        if not collision_rect_rect(camera_x, camera_y, pyxel.width, pyxel.height, min_x, min_y, w, h):
            return
        
        for x, y in self.__points:
            screen_x = x - camera_x
            screen_y = y - camera_y
            if 0 <= screen_x < pyxel.width and 0 <= screen_y < pyxel.height:
                pyxel.pset(x, y, self.lights_substitution_colors.get(pyxel.pget(screen_x, screen_y), 0))

class CircleLight:

    def __init__(self, x:int, y:int, radius:int, lights_substitution_colors:dict, turn_time:int=30, turn_on_chance:float=1, turn_off_chance:float=0):
        self.x = x
        self.y = y
        self.__radius = radius
        self.lights_substitution_colors = lights_substitution_colors
        self.__points = self.__generate_points_list()
        self.on = True
        self.turn_on_chance = turn_on_chance
        self.turn_off_chance = turn_off_chance
        self.__start_frame = pyxel.frame_count
        self.turn_time = turn_time

    def __generate_points_list(self)-> list:
        return [(x, y) for x in range(-self.__radius, self.__radius + 1) for y in range(-self.__radius, self.__radius + 1) if x ** 2 + y ** 2 <= self.__radius ** 2]

    def draw(self, camera_x:int=0, camera_y:int=0):
        if pyxel.frame_count - self.__start_frame >= self.turn_time:
            self.__start_frame = pyxel.frame_count

            if self.on and random.random() <= self.turn_off_chance:
                self.on = False
            elif not self.on and random.random() <= self.turn_on_chance:
                self.on = True

        if not self.on:
            return
        
        min_x = self.x - self.__radius
        min_y = self.y - self.__radius
        r = 2 * self.__radius
        if not collision_rect_rect(camera_x, camera_y, pyxel.width, pyxel.height, min_x, min_y, r, r):
            return
        
        for x, y in self.__points:
            screen_x = self.x + x - camera_x
            screen_y = self.y + y - camera_y
            if 0 <= screen_x < pyxel.width and 0 <= screen_y < pyxel.height:
                pyxel.pset(self.x + x, self.y + y, self.lights_substitution_colors.get(pyxel.pget(screen_x, screen_y), 0))

class QuadrilateralLight:

    def __init__(self, x1:int, y1:int, x2:int, y2:int, x3:int, y3:int, x4:int, y4:int, lights_substitution_colors:dict, turn_time:int=30, turn_on_chance:float=1, turn_off_chance:float=0):
        self.__vertices = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
        self.lights_substitution_colors = lights_substitution_colors
        self.__points = self.__generate_points_list()
        self.on = True
        self.turn_on_chance = turn_on_chance
        self.turn_off_chance = turn_off_chance
        self.__start_frame = pyxel.frame_count
        self.turn_time = turn_time

    def __is_point_in_triangle(self, px:int, py:int, v1:tuple, v2:tuple, v3:tuple)-> bool:
        def area(x1, y1, x2, y2, x3, y3):
            return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)

        a = area(*v1, *v2, *v3)
        a1 = area(px, py, *v2, *v3)
        a2 = area(*v1, px, py, *v3)
        a3 = area(*v1, *v2, px, py)
        return abs(a - (a1 + a2 + a3)) < 1e-2

    def __is_point_in_quad(self, px:int, py:int)-> bool:
        v1, v2, v3, v4 = self.__vertices
        return (self.__is_point_in_triangle(px, py, v1, v2, v3) or self.__is_point_in_triangle(px, py, v1, v3, v4))

    def __generate_points_list(self)-> list:
        xs = [v[0] for v in self.__vertices]
        ys = [v[1] for v in self.__vertices]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        points = []
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                if self.__is_point_in_quad(x, y):
                    points.append((x, y))
        return points

    def draw(self, camera_x:int=0, camera_y:int=0):
        if pyxel.frame_count - self.__start_frame >= self.turn_time:
            self._start_frame = pyxel.frame_count
            if self.on and random.random() <= self.turn_off_chance:
                self.on = False
            elif not self.on and random.random() <= self.turn_on_chance:
                self.on = True

        if not self.on:
            return
        
        xs = [v[0] for v in self.__vertices]
        ys = [v[1] for v in self.__vertices]
        min_x = min(xs)
        min_y = min(ys)
        w = max(xs) - min_x
        h = max(ys) - min_y
        if not collision_rect_rect(camera_x, camera_y, pyxel.width, pyxel.height, min_x, min_y, w, h):
            return

        for x, y in self.__points:
            screen_x = x - camera_x
            screen_y = y - camera_y
            if 0 <= screen_x < pyxel.width and 0 <= screen_y < pyxel.height:
                pyxel.pset(x, y, self.lights_substitution_colors.get(pyxel.pget(screen_x, screen_y), 0))

class LightManager:

    def __init__(self):
        self.__lights = []

    def reset(self):
        self.__lights = []

    def add_light(self, light:TriangleLight|CircleLight|QuadrilateralLight):
        self.__lights.append(light)

    def remove_light(self, light:TriangleLight|CircleLight|QuadrilateralLight):
        self.__lights.remove(light)

    def draw(self, camera_x:int=0, camera_y:int=0):
        for light in self.__lights:
            light.draw(camera_x, camera_y)

