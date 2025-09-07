"""
@author : Léo Imbert
@created : 15/10/2024
@updated : 07/09/2025

TODO :
- Particle max velocity
- Emitters
"""

from draw import Animation
import random
import pyxel
import math

class Particle:

    def __init__(self, x:int, y:int, lifespan:int, speed:int, target:tuple, friction:tuple=(1, 1), acceleration:tuple=(0, 0), dither_duration:int=0, wooble:bool=False):
        self.x, self.y = x, y
        self.lifespan = lifespan
        self.fx, self.fy = friction
        self.ax, self.ay = acceleration
        self.dither = 1
        self.dither_duration = max(dither_duration, 0)
        self.wooble = wooble
        self.wooble_offset = random.random() * 1000 if wooble else 0

        dx = target[0] - x
        dy = target[1] - y
        mag = (dx ** 2 + dy ** 2) ** 0.5
        self.vx = dx / mag * speed if mag != 0 else 0
        self.vy = dy / mag * speed if mag != 0 else 0

    def update(self):
        self.lifespan -= 1

        self.vx *= self.fx
        self.vy *= self.fy
        self.vx += self.ax
        self.vy += self.ay
        self.x += self.vx
        self.y += self.vy

        if self.wooble:
            self.x += math.sin(self.wooble_offset + pyxel.frame_count * 0.1)
            self.y += math.cos(self.wooble_offset + pyxel.frame_count * 0.1)

        if self.lifespan <= self.dither_duration and self.dither_duration:
            self.dither -= 1 / self.dither_duration

class ShapeParticle(Particle):

    def __init__(self, x:int, y:int, w:int, h:int, colors:int|list, lifespan:int, speed:int, target:tuple, friction:tuple=(1, 1), acceleration:tuple=(0, 0), grow:tuple=(1, 1), dither_duration:int=0, hollow:bool=False, wooble:bool=False):
        super().__init__(x, y, lifespan, speed, target, friction, acceleration, dither_duration, wooble)
        self.w, self.h = w, h
        self.colors = [colors] if isinstance(colors, int) else colors
        self.colors_length = len(self.colors)
        self.current_color = 0
        self.lifespan = round(lifespan / self.colors_length) * self.colors_length
        self.initial_lifespan = self.lifespan
        self.gw, self.gh = grow
        self.hollow = hollow

    def update(self):
        super().update()

        self.w *= self.gw
        self.h *= self.gh

        if self.w < 1 or self.h < 1:
            self.lifespan = 0

        if self.lifespan > 0 and self.lifespan % (self.initial_lifespan / self.colors_length) == 0:
            self.current_color = (self.current_color + 1) % self.colors_length

class OvalParticle(ShapeParticle):

    def __init__(self, x:int, y:int, w:int, h:int, colors:int|list, lifespan:int, speed:int, target:tuple, friction:tuple=(1, 1), acceleration:tuple=(0, 0), grow:tuple=(1, 1), dither_duration:int=0, hollow:bool=False, wooble:bool=False):
        super().__init__(x, y, w, h, colors, lifespan, speed, target, friction, acceleration, grow, dither_duration, hollow, wooble)

    def draw(self):
        pyxel.dither(self.dither)
        if self.hollow:    pyxel.ellib(self.x, self.y, self.w, self.h, self.colors[self.current_color])
        else:              pyxel.elli(self.x, self.y, self.w, self.h, self.colors[self.current_color])
        pyxel.dither(1)

class RectangleParticle(ShapeParticle):

    def __init__(self, x:int, y:int, w:int, h:int, colors:int|list, lifespan:int, speed:int, target:tuple, friction:tuple=(1, 1), acceleration:tuple=(0, 0), grow:tuple=(1, 1), dither_duration:int=0, hollow:bool=False, wooble:bool=False):
        super().__init__(x, y, w, h, colors, lifespan, speed, target, friction, acceleration, grow, dither_duration, hollow, wooble)

    def draw(self):
        pyxel.dither(self.dither)
        if self.hollow:    pyxel.rectb(self.x, self.y, self.w, self.h, self.colors[self.current_color])
        else:              pyxel.rect(self.x, self.y, self.w, self.h, self.colors[self.current_color])
        pyxel.dither(1)
        
class TriangleParticle(ShapeParticle):

    def __init__(self, x:int, y:int, side_lenght:int, colors:int|list, lifespan:int, speed:int, target:tuple, friction:tuple=(1, 1), acceleration:tuple=(0, 0), grow:int=1, starting_angle:int=0, dither_duration:int=0, hollow:bool=False, rotating:bool=False, rotation_speed:int=1, wooble:bool=False):
        super().__init__(x, y, side_lenght, side_lenght, colors, lifespan, speed, target, friction, acceleration, (grow, grow), dither_duration, hollow, wooble)
        self.angle = starting_angle
        self.rotating = rotating
        self.rotation_speed = rotation_speed

    def update(self):
        super().update()

        if self.rotating:
            self.angle += self.rotation_speed

    def draw(self):
        d = math.sqrt(3) / 3 * self.w
        x1, y1 = self.x + d * math.cos(math.radians(0 + self.angle)), self.y + d * math.sin(math.radians(0 + self.angle))
        x2, y2 = self.x + d * math.cos(math.radians(120 + self.angle)), self.y + d * math.sin(math.radians(120 + self.angle))
        x3, y3 = self.x + d * math.cos(math.radians(240 + self.angle)), self.y + d * math.sin(math.radians(240 + self.angle))

        pyxel.dither(self.dither)
        if self.hollow:    pyxel.trib(x1, y1, x2, y2, x3, y3, self.colors[self.current_color])
        else:              pyxel.tri(x1, y1, x2, y2, x3, y3, self.colors[self.current_color])
        pyxel.dither(1)

class StarParticle(ShapeParticle):

    def __init__(self, x:int, y:int, radius:int, points:int, colors:int|list, lifespan:int, speed:int, target:tuple, friction:tuple=(1,1), acceleration:tuple=(0,0), grow:int=1, dither_duration:int=0, hollow:bool=False, rotating:bool=False, rotation_speed:float=1):
        super().__init__(x, y, radius, radius, colors, lifespan, speed, target, friction, acceleration, (grow, grow), dither_duration, hollow)
        self.points = max(5, points)
        self.angle = 0
        self.rotating = rotating
        self.rotation_speed = rotation_speed

    def update(self):
        super().update()

        if self.rotating:
            self.angle += self.rotation_speed

    def draw(self):
        pyxel.dither(self.dither)
        step = 360 / self.points
        r_outer = self.w
        r_inner = self.w / 2
        coords = []
        for i in range(self.points * 2):
            r = r_outer if i % 2 == 0 else r_inner
            ang = math.radians(self.angle + step/2 * i)
            coords.append((self.x + r * math.cos(ang), self.y + r * math.sin(ang)))

        for i in range(len(coords)):
            x1, y1 = coords[i]
            x2, y2 = coords[(i+1) % len(coords)]
            if self.hollow:
                pyxel.line(x1, y1, x2, y2, self.colors[self.current_color])
            else:
                pyxel.tri(self.x, self.y, x1, y1, x2, y2, self.colors[self.current_color])
        pyxel.dither(1)

class LineParticle(Particle):

    def __init__(self, x:int, y:int, lenght:int, colors:int|list, lifespan:int, speed:int, target:tuple, friction:tuple=(1, 1), acceleration:tuple=(0, 0), dither_duration:int=0, wooble:bool=False):
        super().__init__(x, y, lifespan, speed, target, friction, acceleration, dither_duration, wooble)
        self.lenght = lenght
        self.colors = [colors] if isinstance(colors, int) else colors
        self.colors_length = len(self.colors)
        self.current_color = 0
        self.lifespan = round(lifespan / self.colors_length) * self.colors_length
        self.initial_lifespan = self.lifespan

    def update(self):
        super().update()

        if self.lifespan > 0 and self.lifespan % (self.initial_lifespan / self.colors_length) == 0:
            self.current_color = (self.current_color + 1) % self.colors_length

    def draw(self):
        vx2 = self.vx * self.fx + self.ax
        vy2 = self.vy * self.fy + self.ay
        mag = (vx2 ** 2 + vy2 ** 2) ** 0.5
        x2 = self.x + (vx2 / mag * self.lenght) if mag != 0 else self.x
        y2 = self.y + (vy2 / mag * self.lenght) if mag != 0 else self.y

        pyxel.dither(self.dither)
        pyxel.line(self.x, self.y, x2, y2, self.colors[self.current_color])
        pyxel.dither(1)

class SpriteParticle(Particle):

    def __init__(self, x:int, y:int, animation:Animation, lifespan:int, speed:int, target:tuple, friction:tuple=(1, 1), acceleration:tuple=(0, 0), dither_duration:int=0, wooble:bool=False):
        super().__init__(x, y, lifespan, speed, target, friction, acceleration, dither_duration, wooble)
        self.animation = animation

    def update(self):
        super().update()

        self.animation.update()

    def draw(self):
        pyxel.dither(self.dither)
        self.animation.draw(self.x, self.y)
        pyxel.dither(1)

class ParticleManager:

    def __init__(self):
        self.particles = []

    def reset(self):
        self.particles = []

    def add_particle(self, new_particle:OvalParticle|RectangleParticle|TriangleParticle|SpriteParticle):
        self.particles.append(new_particle)

    def update(self):
        for particle in self.particles:
            particle.update()

        self.particles = [particle for particle in self.particles if particle.lifespan > 0]

    def draw(self):
        for particle in self.particles:
            particle.draw()

class CircleShockwave:
    
    def __init__(self, x:int, y:int, max_radius:int, colors:list|int, thickness:int, growth_speed:int|float=1):
        self.x = x
        self.y = y
        self.radius = 0
        self.max_radius = max_radius
        self.colors = colors if isinstance(colors, list) else [colors]
        self.growth_speed = growth_speed
        self.thickness = thickness
        self.alive = True
        self.dither = 1

    def update(self):
        self.radius += self.growth_speed
        if self.dither <= 0:
            self.alive = False
        if self.radius >= self.max_radius:
            self.dither -= 0.05

    def draw(self):
        pyxel.dither(self.dither)
        for i in range(int(self.thickness)):
            pyxel.circb(self.x, self.y, self.radius - i, self.colors[i % len(self.colors)])
        pyxel.dither(1)

class ShockwaveManager:

    def __init__(self):
        self.shockwaves = []

    def reset(self):
        self.shockwaves = []

    def add_shockwave(self, shockwave:CircleShockwave):
        self.shockwaves.append(shockwave)

    def remove_shockwave(self, shockwave:CircleShockwave):
        if shockwave in self.shockwaves:
            self.shockwaves.remove(shockwave)

    def update(self):
        for shockwave in self.shockwaves:
            shockwave.update()

        self.shockwaves = [shockwave for shockwave in self.shockwaves if shockwave.alive]

    def draw(self):
        for shockwave in self.shockwaves:
            shockwave.draw()

if __name__ == "__main__":
    particle_manager = ParticleManager()
    shockwave_manager = ShockwaveManager()
    modes = ["oval particle", "rect particle", "triangle particle", "line particle", "star particle"]
    mode = modes[0]

    pyxel.init(228, 128, title="Particles.py Example")
    pyxel.mouse(True)

    def update():
        global mode

        shockwave_manager.update()
        particle_manager.update()

        if pyxel.btnp(pyxel.KEY_SPACE):
            mode = modes[(modes.index(mode) + 1) % len(modes)]

        if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
            shockwave_manager.add_shockwave(CircleShockwave(pyxel.mouse_x, pyxel.mouse_y, random.randint(5, 30), [random.randint(2, 15) for _ in range(3)], 3, random.uniform(1, 2)))
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if mode == "oval particle":
                for _ in range(5):
                    angle = random.uniform(0, 2 * math.pi)
                    target_x = pyxel.mouse_x + math.cos(angle) * 50
                    target_y = pyxel.mouse_y + math.sin(angle) * 50
                    s = random.randint(1, 5)
                    particle_manager.add_particle(OvalParticle(pyxel.mouse_x, pyxel.mouse_y, s, s, [11, 10, 9, 8], 60, random.uniform(0.5, 1.5), (target_x, target_y), acceleration=(0, 0.01), dither_duration=20))
            elif mode == "rect particle":
                for _ in range(5):
                    angle = random.uniform(0, 2 * math.pi)
                    target_x = pyxel.mouse_x + math.cos(angle) * 50
                    target_y = pyxel.mouse_y + math.sin(angle) * 50
                    s = random.randint(1, 5)
                    particle_manager.add_particle(RectangleParticle(pyxel.mouse_x, pyxel.mouse_y, s, s, [11, 10, 9, 8], 60, random.uniform(0.5, 1.5), (target_x, target_y), dither_duration=20))
            elif mode == "triangle particle":
                for _ in range(5):
                    angle = random.uniform(0, 2 * math.pi)
                    target_x = pyxel.mouse_x + math.cos(angle) * 50
                    target_y = pyxel.mouse_y + math.sin(angle) * 50
                    particle_manager.add_particle(TriangleParticle(pyxel.mouse_x, pyxel.mouse_y, random.randint(1, 5), [11, 10, 9, 8], 60, random.uniform(0.5, 1.5), (target_x, target_y), starting_angle=random.randint(0, 360), dither_duration=20, rotating=True))
            elif mode == "line particle":
                for _ in range(5):
                    angle = random.uniform(0, 2 * math.pi)
                    target_x = pyxel.mouse_x + math.cos(angle) * 50
                    target_y = pyxel.mouse_y + math.sin(angle) * 50
                    particle_manager.add_particle(LineParticle(pyxel.mouse_x, pyxel.mouse_y, 5, [11, 10, 9, 8], 60, random.uniform(0.5, 1.5), (target_x, target_y), acceleration=(0, 0.01), dither_duration=20))
            elif mode == "star particle":
                for _ in range(5):
                    angle = random.uniform(0, 2 * math.pi)
                    target_x = pyxel.mouse_x + math.cos(angle) * 50
                    target_y = pyxel.mouse_y + math.sin(angle) * 50
                    s = random.randint(3, 7)
                    particle_manager.add_particle(StarParticle(pyxel.mouse_x, pyxel.mouse_y, s, 5, [11, 10, 9, 8], 60, random.uniform(0.5, 1.5), (target_x, target_y), acceleration=(0, 0.01), dither_duration=20, rotating=True))

    def draw():
        pyxel.cls(1)

        shockwave_manager.draw()
        particle_manager.draw()

        pyxel.text(5, 5, "Left Click For Particles", 9)
        pyxel.text(5, 15, "Right Click For Shockwaves", 9)
        pyxel.text(5, 25, "Space to change mode", 9)
        pyxel.text(5, 35, f"Mode: {mode}", 9)

    pyxel.run(update, draw)