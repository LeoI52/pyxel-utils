"""
@author : Léo Imbert
@created : 15/10/2024
@updated : 29/11/2025
"""

from tween import Tween, ease_in_out_elastic
import math

#? -------------------- PATH -------------------- ?#

class PathFollower:

    def __init__(self, points:list, loop:bool=True, easing_function=None, fps:int=60):
        self.points = points
        self.loop = loop
        self.ease = easing_function or (lambda t: t)
        self.fps = fps

        self.current_point = 0
        x, y, d = points[0]
        self.tween_x = Tween(x, x, d, False, self.ease, fps)
        self.tween_y = Tween(y, y, d, False, self.ease, fps)

    def _start_next_segment(self):
        cp = self.current_point
        np = cp + 1

        if np >= len(self.points):
            if self.loop:
                np = 0
            else:
                np = cp

        x1, y1, _ = self.points[cp]
        x2, y2, d = self.points[np]

        self.tween_x = Tween(x1, x2, d, True, self.ease, self.fps)
        self.tween_y = Tween(y1, y2, d, True, self.ease, self.fps)

        self.current_point = np

    def update(self)-> tuple:
        if not self.tween_x.active and not self.tween_y.active:
            self._start_next_segment()

        return self.tween_x.update(), self.tween_y.update()

#? -------------------- MOTIONS -------------------- ?#

def target_motion(x:float, y:float, target_x:float, target_y:float, speed:float)-> tuple:
    dx = target_x - x
    dy = target_y - y
    dist = math.hypot(dx, dy)
    if dist <= speed:
        return target_x, target_y
    return x + dx / dist * speed, y + dy / dist * speed

def wave_motion(value:float, amplitude:float, duration:float, time:int, fps:int=60)-> float:
    return value + math.sin((2 * math.pi) / (duration * fps) * time) * amplitude

def circular_motion(center_x:float, center_y:float, radius:int, duration:float, time:int, fps:int=60)-> tuple:
    angle = (2 * math.pi) / (duration * fps) * time
    x = center_x + math.cos(angle) * radius
    y = center_y + math.sin(angle) * radius
    return x, y

def elliptical_motion(center_x:float, center_y:float, radius_x:float, radius_y:float, duration:float, time:int, fps:int=60)-> tuple:
    angle = (2 * math.pi) / (duration * fps) * time
    x = center_x + math.cos(angle) * radius_x
    y = center_y + math.sin(angle) * radius_y
    return x, y

def spiral_motion(center_x:float, center_y:float, initial_radius:float, growth_rate:float, duration:float, time:int, fps:int=60)-> tuple:
    angle = (2 * math.pi) / (duration * fps) * time
    radius = initial_radius + growth_rate * time
    x = center_x + math.cos(angle) * radius
    y = center_y + math.sin(angle) * radius
    return x, y

def infinity_motion(center_x:float, center_y:float, size:int, duration:float, time:int, fps:int=60)-> tuple:
    t = (2 * math.pi) / (duration * fps) * time
    x = center_x + (math.sin(t) * size) / (1 + math.cos(t)**2)
    y = center_y + (math.sin(t) * math.cos(t) * size) / (1 + math.cos(t)**2)
    return x, y

#? -------------------- EXAMPLE -------------------- ?#

if __name__ == "__main__":
    import pyxel

    inf_points = []
    cx, cy = 114, 64
    path_follower_x = 0
    path_follower_y = 0
    path_follower = PathFollower([(75, 75, 1), (175, 70, 2), (185, 110, 1), (75, 100, 2)], easing_function=ease_in_out_elastic)

    pyxel.init(228, 128, title="Motions.py Example", fps=60)
    pyxel.mouse(True)

    def update():
        global path_follower_x, path_follower_y

        #? Path Follower
        path_follower_x, path_follower_y = path_follower.update()

    def draw():
        global cx, cy
        pyxel.cls(12)

        #? Wave Motion
        pyxel.text(2, 5, "Wave:", 1)
        pyxel.line(60, 7, 140, 7, 9)
        pyxel.circ(wave_motion(100, 40, 2.5, pyxel.frame_count), 7, 2, 1)

        #? Infinity Motion
        pyxel.text(2, 20, "Infinity:", 1)
        inf_x, inf_y = infinity_motion(90, 22, 30, 3, pyxel.frame_count)
        if (inf_x, inf_y) not in inf_points:
            inf_points.append((inf_x, inf_y))
        for x, y in inf_points:
            pyxel.pset(x, y, 9)
        pyxel.circ(inf_x, inf_y, 2, 1)

        #? Circular Motion
        pyxel.text(2, 35, "Circular:", 1)
        circ_x, circ_y = circular_motion(50, 37, 10, 1, pyxel.frame_count)
        pyxel.circb(50, 38, 10, 9)
        pyxel.circ(circ_x, circ_y, 2, 1)

        #? Elliptical Motion
        pyxel.text(2, 50, "Elliptical:", 1)
        elli_x, elli_y = elliptical_motion(90, 52, 30, 10, 2, pyxel.frame_count)
        pyxel.ellib(60, 42, 60, 20, 9)
        pyxel.circ(elli_x, elli_y, 2, 1)

        #? Path Follower
        pyxel.text(2, 75, "Path Follower:", 1)
        path_points = path_follower.points
        for i in range(len(path_points)):
            next_i = (i + 1) % len(path_points)
            pyxel.line(path_points[i][0], path_points[i][1], path_points[next_i][0], path_points[next_i][1], 9)
            pyxel.circb(path_points[i][0], path_points[i][1], 2, 9)
        pyxel.circ(int(path_follower_x), int(path_follower_y), 3, 1)

        #? Target Motion
        cx, cy = target_motion(cx, cy, pyxel.mouse_x, pyxel.mouse_y, 1.5)
        pyxel.circ(cx, cy, 2, 1)

    pyxel.run(update, draw)