"""
@author : Léo Imbert
@created : 15/10/2024
@updated : 17/08/2025

TODO :
- Redo TriangleLight
- Redo QuadrilateralLight
- Optimize drawing
"""

import random
import pyxel

class TriangleLight:

    def __init__(self, x1:int, y1:int, x2:int, y2:int, x3:int, y3:int, lights_substitution_colors:dict, state_change_interval:int=30, turn_on_chance:float=1, turn_off_chance:float=0):
        self.__vertices = [(x1, y1), (x2, y2), (x3, y3)]
        self.__lights_substitution_colors = lights_substitution_colors
        self.__points = self.__generate_points_list()
        self.on = True
        self.turn_on_chance = turn_on_chance
        self.turn_off_chance = turn_off_chance
        self.__start_frame = pyxel.frame_count
        self.state_change_interval = state_change_interval

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

    def __is_on_screen(self, min_x:int, max_x:int, min_y:int, max_y:int, camera_x:int, camera_y:int)-> bool:
        return not (max_x < camera_x or min_x >= camera_x + pyxel.width or max_y < camera_y or min_y >= camera_y + pyxel.height)

    def draw(self, camera_x:int=0, camera_y:int=0):
        if pyxel.frame_count - self.__start_frame >= self.state_change_interval:
            self.__start_frame = pyxel.frame_count

            if self.on and random.random() <= self.turn_off_chance:
                self.on = False
            elif not self.on and random.random() <= self.turn_on_chance:
                self.on = True

        if not self.on:
            return

        (x1, y1), (x2, y2), (x3, y3) = self.__vertices

        min_x = min(x1, x2, x3)
        max_x = max(x1, x2, x3)
        min_y = min(y1, y2, y3)
        max_y = max(y1, y2, y3)

        if not self.__is_on_screen(min_x, max_x, min_y, max_y, camera_x, camera_y):
            return
        
        for x, y in self.__points:
            if camera_x <= x < camera_x + pyxel.width and camera_y <= y < camera_y + pyxel.height:
                current_color = pyxel.pget(x, y)
                if current_color in self.__lights_substitution_colors:
                    pyxel.pset(x, y, self.__lights_substitution_colors[current_color])

class CircleLight:

    def __init__(self, x:int, y:int, radius:int, lights_substitution_colors:dict, state_change_interval:int=30, turn_on_chance:float=1, turn_off_chance:float=0):
        self.x= x
        self.y = y
        self.__radius = radius
        self.__lights_substitution_colors = lights_substitution_colors
        self.__points = self.__generate_points_list()
        self.on = True
        self.turn_on_chance = turn_on_chance
        self.turn_off_chance = turn_off_chance
        self.__start_frame = pyxel.frame_count
        self.state_change_interval = state_change_interval

    @property
    def radius(self)-> int:
        return self.__radius
    
    @radius.setter
    def radius(self, value):
        self.__radius = value
        self.__points = self.__generate_points_list()

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

class QuadrilateralLight:

    def __init__(self, x1:int, y1:int, x2:int, y2:int, x3:int, y3:int, x4:int, y4:int, lights_substitution_colors:dict, state_change_interval:int=30, turn_on_chance:float=1, turn_off_chance:float=0):
        self.__vertices = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
        self.__lights_substitution_colors = lights_substitution_colors
        self.__points = self.__generate_points_list()
        self.on = True
        self.turn_on_chance = turn_on_chance
        self.turn_off_chance = turn_off_chance
        self.__start_frame = pyxel.frame_count
        self.state_change_interval = state_change_interval

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
        if pyxel.frame_count - self.__start_frame >= self.state_change_interval:
            self._start_frame = pyxel.frame_count
            if self.on and random.random() <= self.turn_off_chance:
                self.on = False
            elif not self.on and random.random() <= self.turn_on_chance:
                self.on = True

        if not self.on:
            return

        for x, y in self.__points:
            screen_x = x - camera_x
            screen_y = y - camera_y
            if 0 <= screen_x < pyxel.width and 0 <= screen_y < pyxel.height:
                current_color = pyxel.pget(x, y)
                if current_color in self.__lights_substitution_colors:
                    pyxel.pset(x, y, self.__lights_substitution_colors[current_color])

class LightManager:

    def __init__(self):
        self.__lights = []

    def reset(self):
        self.__lights = []

    def add_light(self, light:TriangleLight|CircleLight|QuadrilateralLight):
        self.__lights.append(light)

    def remove_light(self, light:TriangleLight|CircleLight|QuadrilateralLight):
        self.__lights.remove(light)

    def draw(self):
        for light in self.__lights:
            light.draw()

if __name__ == "__main__":
    import math

    pyxel.init(228, 128, title="Lights.py Example", fps=60)
    pyxel.mouse(True)

    lm = LightManager()
    g = CircleLight(114, 64, 20, {12:0})
    lm.add_light(g)

    def update():
        if pyxel.btnp(pyxel.KEY_SPACE):
            g.x = random.randint(20, 208)
            g.y = random.randint(20, 108)

        g.radius =  int(20 + (math.cos(pyxel.frame_count / 5)) * 2)

    def draw():
        pyxel.cls(12)

        lm.draw()

    pyxel.run(update, draw)