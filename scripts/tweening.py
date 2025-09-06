"""
@author : Léo Imbert
@created : 06/09/2025
@updated : 06/09/2025
"""

import math

class Tween:

    def __init__(self, start:int, end:int, duration:float, autostart:bool=False, easing_function=None):
        self.start = start
        self.end = end
        self.duration = duration
        self.ease = easing_function or (lambda t: t)

        self.elapsed = 0
        self.active = autostart
        self.value = start

    def update(self, dt:float)-> float:
        if not self.active:
            return self.value
        
        self.elapsed += dt
        t = self.ease(min(self.elapsed / self.duration, 1.0))
        self.value = self.start + (self.end - self.start) * t

        if self.elapsed >= self.duration:
            self.active = False

        return self.value
    
def linear(t): return t

def ease_in_quad(t): return t * t
def ease_out_quad(t): return t * (2 - t)
def ease_in_out_quad(t): return 2 * t * t if t < 0.5 else -1 + (4 - 2 * t) * t

def ease_in_cubic(t): return t ** 3
def ease_out_cubic(t): return (t - 1) ** 3 + 1
def ease_in_out_cubic(t): return 4 * t ** 3 if t < 0.5 else (t - 1) * (2 * t - 2) ** 2 + 1

def ease_in_quart(t): return t ** 4
def ease_out_quart(t): return 1 - (t - 1) ** 4
def ease_in_out_quart(t): return 8 * t ** 4 if t < 0.5 else 1 - 8 * (t - 1) ** 4

def ease_in_quint(t): return t ** 5
def ease_out_quint(t): return 1 + (t - 1) ** 5
def ease_in_out_quint(t): return 16 * t ** 5 if t < 0.5 else 1 + 16 * (t - 1) ** 5

def ease_in_sine(t): return 1 - math.cos((t * math.pi) / 2)
def ease_out_sine(t): return math.sin((t * math.pi) / 2)
def ease_in_out_sine(t): return -(math.cos(math.pi * t) - 1) / 2

def ease_in_circ(t): return 1 - math.sqrt(1 - t * t)
def ease_out_circ(t): return math.sqrt(1 - (t - 1) ** 2)
def ease_in_out_circ(t): return (1 - math.sqrt(1 - (2 * t) ** 2)) / 2 if t < 0.5 else (math.sqrt(1 - (2 * t - 2) ** 2) + 1) / 2

def ease_in_elastic(t):
    if t == 0 or t == 1: return t
    return -2 ** (10 * (t - 1)) * math.sin((t - 1.1) * 5 * math.pi)
def ease_out_elastic(t):
    if t == 0 or t == 1: return t
    return 2 ** (-10 * t) * math.sin((t - 0.1) * 5 * math.pi) + 1
def ease_in_out_elastic(t):
    if t == 0 or t == 1: return t
    t *= 2
    if t < 1: return -0.5 * 2 ** (10 * (t - 1)) * math.sin((t - 1.1) * 5 * math.pi)
    return 0.5 * 2 ** (-10 * (t - 1)) * math.sin((t - 1.1) * 5 * math.pi) + 1

def ease_in_back(t, s=1.70158): return t * t * ((s + 1) * t - s)
def ease_out_back(t, s=1.70158):
    t -= 1
    return t * t * ((s + 1) * t + s) + 1
def ease_in_out_back(t, s=1.70158):
    s *= 1.525
    if t < 0.5: return (t * 2) ** 2 * ((s + 1) * t * 2 - s) / 2
    t = t * 2 - 2
    return (t ** 2 * ((s + 1) * t + s) + 2) / 2

def ease_out_bounce(t):
    if t < 1 / 2.75: return 7.5625 * t * t
    elif t < 2 / 2.75:
        t -= 1.5 / 2.75
        return 7.5625 * t * t + 0.75
    elif t < 2.5 / 2.75:
        t -= 2.25 / 2.75
        return 7.5625 * t * t + 0.9375
    else:
        t -= 2.625 / 2.75
        return 7.5625 * t * t + 0.984375
def ease_in_bounce(t): return 1 - ease_out_bounce(1 - t)
def ease_in_out_bounce(t): return ease_in_bounce(t * 2) / 2 if t < 0.5 else ease_out_bounce(t * 2 - 1) / 2 + 0.5

def ease_wobble(t): return t + 0.1 * math.sin(8 * math.pi * t) * (1 - t)

if __name__ == "__main__":
    import pyxel

    pyxel.init(228, 128, title="Tween.py Example", fps=60)

    t = Tween(11, 216, 1.5, easing_function=ease_out_quint)
    x = t.start

    def update():
        global x
        x = t.update(1/60)

        if pyxel.btnp(pyxel.KEY_SPACE) and not t.active:
            if t.elapsed != 0:
                t.start, t.end = t.end, t.start
            t.elapsed = 0
            t.active = True

    def draw():
        pyxel.cls(12)
        pyxel.circ(x, 64, 10, 1)

    pyxel.run(update, draw)