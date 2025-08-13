"""
@author : Léo Imbert
@created : 15/10/2024
@updated : 13/08/2025

TODO :
- Particle max velocity
- Emitters
"""

from .draw import Animation
import random
import pyxel
import math

class OvalParticle:

    def __init__(self, x:int, y:int, width:int, height:int, colors:list|int, lifespan:int, speed:int|float, target_x:int, target_y:int, growing_speed:float=0, acceleration_speed:float=0, dither_duration:int=0, gravity:float=0, wobble:bool=False, hollow:bool=False):
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__colors = [colors] if isinstance(colors, int) else colors
        self.__colors_length = len(self.__colors)
        self.__current_color = 0
        self.__lifespan = round(lifespan / self.__colors_length) * self.__colors_length
        self.__starting_lifespan = self.__lifespan
        self.__growing_speed = growing_speed
        self.__acceleration_speed = acceleration_speed
        self.__gravity = gravity
        self.__wobble = wobble
        self.__wobble_offset = random.random() * 1000
        self.__hollow = hollow
        self.__dither = 1
        self.__dither_duration = max(dither_duration, 0)

        self.__direction_x = -1 if target_x - self.__x < 0 else 1
        self.__direction_y = -1 if target_y - self.__y < 0 else 1

        direction_x = target_x - self.__x
        direction_y = target_y - self.__y
        distance = math.sqrt(direction_x ** 2 + direction_y ** 2)
        if distance != 0:
            direction_x /= distance
            direction_y /= distance

        self.__speed_x = direction_x * speed
        self.__speed_y = direction_y * speed

    @property
    def lifespan(self)-> int:
        return self.__lifespan

    def update(self):
        self.__speed_x += self.__acceleration_speed * self.__direction_x
        self.__speed_y += self.__acceleration_speed * self.__direction_y

        self.__speed_y += self.__gravity

        self.__x += self.__speed_x
        self.__y += self.__speed_y

        if self.__wobble:
            self.__x += math.sin(self.__wobble_offset + pyxel.frame_count * 0.1)
            self.__y += math.cos(self.__wobble_offset + pyxel.frame_count * 0.1)

        self.__lifespan -= 1
        self.__width += self.__growing_speed
        self.__height += self.__growing_speed

        if self.__width <= 0 or self.__height <= 0:
            self.__lifespan = 0

        if self.__lifespan <= self.__dither_duration and self.__dither_duration:
            self.__dither -= 1 / self.__dither_duration

        if self.__lifespan % (self.__starting_lifespan / self.__colors_length) == 0 and self.__lifespan != 0:
            self.__current_color = (self.__current_color + 1) % self.__colors_length

    def draw(self):
        pyxel.dither(self.__dither)
        if self.__hollow:
            pyxel.ellib(self.__x - self.__width / 2, self.__y - self.__height / 2, self.__width, self.__height, self.__colors[self.__current_color])
        else:             
            pyxel.elli(self.__x - self.__width / 2, self.__y - self.__height / 2, self.__width, self.__height, self.__colors[self.__current_color])
        pyxel.dither(1)

class RectangleParticle:

    def __init__(self, x:int, y:int, width:int, height:int, colors:list|int, lifespan:int,  speed:int|float, target_x:int, target_y:int, growing_speed:float=0, acceleration_speed:float=0, dither_duration:int=0, gravity:float=0, wobble:bool=False, hollow:bool=False):
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__colors = [colors] if isinstance(colors, int) else colors
        self.__colors_length = len(self.__colors)
        self.__current_color = 0
        self.__lifespan = round(lifespan / self.__colors_length) * self.__colors_length
        self.__starting_lifespan = self.__lifespan
        self.__growing_speed = growing_speed
        self.__acceleration_speed = acceleration_speed
        self.__gravity = gravity
        self.__wobble = wobble
        self.__wobble_offset = random.random() * 1000
        self.__hollow = hollow
        self.__dither = 1
        self.__dither_duration = dither_duration


        self.__direction_x = -1 if target_x - self.__x < 0 else 1
        self.__direction_y = -1 if target_y - self.__y < 0 else 1

        direction_x = target_x - self.__x
        direction_y = target_y - self.__y
        distance = math.sqrt(direction_x ** 2 + direction_y ** 2)
        if distance != 0:
            direction_x /= distance
            direction_y /= distance

        self.__speed_x = direction_x * speed
        self.__speed_y = direction_y * speed

    @property
    def lifespan(self)-> int:
        return self.__lifespan

    def update(self):
        self.__speed_x += self.__acceleration_speed * self.__direction_x
        self.__speed_y += self.__acceleration_speed * self.__direction_y

        self.__speed_y += self.__gravity

        self.__x += self.__speed_x
        self.__y += self.__speed_y

        if self.__wobble:
            self.__x += math.sin(self.__wobble_offset + pyxel.frame_count * 0.1)
            self.__y += math.cos(self.__wobble_offset + pyxel.frame_count * 0.1)

        self.__lifespan -= 1
        self.__width += self.__growing_speed
        self.__height += self.__growing_speed

        if self.__width <= 0 or self.__height <= 0:
            self.__lifespan = 0

        if self.__lifespan <= self.__dither_duration and self.__dither_duration:
            self.__dither -= 1 / self.__dither_duration

        if self.__lifespan % (self.__starting_lifespan / self.__colors_length) == 0 and self.__lifespan != 0:
            self.__current_color = (self.__current_color + 1) % self.__colors_length

    def draw(self):
        pyxel.dither(self.__dither)
        if self.__hollow:   
            pyxel.rectb(self.__x - self.__width / 2, self.__y - self.__height / 2, self.__width, self.__height, self.__colors[self.__current_color])
        else:             
            pyxel.rect(self.__x - self.__width / 2, self.__y - self.__height / 2, self.__width, self.__height, self.__colors[self.__current_color])
        pyxel.dither(1)

class TriangleParticle:

    def __init__(self, x:int, y:int, side_length:int, colors:list|int, lifespan:int, speed:int|float, target_x:int, target_y:int, starting_angle:int=270, growing_speed:float=0, acceleration_speed:float=0, dither_duration:int=0, gravity:float=0, wobble:bool=False, hollow:bool=False, rotating:bool=False, rotation_speed:int=1):
        self.__x = x
        self.__y = y
        self.__side_length = side_length
        self.__colors = [colors] if isinstance(colors, int) else colors
        self.__colors_length = len(self.__colors)
        self.__current_color = 0
        self.__lifespan = round(lifespan / self.__colors_length) * self.__colors_length
        self.__starting_lifespan = self.__lifespan
        self.__starting_angle = starting_angle
        self.__growing_speed = growing_speed
        self.__acceleration_speed = acceleration_speed
        self.__gravity = gravity
        self.__wobble = wobble
        self.__wobble_offset = random.random() * 1000
        self.__hollow = hollow
        self.__dither = 1
        self.__dither_duration = dither_duration
        self.__rotating = rotating
        self.__rotation_speed = rotation_speed


        self.__direction_x = -1 if target_x - self.__x < 0 else 1
        self.__direction_y = -1 if target_y - self.__y < 0 else 1

        direction_x = target_x - self.__x
        direction_y = target_y - self.__y
        distance = math.sqrt(direction_x ** 2 + direction_y ** 2)
        if distance != 0:
            direction_x /= distance
            direction_y /= distance

        self.__speed_x = direction_x * speed
        self.__speed_y = direction_y * speed

    @property
    def lifespan(self)-> int:
        return self.__lifespan

    def update(self):
        self.__speed_x += self.__acceleration_speed * self.__direction_x
        self.__speed_y += self.__acceleration_speed * self.__direction_y

        self.__speed_y += self.__gravity

        self.__x += self.__speed_x
        self.__y += self.__speed_y

        if self.__wobble:
            self.__x += math.sin(self.__wobble_offset + pyxel.frame_count * 0.1)
            self.__y += math.cos(self.__wobble_offset + pyxel.frame_count * 0.1)

        self.__lifespan -= 1
        self.__side_length += self.__growing_speed

        if self.__side_length <= 0:
            self.__lifespan = 0

        if self.__lifespan <= self.__dither_duration and self.__dither_duration:
            self.__dither -= 1 / self.__dither_duration

        if self.__rotating:
            self.__starting_angle += self.__rotation_speed

        if self.__lifespan % (self.__starting_lifespan / self.__colors_length) == 0 and self.__lifespan != 0:
            self.__current_color = (self.__current_color + 1) % self.__colors_length

    def draw(self):
        d = math.sqrt(3) / 3 * self.__side_length
        x1, y1 = self.__x + d * math.cos(math.radians(0 + self.__starting_angle)), self.__y + d * math.sin(math.radians(0 + self.__starting_angle))
        x2, y2 = self.__x + d * math.cos(math.radians(120 + self.__starting_angle)), self.__y + d * math.sin(math.radians(120 + self.__starting_angle))
        x3, y3 = self.__x + d * math.cos(math.radians(240 + self.__starting_angle)), self.__y + d * math.sin(math.radians(240 + self.__starting_angle))

        pyxel.dither(self.__dither)
        if self.__hollow:   
            pyxel.trib(x1, y1, x2, y2, x3, y3, self.__colors[self.__current_color])
        else:             
            pyxel.tri(x1, y1, x2, y2, x3, y3, self.__colors[self.__current_color])
        pyxel.dither(1)

class SpriteParticle:

    def __init__(self, x:int, y:int, animation:Animation, lifespan:int, speed:int|float, target_x:int, target_y:int, acceleration_speed:float=0, dither_duration:int=0, gravity:float=0, wobble:bool=False):
        self.__x = x
        self.__y = y
        self.__animation = animation
        self.__lifespan = lifespan
        self.__acceleration_speed = acceleration_speed
        self.__dither = 1
        self.__dither_duration = dither_duration
        self.__gravity = gravity
        self.__wobble = wobble
        self.__wobble_offset = random.random() * 1000

        self.__direction_x = -1 if target_x - self.__x < 0 else 1
        self.__direction_y = -1 if target_y - self.__y < 0 else 1

        direction_x = target_x - self.__x
        direction_y = target_y - self.__y
        distance = math.sqrt(direction_x ** 2 + direction_y ** 2)
        if distance != 0:
            direction_x /= distance
            direction_y /= distance

        self.__speed_x = direction_x * speed
        self.__speed_y = direction_y * speed

    @property
    def lifespan(self)-> int:
        return self.__lifespan

    def update(self):
        self.__speed_x += self.__acceleration_speed * self.__direction_x
        self.__speed_y += self.__acceleration_speed * self.__direction_y

        self.__speed_y += self.__gravity

        self.__x += self.__speed_x
        self.__y += self.__speed_y

        if self.__wobble:
            self.__x += math.sin(self.__wobble_offset + pyxel.frame_count * 0.1)
            self.__y += math.cos(self.__wobble_offset + pyxel.frame_count * 0.1)

        self.__lifespan -= 1

        if self.__lifespan <= self.__dither_duration and self.__dither_duration:
            self.__dither -= 1 / self.__dither_duration

        self.__animation.update()

    def draw(self):
        pyxel.dither(self.__dither)
        self.__animation.draw(self.__x, self.__y)
        pyxel.dither(1)

class ParticleManager:

    def __init__(self):
        self.__particles = []

    def reset(self):
        self.__particles = []

    def add_particle(self, new_particle:OvalParticle|RectangleParticle|TriangleParticle|SpriteParticle):
        self.__particles.append(new_particle)

    def update(self):
        for particle in self.__particles:
            particle.update()

        self.__particles = [particle for particle in self.__particles if particle.lifespan > 0]

    def draw(self):
        for particle in self.__particles:
            particle.draw()

class CircleShockwave:
    
    def __init__(self, x:int, y:int, max_radius:int, colors:list|int, thickness:int, growth_speed:int|float=1):
        self.__x = x
        self.__y = y
        self.__radius = 0
        self.__max_radius = max_radius
        self.__colors = colors if isinstance(colors, list) else [colors]
        self.__growwth_speed = growth_speed
        self.__thickness = thickness
        self.__alive = True
        self.__dither = 1

    @property
    def alive(self)-> bool:
        return self.__alive

    def update(self):
        self.__radius += self.__growwth_speed
        if self.__dither <= 0:
            self.__alive = False
        if self.__radius >= self.__max_radius:
            self.__dither -= 0.05

    def draw(self):
        pyxel.dither(self.__dither)
        for i in range(int(self.__thickness)):
            pyxel.circb(self.__x, self.__y, self.__radius - i, self.__colors[i % len(self.__colors)])
        pyxel.dither(1)

class ShockwaveManager:

    def __init__(self):
        self.__shockwaves = []

    def reset(self):
        self.__shockwaves = []

    def add_shockwave(self, shockwave:CircleShockwave):
        self.__shockwaves.append(shockwave)

    def remove_shockwave(self, shockwave:CircleShockwave):
        if shockwave in self.__shockwaves:
            self.__shockwaves.remove(shockwave)

    def update(self):
        for shockwave in self.__shockwaves:
            shockwave.update()

        self.__shockwaves = [shockwave for shockwave in self.__shockwaves if shockwave.alive]

    def draw(self):
        for shockwave in self.__shockwaves:
            shockwave.draw()
