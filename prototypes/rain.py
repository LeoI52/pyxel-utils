import pyxel
import random

pyxel.init(8, 8, fps=60)
pyxel.fullscreen(True)
pyxel.colors.clear()
pyxel.colors.extend([0x000000, 0x1D2B53, 0x7E2553, 0x008751, 0xAB5236, 0x5F574F, 0xC2C3C7, 0xFFF1E8, 0xFF004D, 0xFFA300, 0xFFEC27, 0x00E436, 0x29ADFF, 0x83769C, 0xFF77A8, 0xFFCCAA])

class Drop:

    def __init__(self, x, y, length, target, sp_x=2, sp_y=4):
        self.x = x
        self.y = y
        self.len = int(length)
        self.target = target
        self.sp_x = sp_x
        self.sp_y = sp_y

    def update(self):
        self.x += self.sp_x
        self.y += self.sp_y

    def draw(self):
        for i in range(self.len, -1, -1):
            pyxel.pset(int(self.x - (i // 2)), int(self.y - i), 7)

class Ripple:

    def __init__(self, x, y, life):
        self.x = x
        self.y = y
        self.life = life
        self.t = 1
        self.width = 2
        self.height = 1

    def update(self):
        self.t += 0.5

    def draw(self):
        pyxel.ellib(self.x - (self.width / 2) * self.t, self.y - (self.height / 2) * self.t, self.width * self.t, self.height * self.t, 7)

class RainOverlay:

    def __init__(self, num_drops=50):
        self.drops = [
            Drop(
                x=-100 + random.uniform(0, 128),
                y=-1 * random.uniform(0, 300),
                length=3 + random.uniform(0, 10),
                target=80 + random.uniform(0, 68),
            )
            for _ in range(num_drops)
        ]
        self.ripples = []

    def update(self):
        for d in self.drops:
            d.update()

        for r in self.ripples:
            r.update()

        for i in range(len(self.drops) - 1, -1, -1):
            if self.drops[i].y >= self.drops[i].target:
                old = self.drops.pop(i)
                self.drops.append(
                    Drop(
                        x=-100 + random.uniform(0, 128),
                        y=-1 * random.uniform(0, 300),
                        length=3 + random.uniform(0, 10),
                        target=80 + random.uniform(0, 68),
                    )
                )
                self.ripples.append(Ripple(old.x, old.y, life=10 + random.uniform(0, 5)))

        for i in range(len(self.ripples) - 1, -1, -1):
            if self.ripples[i].t > self.ripples[i].life:
                self.ripples.pop(i)

    def draw(self):
        for d in self.drops:
            d.draw()
        for r in self.ripples:
            r.draw()

def update():
    pass

def draw():
    pyxel.cls(0)

pyxel.run(update, draw)