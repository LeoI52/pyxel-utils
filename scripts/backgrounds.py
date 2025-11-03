"""
@author : Léo Imbert
@created : 20/10/2025
@updated : 20/10/2025
"""

from vars import LEFT, RIGHT, BOTTOM
from animations import wave_motion
import random
import pyxel
import math

class StarBackground:

    def __init__(self, number_stars:int=100, dir:int=LEFT, stars_color:int=7, stars_speed:tuple=(0.4,0.9)):
        self.stars = [[random.randint(0, pyxel.width), random.randint(0, pyxel.height), random.randint(0, 1000), random.uniform(*stars_speed)] for _ in range(number_stars)]
        self.stars_color = stars_color
        self.dir = dir

    def update(self):
        for star in self.stars:
            d = -1 if self.dir in [RIGHT, BOTTOM] else 1
            if self.dir in [LEFT, RIGHT]:
                star[0] = (star[0] + star[3] * d) % pyxel.width
            else:
                star[1] = (star[1] + star[3] * d) % pyxel.height
            star[2] += 1

    def draw(self, camera_x:int=0, camera_y:int=0):
        for x, y, t, _ in self.stars:
            s = wave_motion(2, 1, 0.01, t)
            pyxel.rect(camera_x + x, camera_y + y, s, s, self.stars_color)

class FireBackground:

    def __init__(self, height:int=36, spread:float=0.5, palette:list=[0,8,8,8,9,9,9,9,10,10,7], colkey:int=0):
        self.width = round(pyxel.width / 4)
        self.spread = spread
        self.height = height
        self.pixels = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.palette = palette
        self.maxint = len(palette) - 1
        self.colkey = colkey

        for x in range(self.width):
            self.pixels[self.height - 1][x] = self.maxint

    def update(self):
        for y in range(1, self.height):
            for x in range(self.width):
                newint = self.pixels[y][x] - math.floor(random.random() + self.spread)
                if newint < 1:
                    newint = 0
                self.pixels[y - 1][x] = newint

    def draw(self, camera_x:int=0, camera_y:int=0):
        w, h, off = self.width, self.height, pyxel.height - self.height

        for y in range(h):
            for x in range(w):
                intensity = self.pixels[y][x]
                col = self.palette[intensity] if intensity < len(self.palette) else self.colkey
                if col != self.colkey:
                    pyxel.pset(camera_x + x, camera_y + y + off, col)
                    pyxel.pset(camera_x + x + w, camera_y + y + off, col)
                    pyxel.pset(camera_x + x + w * 2, camera_y + y + off, col)
                    pyxel.pset(camera_x + x + w * 3, camera_y + y + off, col)

class NebulaBackground:

    def __init__(self, color_palette:list=[1, 2, 13, 5, 6], density:int=200, speed:float=0.1):
        self.clouds = [[random.randint(0, pyxel.width),random.randint(0, pyxel.height),random.choice(color_palette),random.uniform(5, 15),random.uniform(-speed, speed),random.uniform(-speed, speed)] for _ in range(density)]
        self.color_palette = color_palette

    def update(self):
        for c in self.clouds:
            c[0] = (c[0] + c[4]) % pyxel.width
            c[1] = (c[1] + c[5]) % pyxel.height

    def draw(self, camera_x:int=0, camera_y:int=0):
        for x, y, col, radius, *_ in self.clouds:
            for i in range(int(radius)):
                pyxel.circ(camera_x + x, camera_y + y, int(radius - i), col)

class GradientBackground:

    def __init__(self, colors:list=[1, 5, 6, 7], vertical:bool=True, scroll_speed:float=0.2):
        self.colors = colors
        self.vertical = vertical
        self.scroll_speed = scroll_speed
        self.offset = 0

    def update(self):
        self.offset += self.scroll_speed

    def draw(self, camera_x:int=0, camera_y:int=0):
        steps = len(self.colors)
        for i in range(pyxel.height if self.vertical else pyxel.width):
            t = ((i + self.offset) % pyxel.height) / pyxel.height
            c = self.colors[int(t * steps) % steps]
            if self.vertical:
                pyxel.line(camera_x, camera_y + i, camera_x + pyxel.width, camera_y + i, c)
            else:
                pyxel.line(camera_x + i, camera_y, camera_x + i, camera_y + pyxel.height, c)

if __name__ == "__main__":
    pyxel.init(228, 128, title="Backgrounds.py Example")
    pyxel.mouse(True)

    b = StarBackground()

    def update():
        b.update()

    def draw():
        pyxel.cls(1)

        b.draw()

    pyxel.run(update, draw)