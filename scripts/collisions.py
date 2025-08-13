"""
@author : Léo Imbert
@created : 15/10/2024
@updated : 13/08/2025
"""

def collision_point_rect(x1:int, y1:int, x2:int, y2:int, w2:int, h2:int)-> bool:
    return x2 <= x1 <= x2 + w2 and y2 <= y1 <= y2 + h2

def collision_point_circle(x1:int, y1:int, x2:int, y2:int, r2:int)-> bool:
    return (x1 - x2) ** 2 + (y1 - y2) ** 2 <= r2 ** 2

def collision_rect_rect(x1:int, y1:int, w1:int, h1:int, x2:int, y2:int, w2:int, h2:int)-> bool:
    return not (x1 + w1 < x2 or x2 + w2 < x1 or y1 + h1 < y2 or y2 + h2 < y1)

def collision_circle_circle(x1:int, y1:int, r1:int, x2:int, y2:int, r2:int)-> bool:
    return (x2 - x1) ** 2 + (y2 - y1) ** 2 <= (r1 + r2) ** 2

def collision_rect_circle(x1:int, y1:int, w1:int, h1:int, x2:int, y2:int, r2:int)-> bool:
    return ((max(x1, min(x2, x1 + w1)) - x2) ** 2 + (max(y1, min(y2, y1 + h1)) - y2) ** 2) <= r2 ** 2

def collision_line_line(x1:int, y1:int, x2:int, y2:int, x3:int, y3:int, x4:int, y4:int)-> bool:
    def ccw(ax, ay, bx, by, cx, cy):
        return (cy - ay) * (bx - ax) > (by - ay) * (cx - ax)
    return ccw(x1, y1, x3, y3, x4, y4) != ccw(x2, y2, x3, y3, x4, y4) and ccw(x1, y1, x2, y2, x3, y3) != ccw(x1, y1, x2, y2, x4, y4)