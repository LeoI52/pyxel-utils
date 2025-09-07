"""
@author : Léo Imbert
@created : 15/10/2024
@updated : 07/09/2025
"""

import math

def collision_point_rect(x1:int, y1:int, x2:int, y2:int, w2:int, h2:int)-> bool:
    return x2 <= x1 <= x2 + w2 and y2 <= y1 <= y2 + h2

def collision_point_circle(x1:int, y1:int, x2:int, y2:int, r2:int)-> bool:
    return (x1 - x2) ** 2 + (y1 - y2) ** 2 <= r2 ** 2

def collision_rect_rect(x1:int, y1:int, w1:int, h1:int, x2:int, y2:int, w2:int, h2:int)-> bool:
    return not (x1 + w1 < x2 or x2 + w2 < x1 or y1 + h1 < y2 or y2 + h2 < y1)

def collision_circle_circle(x1:int, y1:int, r1:int, x2:int, y2:int, r2:int)-> bool:
    return math.hypot(x2 - x1, y2 - y1) <= r1 + r2

def collision_rect_circle(x1:int, y1:int, w1:int, h1:int, x2:int, y2:int, r2:int)-> bool:
    return ((max(x1, min(x2, x1 + w1)) - x2) ** 2 + (max(y1, min(y2, y1 + h1)) - y2) ** 2) <= r2 ** 2

def collision_line_line(x1:int, y1:int, x2:int, y2:int, x3:int, y3:int, x4:int, y4:int)-> bool:
    def ccw(ax, ay, bx, by, cx, cy): return (cy - ay) * (bx - ax) > (by - ay) * (cx - ax)
    return ccw(x1, y1, x3, y3, x4, y4) != ccw(x2, y2, x3, y3, x4, y4) and ccw(x1, y1, x2, y2, x3, y3) != ccw(x1, y1, x2, y2, x4, y4)

if __name__ == "__main__":
    import pyxel

    pyxel.init(228, 128, title="Collisions.py Example")

    def update():
        pass

    def draw():
        pyxel.cls(12)

        c1 = 8 if collision_circle_circle(pyxel.mouse_x, pyxel.mouse_y, 10, 30, 30, 15) or collision_rect_circle(120, 70, 40, 30, pyxel.mouse_x, pyxel.mouse_y, 10) else 3
        c2 = 8 if collision_point_circle(pyxel.mouse_x, pyxel.mouse_y, 30, 30, 15) or collision_point_rect(pyxel.mouse_x, pyxel.mouse_y, 120, 70, 40, 30) else 3

        pyxel.circ(30, 30, 15, 7)
        pyxel.rect(120, 70, 40, 30, 7)

        pyxel.circb(pyxel.mouse_x, pyxel.mouse_y, 10, c1)
        pyxel.circ(pyxel.mouse_x, pyxel.mouse_y, 1, c2)

    pyxel.run(update, draw)