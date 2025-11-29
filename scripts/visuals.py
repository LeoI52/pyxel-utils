"""
@author : Léo Imbert
@created : 20/10/2025
@updated : 29/11/2025
"""

from motions import wave_motion
from vars import *
import random
import pyxel
import math

#? -------------------- BACKGROUNDS -------------------- ?#

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
            s = wave_motion(2, 1, 1, t)
            pyxel.rect(camera_x + x, camera_y + y, s, s, self.stars_color)

class NebulaBackground:

    def __init__(self, color_palette:list=[1, 2, 13, 5, 6], density:int=200, speed:float=0.1):
        self.clouds = [[random.randint(0, pyxel.width), random.randint(0, pyxel.height), random.choice(color_palette), random.uniform(5, 15), random.uniform(-speed, speed), random.uniform(-speed, speed)] for _ in range(density)]
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

    def __init__(self, colors:list=[1, 5, 6, 7], dir:int=VERTICAL, scroll_speed:float=0.2):
        self.colors = colors
        self.dir = dir
        self.scroll_speed = scroll_speed
        self.offset = 0

    def update(self):
        self.offset += self.scroll_speed

    def draw(self, camera_x:int=0, camera_y:int=0):
        steps = len(self.colors)
        for i in range(pyxel.height if self.dir == VERTICAL else pyxel.width):
            t = ((i + self.offset) % pyxel.height) / pyxel.height
            c = self.colors[int(t * steps) % steps]
            if self.dir == VERTICAL:
                pyxel.line(camera_x, camera_y + i, camera_x + pyxel.width, camera_y + i, c)
            else:
                pyxel.line(camera_x + i, camera_y, camera_x + i, camera_y + pyxel.height, c)

class MatrixRainBackground:
    
    def __init__(self, columns:int=32, speed:float=1.5, colors:list=[3, 11, 7]):
        self.column_width = pyxel.width // columns
        self.columns = columns
        self.speed = speed
        self.colors = colors
        self.drops = [[random.randint(-20, pyxel.height), random.uniform(0.5, 2.0), random.randint(5, 20)] for _ in range(columns)]
    
    def update(self):
        for drop in self.drops:
            drop[0] += drop[1] * self.speed
            if drop[0] > pyxel.height + drop[2]:
                drop[0] = -drop[2]
                drop[1] = random.uniform(0.5, 2.0)
                drop[2] = random.randint(5, 20)
    
    def draw(self, camera_x:int=0, camera_y:int=0):
        for i, (y, speed, length) in enumerate(self.drops):
            x = i * self.column_width + self.column_width // 2
            for j in range(length):
                char_y = y - j * 4
                if 0 <= char_y < pyxel.height:
                    color_idx = min(j // 3, len(self.colors) - 1)
                    pyxel.rect(camera_x + x, camera_y + char_y, 2, 3, self.colors[color_idx])

#? -------------------- EFFECTS -------------------- ?#

class Flash:

    def __init__(self, color:int, intensity:float, lifetime:int, decay:float=0):
        self.color = color
        self.intensity = intensity
        self.lifetime = lifetime
        self.decay = decay

    def update(self):
        self.lifetime = max(0, self.lifetime - 1)
        self.intensity = max(0, self.intensity - self.decay)

    def draw(self, camera_x:int=0, camera_y:int=0):
        pyxel.dither(self.intensity)
        pyxel.rect(camera_x, camera_y, pyxel.width, pyxel.height, self.color)
        pyxel.dither(1)

class FlashManager:

    def __init__(self):
        self.__flashes = []

    def add_flash(self, flash:Flash):
        self.__flashes.append(flash)

    def update(self):
        for flash in self.__flashes:
            flash.update()
        self.__flashes = [flash for flash in self.__flashes if flash.lifetime]
    
    def draw(self, camera_x:int=0, camera_y:int=0):
        for flash in self.__flashes:
            flash.draw(camera_x, camera_y)

class LightningBolt:

    def __init__(self, start_x:int, colors:list):

        self.points = [(start_x, 0)]
        x, y = start_x, 0
        
        while y < pyxel.height:
            x += random.randint(-8, 8)
            y += random.randint(8, 15)
            self.points.append((x, y))
            
            if random.random() < 0.3 and len(self.points) > 2:
                branch_x = x + random.randint(-15, 15)
                branch_y = y + random.randint(5, 10)
                self.points.append((branch_x, branch_y))

        self.colors = colors
        self.lifetime = 10

    def update(self):
        self.lifetime = max(0, self.lifetime - 1)

    def draw(self, camera_x:int=0, camera_y:int=0):
        color_idx = min(self.lifetime // 3, len(self.colors) - 1)
        color = self.colors[color_idx]
        
        for i in range(len(self.points) - 1):
            x1, y1 = self.points[i]
            x2, y2 = self.points[i + 1]
            pyxel.line(camera_x + x1, camera_y + y1, camera_x + x2, camera_y + y2, color)

class LightningManager:

    def __init__(self, strike_chance:float=0.02, flash_color:int=7, lightning_colors:list=[7, 6, 13], flash_time:int=15):
        self.strike_chance = strike_chance
        self.flash_color = flash_color
        self.lightning_colors = lightning_colors
        self.bolts = []
        self.flashes = []
        self.flash_timer = 0
        self.flash_time = flash_time

    def update(self):
        if random.random() < self.strike_chance and len(self.bolts) < 2:
            start_x = random.randint(10, pyxel.width - 10)
            self.bolts.append(LightningBolt(start_x, self.lightning_colors))
            self.flashes.append(Flash(self.flash_color, random.uniform(0.3, 0.6), 5, 0.1))
            self.flash_timer = self.flash_time
        
        for flash in self.flashes:
            flash.update()
        self.flashes = [flash for flash in self.flashes if flash.lifetime]

        for bolt in self.bolts:
            bolt.update()
        self.bolts = [bolt for bolt in self.bolts if bolt.lifetime]
        
        self.flash_timer = max(0, self.flash_timer - 1)

    def draw(self, camera_x:int=0, camera_y:int=0):
        for flash in self.flashes:
            flash.draw(camera_x, camera_y)

        for bolt in self.bolts:
            bolt.draw(camera_x, camera_y)

class FireOverlay:

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

#? -------------------- EXAMPLE -------------------- ?#

if __name__ == "__main__":
    pyxel.init(228, 128, title="Visuals.py Example")
    pyxel.mouse(True)

    b = LightningManager()

    def update():
        b.update()

    def draw():
        pyxel.cls(1)

        b.draw()

    pyxel.run(update, draw)