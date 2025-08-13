"""
@author : Léo Imbert
@created : 15/10/2024
@updated : 13/08/2025
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

def lerp(start:float, end:float, speed:float=0.1)-> float:
    return start + (end - start) * speed

def ease_in_out(value:float)-> float:
    return 3 * value ** 2 - 2 * value ** 3

def wave_motion(value:float, wave_speed:float, amplitude:float, time:int)-> float:
    return value + (math.cos(time / wave_speed)) * amplitude

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

def back_forth_motion(center_x:float, amplitude:float, speed:float, time:int)-> float:
    return center_x + math.sin(time * speed) * amplitude

if __name__ == "__main__":
    import pyxel

    lerp_current = 40
    lerp_target = 160
    wave_points = []
    inf_points = []
    path_follower_x = 75
    path_follower_y = 75
    path_current_point = 0
    path_points = [(75, 75), (175, 75), (175, 110), (75, 110)]

    pyxel.init(228, 128, title="Animations.py Example")
    pyxel.mouse(True)

    def update():
        global lerp_current, lerp_target, path_follower_x, path_follower_y, path_current_point

        #? Lerp
        if pyxel.frame_count % 120 == 0:
            lerp_target = 160 if lerp_target == 40 else 40
        lerp_current = lerp(lerp_current, lerp_target, 0.05)

        #? Path Follower
        path_follower_x, path_follower_y, path_current_point = follow_path(path_follower_x, path_follower_y, 1.5, path_current_point, path_points, True)

    def draw():
        pyxel.cls(12)

        #? Lerp
        pyxel.text(5, 5, "Lerp:", 1)
        pyxel.rectb(40, 5, 8, 4, 9)
        pyxel.rectb(160, 5, 8, 4, 9)
        pyxel.rect(lerp_current, 5, 8, 4, 1)

        #? Ease In Out
        pyxel.text(5, 15, "Ease In/Out:", 1)
        t = (pyxel.frame_count % 120) / 120.0
        eased_t = ease_in_out(t)
        ease_x = 60 + eased_t * 50
        pyxel.line(60, 19, 110, 19, 9)
        pyxel.circ(ease_x, 17, 2, 1)

        #? Wave Motion
        pyxel.text(5, 25, "Wave:", 1)
        wave_y = wave_motion(27, 20, 3, pyxel.frame_count)
        if wave_y not in wave_points:
            wave_points.append(wave_y)
        for y in wave_points:
            pyxel.pset(30, y, 9)
        pyxel.circ(30, wave_y, 2, 1)

        #? Circular Motion
        pyxel.text(5, 35, "Circular:", 1)
        circ_x, circ_y = circular_motion(60, 38, 10, 0.05, pyxel.frame_count)
        pyxel.circb(60, 38, 10, 9)
        pyxel.circ(circ_x, circ_y, 2, 1)

        #? Infinity Motion
        pyxel.text(5, 45, "Infinity:", 1)
        inf_x, inf_y = infinity_motion(120, 48, 30, 0.03, pyxel.frame_count)
        if (inf_x, inf_y) not in inf_points:
            inf_points.append((inf_x, inf_y))
        for x, y in inf_points:
            pyxel.pset(x, y, 9)
        pyxel.circ(inf_x, inf_y, 2, 1)

        #? Path Follower
        pyxel.text(5, 75, "Path Follower:", 1)
        for i in range(len(path_points)):
            next_i = (i + 1) % len(path_points)
            pyxel.line(path_points[i][0], path_points[i][1], path_points[next_i][0], path_points[next_i][1], 9)
            pyxel.circb(path_points[i][0], path_points[i][1], 2, 9)
        pyxel.circ(int(path_follower_x), int(path_follower_y), 3, 1)

    pyxel.run(update, draw)