"""
@author : Léo Imbert
@created : 15/10/2024
@updated : 07/09/2025
"""

import math

def follow_path(x:int, y:int, speed:float, current_point:int, points:list, loop:bool=True)-> tuple:
    direction_x = points[current_point][0] - x
    direction_y = points[current_point][1] - y
    distance = math.sqrt(direction_x ** 2 + direction_y ** 2)

    if distance < max(speed, 0.1):
        current_point = (current_point + 1) % len(points) if loop else current_point + 1
        if current_point >= len(points) and not loop:
            current_point -= 1
        return x, y, current_point
    
    direction_x /= distance
    direction_y /= distance

    return x + direction_x * speed, y + direction_y * speed, current_point

def target_motion(x:float, y:float, target_x:float, target_y:float, speed:float)-> tuple:
    dx = target_x - x
    dy = target_y - y
    dist = math.hypot(dx, dy)
    if dist == 0:
        return x, y
    return x + dx / dist * speed, y + dy / dist * speed

def wave_motion(value:float, amplitude:float, speed:float, time:int)-> float:
    return value + math.cos(time * speed) * amplitude

def circular_motion(center_x:float, center_y:float, radius:int, speed:float, time:int)-> tuple:
    angle = time * speed
    x = center_x + math.cos(angle) * radius
    y = center_y + math.sin(angle) * radius
    return x, y

def elliptical_motion(center_x:float, center_y:float, radius_x:float, radius_y:float, speed:float, time:int)-> tuple:
    angle = time * speed
    x = center_x + math.cos(angle) * radius_x
    y = center_y + math.sin(angle) * radius_y
    return x, y

def spiral_motion(center_x:float, center_y:float, initial_radius:float, growth_rate:float, speed:float, time:int)-> tuple:
    angle = time * speed
    radius = initial_radius + growth_rate * time
    x = center_x + math.cos(angle) * radius
    y = center_y + math.sin(angle) * radius
    return x, y

def infinity_motion(center_x:float, center_y:float, size:int, speed:float, time:int)-> tuple:
    t = time * speed
    x = center_x + (math.sin(t) * size) / (1 + math.cos(t)**2)
    y = center_y + (math.sin(t) * math.cos(t) * size) / (1 + math.cos(t)**2)
    return x, y

if __name__ == "__main__":
    import pyxel

    inf_points = []
    cx, cy = 114, 64
    path_follower_x = 75
    path_follower_y = 75
    path_current_point = 0
    path_points = [(75, 75), (175, 70), (185, 110), (75, 100)]

    pyxel.init(228, 128, title="Animations.py Example")
    pyxel.mouse(True)

    def update():
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            print(pyxel.mouse_x, pyxel.mouse_y)
        global path_follower_x, path_follower_y, path_current_point

        #? Path Follower
        path_follower_x, path_follower_y, path_current_point = follow_path(path_follower_x, path_follower_y, 1.5, path_current_point, path_points, True)

    def draw():
        global cx, cy
        pyxel.cls(12)

        #? Wave Motion
        pyxel.text(2, 5, "Wave:", 1)
        pyxel.line(60, 7, 140, 7, 9)
        pyxel.circ(wave_motion(100, 40, 0.05, pyxel.frame_count), 7, 2, 1)

        #? Infinity Motion
        pyxel.text(2, 20, "Infinity:", 1)
        inf_x, inf_y = infinity_motion(90, 22, 30, 0.05, pyxel.frame_count)
        if (inf_x, inf_y) not in inf_points:
            inf_points.append((inf_x, inf_y))
        for x, y in inf_points:
            pyxel.pset(x, y, 9)
        pyxel.circ(inf_x, inf_y, 2, 1)

        #? Circular Motion
        pyxel.text(2, 35, "Circular:", 1)
        circ_x, circ_y = circular_motion(50, 37, 10, 0.05, pyxel.frame_count)
        pyxel.circb(50, 38, 10, 9)
        pyxel.circ(circ_x, circ_y, 2, 1)

        #? Elliptical Motion
        pyxel.text(2, 50, "Elliptical:", 1)
        elli_x, elli_y = elliptical_motion(90, 52, 30, 10, 0.1, pyxel.frame_count)
        pyxel.ellib(60, 42, 60, 20, 9)
        pyxel.circ(elli_x, elli_y, 2, 1)

        #? Path Follower
        pyxel.text(2, 75, "Path Follower:", 1)
        for i in range(len(path_points)):
            next_i = (i + 1) % len(path_points)
            pyxel.line(path_points[i][0], path_points[i][1], path_points[next_i][0], path_points[next_i][1], 9)
            pyxel.circb(path_points[i][0], path_points[i][1], 2, 9)
        pyxel.circ(int(path_follower_x), int(path_follower_y), 3, 1)

        #? Target Motion
        cx, cy = target_motion(cx, cy, pyxel.mouse_x, pyxel.mouse_y, 1.5)
        pyxel.circ(cx, cy, 2, 1)

    pyxel.run(update, draw)