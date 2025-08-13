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

def wave_motion(value:float, wave_speed:float, wave_height:float, time:int)-> float:
    return value + (math.cos(time / wave_speed)) * wave_height

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
    x = center_x + math.sin(t) * size
    y = center_y + math.sin(t * 2) * size / 2
    return x, y

def back_forth_motion(center_x:float, amplitude:float, speed:float, time:int)-> float:
    return center_x + math.sin(time * speed) * amplitude
