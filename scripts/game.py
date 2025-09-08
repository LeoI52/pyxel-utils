"""
@author : Léo Imbert
@created : 15/10/2024
@updated : 08/09/2025
"""

from vars import DEFAULT_PYXEL_COLORS, LEFT, RIGHT, TOP, BOTTOM
import random
import pyxel
import math
import time
import sys
import os

class Transition:

    def __init__(self, new_scene_id:int, speed:int, transition_color:int, new_camera_x:int=0, new_camera_y:int=0, action=None):
        self.new_scene_id = new_scene_id
        self.speed = speed
        self.transition_color = transition_color
        self.new_camera_x = new_camera_x
        self.new_camera_y = new_camera_y
        self.action = action
        self.direction = 1

class TransitionDither(Transition):

    def __init__(self, new_scene_id:int, speed:int, transition_color:int, new_camera_x:int=0, new_camera_y:int=0, action=None):
        super().__init__(new_scene_id, speed, transition_color, new_camera_x, new_camera_y, action)
        self.dither = 0

    def handle(self, pyxel_manager):
        self.dither += self.speed * self.direction

        if self.dither > 1 and self.direction == 1:
            self.direction = -1
            pyxel_manager.change_scene(self.new_scene_id, self.new_camera_x, self.new_camera_y, self.action)
        if self.dither < 0 and self.direction == -1:
            pyxel_manager.transition = None
            return
        pyxel.dither(self.dither)
        pyxel.rect(pyxel_manager.camera_x, pyxel_manager.camera_y, pyxel.width, pyxel.height, self.transition_color)
        pyxel.dither(1)

class TransitionCircle(Transition):

    def __init__(self, new_scene_id:int, speed:int, transition_color:int, new_camera_x:int=0, new_camera_y:int=0, action=None):
        super().__init__(new_scene_id, speed, transition_color, new_camera_x, new_camera_y, action)
        self.radius = 0
        self.max_radius = math.hypot(pyxel.width, pyxel.height) / 2

    def handle(self, pyxel_manager):
        self.radius += self.speed * self.direction

        if self.radius > self.max_radius and self.direction == 1:
            self.direction = -1
            pyxel_manager.change_scene(self.new_scene_id, self.new_camera_x, self.new_camera_y, self.action)
        if self.radius < 0 and self.direction == -1:
            pyxel_manager.transition = None
            return
        pyxel.circ(pyxel_manager.camera_x + pyxel.width / 2, pyxel_manager.camera_y + pyxel.height / 2, self.radius, self.transition_color)

class TransitionClosingDoors(Transition):

    def __init__(self, pyxel_manager, new_scene_id:int, speed:int, transition_color:int, new_camera_x:int=0, new_camera_y:int=0, action=None):
        super().__init__(new_scene_id, speed, transition_color, new_camera_x, new_camera_y, action)
        self.w = 0
        self.x = pyxel_manager.camera_x + pyxel.width

    def handle(self, pyxel_manager):
        self.w += self.speed * self.direction
        self.x -= self.speed * self.direction

        if self.w > pyxel.width // 2 and self.direction == 1:
            self.direction = -1
            pyxel_manager.change_scene(self.new_scene_id, self.new_camera_x, self.new_camera_y, self.action)
        if self.w < 0 and self.direction == -1:
            pyxel_manager.transition = None
            return
        pyxel.rect(pyxel_manager.camera_x, pyxel_manager.camera_y, self.w, pyxel.height, self.transition_color)
        pyxel.rect(self.x, pyxel_manager.camera_y, self.w, pyxel.height, self.transition_color)

class TransitionRectangle(Transition):

    def __init__(self, pyxel_manager, new_scene_id:int, speed:int, transition_color:int, dir:int=LEFT, new_camera_x:int=0, new_camera_y:int=0, action=None):
        super().__init__(new_scene_id, speed, transition_color, new_camera_x, new_camera_y, action)
        self.dir = dir
        self.w = 0
        self.x = pyxel_manager.camera_x + pyxel.width if dir == RIGHT else pyxel_manager.camera_x
        self.y = pyxel_manager.camera_y + pyxel.height if dir == BOTTOM else pyxel_manager.camera_y

    def handle(self, pyxel_manager):
        if self.dir in [RIGHT, LEFT]:
            self.w += self.speed * self.direction

            if (self.direction == 1 and self.dir == RIGHT) or (self.direction == -1 and self.dir == LEFT):
                self.x = self.x - self.speed if self.dir == RIGHT else self.x + self.speed
            if self.w > pyxel.width and self.direction == 1:
                self.direction = -1
                pyxel_manager.change_scene(self.new_scene_id, self.new_camera_x, self.new_camera_y, self.action)
            if self.w < 0 and self.direction == -1:
                pyxel_manager.transition = None
                return
            
            pyxel.rect(self.x, pyxel_manager.camera_y, self.w, pyxel.height, self.transition_color)
        elif self.dir in [TOP, BOTTOM]:
            self.w += self.speed * self.direction

            if (self.direction == 1 and self.dir == BOTTOM) or (self.direction == -1 and self.dir == TOP):
                self.y = self.y - self.speed if self.dir == BOTTOM else self.y + self.speed
            if self.w > pyxel.height and self.direction == 1:
                self.direction = -1
                pyxel_manager.change_scene(self.new_scene_id, self.new_camera_x, self.new_camera_y, self.action)
            if self.w < 0 and self.direction == -1:
                pyxel_manager.transition = None
                return
            
            pyxel.rect(pyxel_manager.camera_x, self.y, pyxel.width, self.w, self.transition_color)

class TransitionOuterCircle(Transition):

    def __init__(self, new_scene_id:int, speed:int, transition_color:int, new_camera_x:int=0, new_camera_y:int=0, action=None):
        super().__init__(new_scene_id, speed, transition_color, new_camera_x, new_camera_y, action)
        self.start_end = int(math.hypot(pyxel.width, pyxel.height) / 2) + 1
        self.end = self.start_end

    def handle(self, pyxel_manager):
        self.end -= self.speed * self.direction

        if self.end < 0 and self.direction == 1:
            self.direction = -1
            pyxel_manager.change_scene(self.new_scene_id, self.new_camera_x, self.new_camera_y, self.action)
        if self.end > self.start_end and self.direction == -1:
            pyxel_manager.transition = None
            return
        
        for radius in range(self.start_end, self.end, -1):
            pyxel.ellib(pyxel_manager.camera_x + pyxel.width / 2 - radius, pyxel_manager.camera_y + pyxel.height / 2 - radius, radius * 2, radius * 2, self.transition_color)
            pyxel.ellib(pyxel_manager.camera_x + pyxel.width / 2 - radius + 1, pyxel_manager.camera_y + pyxel.height / 2 - radius, radius * 2, radius * 2, self.transition_color)

class TransitionTriangle(Transition):

    def __init__(self, new_scene_id:int, speed:int, transition_color:int, new_camera_x:int=0, new_camera_y:int=0, action=None):
        super().__init__(new_scene_id, speed, transition_color, new_camera_x, new_camera_y, action)
        self.size = 0
        self.angle = 270

    def handle(self, pyxel_manager):
        self.size += self.speed * self.direction
        self.angle += 5 * self.direction

        if self.size / 2.5 > max(pyxel.width, pyxel.height) and self.direction == 1:
            self.direction = -1
            pyxel_manager.change_scene(self.new_scene_id, self.new_camera_x, self.new_camera_y, self.action)
        if self.size < 0 and self.direction == -1:
            pyxel_manager.transition = None
            return
        d = math.sqrt(3) / 3 * self.size
        x1, y1 = pyxel_manager.camera_x + pyxel.width / 2 + d * math.cos(math.radians(0 + self.angle)), pyxel_manager.camera_y + pyxel.height / 2 + d * math.sin(math.radians(0 + self.angle))
        x2, y2 = pyxel_manager.camera_x + pyxel.width / 2 + d * math.cos(math.radians(120 + self.angle)), pyxel_manager.camera_y + pyxel.height / 2 + d * math.sin(math.radians(120 + self.angle))
        x3, y3 = pyxel_manager.camera_x + pyxel.width / 2 + d * math.cos(math.radians(240 + self.angle)), pyxel_manager.camera_y + pyxel.height / 2 + d * math.sin(math.radians(240 + self.angle))
        pyxel.tri(x1, y1, x2, y2, x3, y3, self.transition_color)

class PyxelManager:

    def __init__(self, width:int, height:int, scenes:list, default_scene_id:int=0, fps:int=60, fullscreen:bool=False, mouse:bool=False, quit_key:int=pyxel.KEY_ESCAPE, camera_x:int=0, camera_y:int=0, debug_background_color:int=0, debug_text_color:int=7):
        
        self.__scenes_dict = {scene.id:scene for scene in scenes}
        self.__current_scene = self.__scenes_dict[default_scene_id]
        self.transition = None

        self.__cam_x = self.__cam_tx = camera_x
        self.__cam_y = self.__cam_ty = camera_y
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
            pyxel.load(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), self.__current_scene.pyxres_path))
        pyxel.title(self.__current_scene.title)
        pyxel.screen_mode(self.__current_scene.screen_mode)
        pyxel.colors.from_list(self.__current_scene.palette)

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
    
    def set_camera(self, new_camera_x:int, new_camera_y:int):
        self.__cam_x = self.__cam_tx = max(self.__cam_bounds[0], min(new_camera_x, self.__cam_bounds[2] - pyxel.width))
        self.__cam_y = self.__cam_ty = max(self.__cam_bounds[1], min(new_camera_y, self.__cam_bounds[3] - pyxel.height))

    def move_camera(self, new_camera_x:int, new_camera_y:int):
        self.__cam_tx = max(self.__cam_bounds[0], min(new_camera_x, self.__cam_bounds[2] - pyxel.width))
        self.__cam_ty = max(self.__cam_bounds[1], min(new_camera_y, self.__cam_bounds[3] - pyxel.height))

    def set_camera_bounds(self, min_x:int, min_y:int, max_x:int, max_y:int):
        self.__cam_bounds = (min_x, min_y, max_x, max_y)
        self.__cam_tx = max(self.__cam_bounds[0], min(self.__cam_tx, self.__cam_bounds[2] - pyxel.width))
        self.__cam_ty = max(self.__cam_bounds[1], min(self.__cam_ty, self.__cam_bounds[3] - pyxel.height))
        self.__cam_x = max(self.__cam_bounds[0], min(self.__cam_x, self.__cam_bounds[2] - pyxel.width))
        self.__cam_y = max(self.__cam_bounds[1], min(self.__cam_y, self.__cam_bounds[3] - pyxel.height))

    def shake_camera(self, amount:int, decay:float):
        self.__shake_amount = amount
        self.__shake_decay = decay

    def change_scene(self, new_scene_id:int, new_camera_x:int=0, new_camera_y:int=0, action=None):
        self.set_camera(new_camera_x, new_camera_y)

        self.__current_scene = self.__scenes_dict.get(new_scene_id, 0)
        if action:
            action()

        if self.__current_scene.pyxres_path:
            pyxel.load(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), self.__current_scene.pyxres_path))
        pyxel.title(self.__current_scene.title)
        pyxel.screen_mode(self.__current_scene.screen_mode)
        pyxel.colors.from_list(self.__current_scene.palette)

    def change_scene_transition(self, transition:Transition):
        self.transition = transition

    def apply_palette_effect(self, effect_function, **kwargs):
        pyxel.colors.from_list(effect_function(self.__current_scene.palette, kwargs))

    def reset_palette(self):
        pyxel.colors.from_list(self.__current_scene.palette)

    def update(self):
        self.__cam_x += (self.__cam_tx - self.__cam_x) * 0.1
        self.__cam_y += (self.__cam_ty - self.__cam_y) * 0.1

        if self.__shake_amount > 0:
            a = self.__shake_amount
            pyxel.camera(self.__cam_x + random.uniform(-a, a), self.__cam_y + random.uniform(-a, a))
            self.__shake_amount = max(0, self.__shake_amount - self.__shake_decay)
        else:
            pyxel.camera(self.__cam_x, self.__cam_y)

        if not self.transition:
            self.__current_scene.update()

    def draw(self):
        self.__current_scene.draw()
        if self.transition:
            self.transition.handle(self)

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

class CutsceneAction:

    def __init__(self, duration:float, update_action=None, draw_action=None):
        self.duration = duration
        self.update_action = update_action
        self.draw_action = draw_action
        self.elapsed = 0
        self.finished = False

    def update(self, dt:float):
        if self.finished:
            return
        
        if self.update_action:
            self.update_action(self, dt)

        self.elapsed += dt
        if self.elapsed >= self.duration:
            self.finished = True

    def draw(self):
        if self.draw_action and not self.finished:
            self.draw_action(self)

class Cutscene:

    def __init__(self):
        self.actions = []
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

    def update(self, dt:float):
        if not self.active or self.finished:
            return
        
        if self.action_index < len(self.actions):
            action = self.actions[self.action_index]
            action.update(dt)
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


def wait_action(duration: float):
    return CutsceneAction(duration)

def screen_shake_action(pyxel_manager, amount: int, decay: float, duration: float):
    def update(a, dt):
        pyxel_manager.shake_camera(amount, decay)
    return CutsceneAction(duration, update_action=update)

def show_text_action(text: str, duration: float, x: int, y: int, color: int = 7):
    def draw(a):
        pyxel.text(x, y, text, color)
    return CutsceneAction(duration, draw_action=draw)

if __name__ == "__main__":
    def update_1():
        if pyxel.btnp(pyxel.KEY_B):
            pm.debug = not pm.debug
        if pyxel.btnp(pyxel.KEY_SPACE):
            pm.change_scene_transition(TransitionRectangle(pm, 1, 2, 1, RIGHT))
        if pyxel.btnp(pyxel.KEY_C):
            pm.change_scene_transition(TransitionTriangle(2, 5, 1, action=lambda: cutscene.start()))

    def draw_1():
        pyxel.cls(10)

    def update_2():
        if pyxel.btnp(pyxel.KEY_B):
            pm.debug = not pm.debug
        if pyxel.btnp(pyxel.KEY_SPACE):
            pm.change_scene_transition(TransitionDither(0, 0.05, 1))

    def draw_2():
        pyxel.cls(3)

    def update_3():
        cutscene.update(1/60)

        if cutscene.finished:
            pm.change_scene_transition(TransitionClosingDoors(pm, 0, 5, 1))

    def draw_3():
        pyxel.cls(12)

        pyxel.rect(10, 10, 50, 50, 8)

        cutscene.draw()

    s1 = Scene(0, "Game.py Example - Scene 1", update_1, draw_1)
    s2 = Scene(1, "Game.py Example - Scene 2", update_2, draw_2)
    s3 = Scene(2, "Game.py Example - Scene 3", update_3, draw_3)
    pm = PyxelManager(228, 128, [s1, s2, s3], mouse=True)

    cutscene = Cutscene()
    cutscene.add_action(show_text_action("Our hero enters...", 2, 10, 10, 7))
    cutscene.add_action(screen_shake_action(pm, 4, 0.2, 1))
    cutscene.add_action(wait_action(1))
    cutscene.add_action(show_text_action("A new journey begins!", 2, 10, 30, 10))

    pm.run()