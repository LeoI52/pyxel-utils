"""
@author : Léo Imbert
@created : 15/10/2024
@updated : 29/11/2025
"""

from tween import Tween
from gui import Text
from vars import *
import random
import pyxel
import math
import time

#? -------------------- TRANSITIONS -------------------- ?#

class Transition:

    def __init__(self, new_scene_id:int, speed:int, transition_color:int, new_camera_x:int=0, new_camera_y:int=0, action=None, load_pyxres:bool=False, load_palette:bool=False):
        self.new_scene_id = new_scene_id
        self.speed = speed
        self.transition_color = transition_color
        self.new_camera_x = new_camera_x
        self.new_camera_y = new_camera_y
        self.action = action
        self.load_pyxres = load_pyxres
        self.load_palette = load_palette
        self.direction = 1

class TransitionDither(Transition):

    def __init__(self, new_scene_id:int, duration:float, transition_color:int, new_camera_x:int=0, new_camera_y:int=0, action=None, load_pyxres:bool=False, load_palette:bool=False, fps:int=60):
        super().__init__(new_scene_id, 1 / (duration / 2 * fps), transition_color, new_camera_x, new_camera_y, action, load_pyxres, load_palette)
        self.dither = 0

    def update(self, pyxel_manager):
        self.dither += self.speed * self.direction

        if self.dither > 1 and self.direction == 1:
            self.direction = -1
            pyxel_manager.change_scene(self.new_scene_id, self.new_camera_x, self.new_camera_y, self.action, self.load_pyxres, self.load_palette)
        if self.dither < 0 and self.direction == -1:
            pyxel_manager.finish_transition()
            return

    def draw(self, pyxel_manager):
        pyxel.dither(self.dither)
        pyxel.rect(pyxel_manager.camera_x, pyxel_manager.camera_y, pyxel.width, pyxel.height, self.transition_color)
        pyxel.dither(1)

class TransitionCircle(Transition):

    def __init__(self, new_scene_id:int, duration:float, transition_color:int, new_camera_x:int=0, new_camera_y:int=0, action=None, load_pyxres:bool=False, load_palette:bool=False, fps:int=60):
        self.radius = 0
        self.max_radius = math.hypot(pyxel.width, pyxel.height) / 2
        super().__init__(new_scene_id, self.max_radius / (duration / 2 * fps), transition_color, new_camera_x, new_camera_y, action, load_pyxres, load_palette)

    def update(self, pyxel_manager):
        self.radius += self.speed * self.direction

        if self.radius > self.max_radius and self.direction == 1:
            self.direction = -1
            pyxel_manager.change_scene(self.new_scene_id, self.new_camera_x, self.new_camera_y, self.action, self.load_pyxres, self.load_palette)
        if self.radius < 0 and self.direction == -1:
            pyxel_manager.finish_transition()
            return

    def draw(self, pyxel_manager):
        pyxel.circ(pyxel_manager.camera_x + pyxel.width / 2, pyxel_manager.camera_y + pyxel.height / 2, self.radius, self.transition_color)

class TransitionClosingDoors(Transition):

    def __init__(self, new_scene_id:int, duration:float, transition_color:int, new_camera_x:int=0, new_camera_y:int=0, action=None, load_pyxres:bool=False, load_palette:bool=False, fps:int=60):
        super().__init__(new_scene_id, pyxel.width / (duration * fps), transition_color, new_camera_x, new_camera_y, action, load_pyxres, load_palette)
        self.w = 0
        self.x = pyxel.width

    def update(self, pyxel_manager):
        self.w += self.speed * self.direction
        self.x -= self.speed * self.direction

        if self.w > pyxel.width // 2 and self.direction == 1:
            self.direction = -1
            pyxel_manager.change_scene(self.new_scene_id, self.new_camera_x, self.new_camera_y, self.action, self.load_pyxres, self.load_palette)
            self.x = pyxel.width // 2
        if self.w < 0 and self.direction == -1:
            pyxel_manager.finish_transition()
            return

    def draw(self, pyxel_manager):
        pyxel.rect(pyxel_manager.camera_x, pyxel_manager.camera_y, self.w, pyxel.height, self.transition_color)
        pyxel.rect(pyxel_manager.camera_x + self.x, pyxel_manager.camera_y, self.w, pyxel.height, self.transition_color)

class TransitionRectangle(Transition):

    def __init__(self, new_scene_id:int, duration:float, transition_color:int, dir:int=LEFT, new_camera_x:int=0, new_camera_y:int=0, action=None, load_pyxres:bool=False, load_palette:bool=False, fps:int=60):
        speed = pyxel.width / (duration / 2 * fps) if dir in [LEFT, RIGHT] else pyxel.height / (duration / 2 * fps)
        super().__init__(new_scene_id, speed, transition_color, new_camera_x, new_camera_y, action, load_pyxres, load_palette)
        self.dir = dir
        self.w = 0
        self.x = pyxel.width if dir == RIGHT else 0
        self.y = pyxel.height if dir == BOTTOM else 0

    def update(self, pyxel_manager):
        if self.dir in [RIGHT, LEFT]:
            self.w += self.speed * self.direction

            if (self.direction == 1 and self.dir == RIGHT) or (self.direction == -1 and self.dir == LEFT):
                self.x = self.x - self.speed if self.dir == RIGHT else self.x + self.speed
            if self.w > pyxel.width and self.direction == 1:
                self.direction = -1
                pyxel_manager.change_scene(self.new_scene_id, self.new_camera_x, self.new_camera_y, self.action, self.load_pyxres, self.load_palette)
                self.x = 0
            if self.w < 0 and self.direction == -1:
                pyxel_manager.finish_transition()
                return
        elif self.dir in [TOP, BOTTOM]:
            self.w += self.speed * self.direction

            if (self.direction == 1 and self.dir == BOTTOM) or (self.direction == -1 and self.dir == TOP):
                self.y = self.y - self.speed if self.dir == BOTTOM else self.y + self.speed
            if self.w > pyxel.height and self.direction == 1:
                self.direction = -1
                pyxel_manager.change_scene(self.new_scene_id, self.new_camera_x, self.new_camera_y, self.action, self.load_pyxres, self.load_palette)
                self.y = 0
            if self.w < 0 and self.direction == -1:
                pyxel_manager.finish_transition()
                return

    def draw(self, pyxel_manager):
        if self.dir in [RIGHT, LEFT]:
            pyxel.rect(pyxel_manager.camera_x + self.x, pyxel_manager.camera_y, self.w, pyxel.height, self.transition_color)
        elif self.dir in [TOP, BOTTOM]:
            pyxel.rect(pyxel_manager.camera_x, pyxel_manager.camera_y + self.y, pyxel.width, self.w, self.transition_color)

class TransitionOuterCircle(Transition):

    def __init__(self, new_scene_id:int, duration:float, transition_color:int, new_camera_x:int=0, new_camera_y:int=0, action=None, load_pyxres:bool=False, load_palette:bool=False, fps:int=60):
        self.start_end = int(math.hypot(pyxel.width, pyxel.height) / 2) + 1
        self.end = self.start_end
        super().__init__(new_scene_id, math.ceil(self.start_end / (duration / 2 * fps)), transition_color, new_camera_x, new_camera_y, action, load_pyxres, load_palette)

    def update(self, pyxel_manager):
        self.end -= self.speed * self.direction

        if self.end < 0 and self.direction == 1:
            self.direction = -1
            pyxel_manager.change_scene(self.new_scene_id, self.new_camera_x, self.new_camera_y, self.action, self.load_pyxres, self.load_palette)
        if self.end > self.start_end and self.direction == -1:
            pyxel_manager.finish_transition()
            return

    def draw(self, pyxel_manager):        
        for radius in range(self.start_end, self.end, -1):
            pyxel.ellib(pyxel_manager.camera_x + pyxel.width / 2 - radius, pyxel_manager.camera_y + pyxel.height / 2 - radius, radius * 2, radius * 2, self.transition_color)
            pyxel.ellib(pyxel_manager.camera_x + pyxel.width / 2 - radius + 1, pyxel_manager.camera_y + pyxel.height / 2 - radius, radius * 2, radius * 2, self.transition_color)

class TransitionTriangle(Transition):

    def __init__(self, new_scene_id:int, duration:float, transition_color:int, new_camera_x:int=0, new_camera_y:int=0, action=None, load_pyxres:bool=False, load_palette:bool=False, fps:int=60):
        super().__init__(new_scene_id, (max(pyxel.width, pyxel.height) * 2.5) / (duration / 2 * fps), transition_color, new_camera_x, new_camera_y, action, load_pyxres, load_palette)
        self.size = 0
        self.angle = 270

    def update(self, pyxel_manager):
        self.size += self.speed * self.direction
        self.angle += 5 * self.direction

        if self.size / 2.5 > max(pyxel.width, pyxel.height) and self.direction == 1:
            self.direction = -1
            pyxel_manager.change_scene(self.new_scene_id, self.new_camera_x, self.new_camera_y, self.action, self.load_pyxres, self.load_palette)
        if self.size < 0 and self.direction == -1:
            pyxel_manager.finish_transition()
            return

    def draw(self, pyxel_manager):
        d = math.sqrt(3) / 3 * self.size
        x1, y1 = pyxel_manager.camera_x + pyxel.width / 2 + d * math.cos(math.radians(0 + self.angle)), pyxel_manager.camera_y + pyxel.height / 2 + d * math.sin(math.radians(0 + self.angle))
        x2, y2 = pyxel_manager.camera_x + pyxel.width / 2 + d * math.cos(math.radians(120 + self.angle)), pyxel_manager.camera_y + pyxel.height / 2 + d * math.sin(math.radians(120 + self.angle))
        x3, y3 = pyxel_manager.camera_x + pyxel.width / 2 + d * math.cos(math.radians(240 + self.angle)), pyxel_manager.camera_y + pyxel.height / 2 + d * math.sin(math.radians(240 + self.angle))
        pyxel.tri(x1, y1, x2, y2, x3, y3, self.transition_color)

class TransitonPixelate(Transition):

    def __init__(self, new_scene_id:int, duration:float, cell_size:int, transition_color:int, new_camera_x:int=0, new_camera_y:int=0, action=None, load_pyxres:bool=False, load_palette:bool=False, fps:int=60):
        super().__init__(new_scene_id, round((pyxel.width // cell_size) * (pyxel.height // cell_size) / (duration / 2 * fps)), transition_color, new_camera_x, new_camera_y, action, load_pyxres, load_palette)
        self.hidden_pixels = [(x, y) for x in range(0, pyxel.width, cell_size) for y in range(0, pyxel.height, cell_size)]
        self.visible_pixels = []
        self.cell_size = cell_size

    def update(self, pyxel_manager):
        if len(self.hidden_pixels) > 0 and self.direction == 1:
            for _ in range(self.speed):
                if len(self.hidden_pixels) <= 0:
                    break
                self.visible_pixels.append(self.hidden_pixels.pop(random.randint(0, len(self.hidden_pixels) - 1)))
        elif self.direction == 1:
            self.direction = -1
            pyxel_manager.change_scene(self.new_scene_id, self.new_camera_x, self.new_camera_y, self.action, self.load_pyxres, self.load_palette)
        elif len(self.visible_pixels) > 0 and self.direction == -1:
            for _ in range(self.speed):
                if len(self.visible_pixels) <= 0:
                    break
                self.hidden_pixels.append(self.visible_pixels.pop(random.randint(0, len(self.visible_pixels) - 1)))
        elif self.direction == -1:
            pyxel_manager.finish_transition()
            return

    def draw(self, pyxel_manager):
        for px, py in self.visible_pixels:
            pyxel.rect(pyxel_manager.camera_x + px, pyxel_manager.camera_y + py, self.cell_size, self.cell_size, self.transition_color)

class TransitionDiagonal(Transition):
    def __init__(self, new_scene_id:int, duration:float, transition_color:int, dir:int=TOP_LEFT, new_camera_x:int=0, new_camera_y:int=0, action=None, load_pyxres:bool=False, load_palette:bool=False, fps:int=60):
        self.max_pos = pyxel.width + pyxel.height
        super().__init__(new_scene_id,  self.max_pos / (duration / 2 * fps), transition_color, new_camera_x, new_camera_y, action, load_pyxres, load_palette)
        self.start = self.end = 0
        self.dir = dir

    def update(self, pyxel_manager):
        if self.direction == 1:   self.end += self.speed
        else:                     self.start += self.speed

        if self.end > self.max_pos and self.direction == 1:
            self.direction = -1
            pyxel_manager.change_scene(self.new_scene_id, self.new_camera_x, self.new_camera_y, self.action, self.load_pyxres, self.load_palette)
        if self.start > self.max_pos and self.direction == -1:
            pyxel_manager.finish_transition()
            return

    def draw(self, pyxel_manager):
        for i in range(round(self.start), round(self.end) + 1):
            if self.dir == TOP_LEFT:
                pyxel.line(pyxel_manager.camera_x, pyxel_manager.camera_y + i, pyxel_manager.camera_x + i, pyxel_manager.camera_y, self.transition_color)
            elif self.dir == TOP_RIGHT:
                pyxel.line(pyxel_manager.camera_x + pyxel.width, pyxel_manager.camera_y + i, pyxel_manager.camera_x + pyxel.width - i, pyxel_manager.camera_y, self.transition_color)
            elif self.dir == BOTTOM_LEFT:
                pyxel.line(pyxel_manager.camera_x, pyxel_manager.camera_y + pyxel.height - i, pyxel_manager.camera_x + i, pyxel_manager.camera_y + pyxel.height, self.transition_color)
            else:
                pyxel.line(pyxel_manager.camera_x + pyxel.width, pyxel_manager.camera_y + pyxel.height - i, pyxel_manager.camera_x + pyxel.width - i, pyxel_manager.camera_y + pyxel.height, self.transition_color)

class TransitionSlice(Transition):
    
    def __init__(self, new_scene_id:int, duration:float, transition_color:int, num_slices:int=8, new_camera_x:int=0, new_camera_y:int=0, action=None, load_pyxres:bool=False, load_palette:bool=False, fps:int=60):
        self.num_slices = num_slices
        self.slice_height = pyxel.height // num_slices
        super().__init__(new_scene_id, pyxel.width / (duration / 2 * fps), transition_color, new_camera_x, new_camera_y, action, load_pyxres, load_palette)
        self.position = 0
    
    def update(self, pyxel_manager):
        self.position += self.speed * self.direction
        
        if self.position > pyxel.width and self.direction == 1:
            self.direction = -1
            pyxel_manager.change_scene(self.new_scene_id, self.new_camera_x, self.new_camera_y, self.action, self.load_pyxres, self.load_palette)
        if self.position < 0 and self.direction == -1:
            pyxel_manager.finish_transition()
    
    def draw(self, pyxel_manager):
        for i in range(self.num_slices):
            y = pyxel_manager.camera_y + i * self.slice_height
            
            if i % 2 == 0:
                pyxel.rect(pyxel_manager.camera_x, y, self.position, self.slice_height, self.transition_color)
            else:
                pyxel.rect(pyxel_manager.camera_x + pyxel.width - self.position, y, self.position, self.slice_height, self.transition_color)

#? -------------------- SCENE MANAGER -------------------- ?#

class PyxelManager:

    def __init__(self, width:int, height:int, scenes:list, default_scene_id:int=0, fps:int=60, fullscreen:bool=False, mouse:bool=False, quit_key:int=pyxel.KEY_ESCAPE, camera_x:int=0, camera_y:int=0, debug_background_color:int=0, debug_text_color:int=7):
        
        self.__scenes_dict = {scene.id:scene for scene in scenes}
        self.__current_scene = self.__scenes_dict[default_scene_id]
        self.__current_scene_id = default_scene_id
        self.__transition = None

        self.__cam_x = self.__cam_tx = camera_x
        self.__cam_y = self.__cam_ty = camera_y
        self.__cam_interpolation = 0.1
        self.__cam_bounds = (-float("inf"), -float("inf"), float("inf"), float("inf"))
        self.__shake_amount = 0
        self.__shake_decay = 0

        self.__fps = fps
        self.__previous_frame_time = time.time()
        self.__current_fps = 0

        self.debug = False
        self.debug_background_color = debug_background_color
        self.debug_text_color = debug_text_color

        pyxel.init(width, height, fps=fps, quit_key=quit_key)
        pyxel.fullscreen(fullscreen)
        pyxel.mouse(mouse)

        if self.__current_scene.pyxres_path:
            pyxel.load(self.__current_scene.pyxres_path)
        pyxel.colors.from_list(self.__current_scene.palette)
        pyxel.title(self.__current_scene.title)
        pyxel.screen_mode(self.__current_scene.screen_mode)

    @property
    def camera_x(self)-> int|float:
        return self.__cam_x
    
    @property
    def camera_y(self)-> int|float:
        return self.__cam_y

    @property
    def mouse_x(self)-> int:
        return self.__cam_x + pyxel.mouse_x
    
    @property
    def mouse_y(self)-> int:
        return self.__cam_y + pyxel.mouse_y
    
    @property
    def current_scene_id(self)-> int:
        return self.__current_scene_id

    def set_camera(self, new_camera_x:int, new_camera_y:int):
        self.__cam_x = self.__cam_tx = max(self.__cam_bounds[0], min(new_camera_x, self.__cam_bounds[2] - pyxel.width))
        self.__cam_y = self.__cam_ty = max(self.__cam_bounds[1], min(new_camera_y, self.__cam_bounds[3] - pyxel.height))

    def move_camera(self, new_camera_x:int, new_camera_y:int, interpolation:float=0.1):
        self.__cam_tx = max(self.__cam_bounds[0], min(new_camera_x, self.__cam_bounds[2] - pyxel.width))
        self.__cam_ty = max(self.__cam_bounds[1], min(new_camera_y, self.__cam_bounds[3] - pyxel.height))
        self.__cam_interpolation = interpolation

    def set_camera_bounds(self, min_x:int, min_y:int, max_x:int, max_y:int):
        self.__cam_bounds = (min_x, min_y, max_x, max_y)
        self.__cam_tx = max(self.__cam_bounds[0], min(self.__cam_tx, self.__cam_bounds[2] - pyxel.width))
        self.__cam_ty = max(self.__cam_bounds[1], min(self.__cam_ty, self.__cam_bounds[3] - pyxel.height))
        self.__cam_x = max(self.__cam_bounds[0], min(self.__cam_x, self.__cam_bounds[2] - pyxel.width))
        self.__cam_y = max(self.__cam_bounds[1], min(self.__cam_y, self.__cam_bounds[3] - pyxel.height))

    def shake_camera(self, amount:int, decay:float):
        self.__shake_amount = amount
        self.__shake_decay = decay

    def change_scene(self, new_scene_id:int, new_camera_x:int=0, new_camera_y:int=0, action=None, load_pyxres:bool=False, load_palette:bool=False):
        self.set_camera(new_camera_x, new_camera_y)

        self.__current_scene = self.__scenes_dict[new_scene_id]
        self.__current_scene_id = new_scene_id
        if action:
            action()

        if self.__current_scene.pyxres_path and load_pyxres:
            pyxel.load(self.__current_scene.pyxres_path)
        if load_palette:
            pyxel.colors.from_list(self.__current_scene.palette)
        pyxel.title(self.__current_scene.title)
        pyxel.screen_mode(self.__current_scene.screen_mode)

    def change_scene_transition(self, transition:Transition):
        self.__transition = transition

    def finish_transition(self):
        self.__transition = None

    def apply_palette_effect(self, effect_function, **kwargs):
        pyxel.colors.from_list(effect_function(self.__current_scene.palette, kwargs))

    def reset_palette(self):
        pyxel.colors.from_list(self.__current_scene.palette)

    def update(self):
        if self.__transition:
            self.__transition.update(self)

        self.__cam_x += (self.__cam_tx - self.__cam_x) * self.__cam_interpolation
        self.__cam_y += (self.__cam_ty - self.__cam_y) * self.__cam_interpolation

        if self.__shake_amount > 0:
            a = self.__shake_amount
            pyxel.camera(self.__cam_x + random.uniform(-a, a), self.__cam_y + random.uniform(-a, a))
            self.__shake_amount = max(0, self.__shake_amount - self.__shake_decay)
        else:
            pyxel.camera(self.__cam_x, self.__cam_y)

        if not self.__transition:
            self.__current_scene.update()

    def draw(self):
        self.__current_scene.draw()
        if self.__transition:
            self.__transition.draw(self)

        if self.debug:
            pyxel.rect(self.__cam_x + 1, self.__cam_y + 1, 66, 27, self.debug_background_color)
            pyxel.text(self.__cam_x + 3, self.__cam_y + 3, f"Scene[{self.__current_scene.id}]", self.debug_text_color)
            pyxel.text(self.__cam_x + 3, self.__cam_y + 9, f"Screen[{pyxel.mouse_x},{pyxel.mouse_y}]", self.debug_text_color)
            pyxel.text(self.__cam_x + 3, self.__cam_y + 15, f"World[{self.mouse_x:.0f},{self.mouse_y:.0f}]", self.debug_text_color)
            pyxel.text(self.__cam_x + 3, self.__cam_y + 21, f"Fps[{self.__current_fps:.0f}]", self.debug_text_color)

        if pyxel.frame_count % self.__fps == 0:
            self.__current_fps = 1 / (time.time() - self.__previous_frame_time)
        self.__previous_frame_time = time.time()

    def run(self):
        pyxel.run(self.update, self.draw)

class Scene:

    def __init__(self, id:int, title:str, update, draw, pyxres_path:str=None, palette:list=DEFAULT_PYXEL_COLORS, screen_mode:int=0):
        self.id = id
        self.title = title
        self.update = update
        self.draw = draw
        self.pyxres_path = pyxres_path
        self.palette = palette
        self.screen_mode = screen_mode

#? -------------------- CUTSCENES -------------------- ?#

class CutsceneAction:

    def __init__(self, duration:float, update_action=None, draw_action=None, fps:int=60):
        self.duration = duration
        self.update_action = update_action
        self.draw_action = draw_action
        self.elapsed = 0
        self.dt = 1 / fps
        self.finished = False

    def update(self):
        if self.finished:
            return
        
        if self.update_action:
            self.update_action(self)

        self.elapsed += self.dt
        if self.elapsed >= self.duration:
            self.finished = True

    def draw(self):
        if self.draw_action and not self.finished:
            self.draw_action(self)

class Cutscene:

    def __init__(self, actions:list=None):
        self.actions = actions or []
        self.action_index = 0
        self.active = False
        self.finished = False

    def add_action(self, action:CutsceneAction):
        self.actions.append(action)

    def start(self):
        self.active = True
        self.finished = False
        self.action_index = 0
        for action in self.actions:
            action.elapsed = 0
            action.finished = False

    def update(self):
        if not self.active or self.finished:
            return
        
        if self.action_index < len(self.actions):
            action = self.actions[self.action_index]
            action.update()
            if action.finished:
                self.action_index += 1
        else:
            self.finished = True
            self.active = False

    def draw(self):
        if not self.active or self.finished:
            return
        
        if self.action_index < len(self.actions):
            action = self.actions[self.action_index]
            action.draw()

def parallel_action(actions:list, duration:float, fps:int=60):
    
    def update(action):
        for act in actions:
            act.update()

    def draw(action):
        for act in actions:
            act.draw()

    return CutsceneAction(duration, update, draw, fps)

def wait_action(duration:float, fps:int=60):
    return CutsceneAction(duration, fps=fps)

def tween_camera_action(manager:PyxelManager, start_x:int, start_y:int, end_x:int, end_y:int, duration:float, easing=None, fps:int=60):
    tween_x = Tween(start_x, end_x, duration, True, easing, fps)
    tween_y = Tween(start_y, end_y, duration, True, easing, fps)

    def update(action):
        manager.set_camera(tween_x.update(), tween_y.update())

    return CutsceneAction(duration, update, fps=fps)

def shake_camera_action(manager:PyxelManager, amount:int, decay:float, duration:float, fps:int=60):

    def update(action):
        if action.elapsed <= 0:
            manager.shake_camera(amount, decay)

    return CutsceneAction(duration, update, fps=fps)

def palette_effect_action(manager:PyxelManager, effect_function, duration:float, fps:int=60, **kwargs):

    def update(action):
        manager.apply_palette_effect(effect_function, **kwargs)
        if action.finished:
            manager.reset_palette()

    return CutsceneAction(duration, update, fps)

def tween_move_object_action(obj, start_x:float, start_y:float, end_x:float, end_y:float, duration:float, easing=None, fps:int=60):
    tween_x = Tween(start_x, end_x, duration, True, easing, fps)
    tween_y = Tween(start_y, end_y, duration, True, easing, fps)

    def update(action):
        obj.x = tween_x.update()
        obj.y = tween_y.update()

    return CutsceneAction(duration, update, fps)

def typewriter_text_action(text:Text, duration:float, fps:int=60):
    visible_chars = [0]
    t = text.text
    total_chars = len(text.text) + 1

    def update(action):
        text.update()
        progress = min(action.elapsed / duration, 1.0)
        visible_chars[0] = min(int(total_chars * progress), len(t))

    def draw(action):
        text.text = t[:visible_chars[0]]
        text.initialize()
        text.draw()

    return CutsceneAction(duration, update, draw, fps)

#? -------------------- EXAMPLE -------------------- ?#

if __name__ == "__main__":
    from tween import ease_out_quint

    def update_1():
        if pyxel.btnp(pyxel.KEY_B):
            pm.debug = not pm.debug
        if pyxel.btnp(pyxel.KEY_SPACE):
            pm.change_scene_transition(TransitionDiagonal(1, 2, 1, BOTTOM_RIGHT))
        if pyxel.btnp(pyxel.KEY_C):
            pm.change_scene_transition(TransitionTriangle(2, 4, 1, action=lambda: cutscene.start()))

    def draw_1():
        pyxel.cls(10)

    def update_2():
        if pyxel.btnp(pyxel.KEY_B):
            pm.debug = not pm.debug
        if pyxel.btnp(pyxel.KEY_SPACE):
            pm.change_scene_transition(TransitionTriangle(0, 1, 1))

    def draw_2():
        pyxel.cls(3)

    def update_3():
        cutscene.update()

        if cutscene.finished:
            pm.change_scene_transition(TransitionClosingDoors(0, 4, 1))

    def draw_3():
        pyxel.cls(12)

        pyxel.rect(10, 10, 50, 50, 8)

        cutscene.draw()

    s1 = Scene(0, "Game.py Example - Scene 1", update_1, draw_1)
    s2 = Scene(1, "Game.py Example - Scene 2", update_2, draw_2)
    s3 = Scene(2, "Game.py Example - Scene 3", update_3, draw_3)
    pm = PyxelManager(228, 128, [s1, s2, s3], mouse=True)

    cutscene = Cutscene()
    t = Text("Hello", -48, -48, 8, FONT_DEFAULT, 2, relative=False)

    cutscene.add_action(wait_action(1))
    cutscene.add_action(tween_camera_action(pm, 0, 0, -50, -50, 2, ease_out_quint))
    cutscene.add_action(shake_camera_action(pm, 5, 0.5, 1))
    cutscene.add_action(typewriter_text_action(t, 5))
    cutscene.add_action(wait_action(0.5))

    pm.run()