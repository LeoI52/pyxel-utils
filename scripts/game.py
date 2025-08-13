"""
@author : Léo Imbert
@created : 15/10/2024
@updated : 13/08/2025

TODO :
- Debug Mode
"""

from .vars import DEFAULT_PYXEL_COLORS
import random
import pyxel
import math
import sys
import os

class PyxelManager:

    def __init__(self, width:int, height:int, scenes:list, default_scene_id:int=0, fps:int=60, fullscreen:bool=False, mouse:bool=False, quit_key:int=pyxel.KEY_ESCAPE, camera_x:int=0, camera_y:int=0):
        
        self.__fps = fps
        self.__scenes_dict = {scene.id:scene for scene in scenes}
        self.__current_scene = self.__scenes_dict.get(default_scene_id, 0)
        self.__transition = {}

        self.__cam_x = self.__cam_tx = camera_x
        self.__cam_y = self.__cam_ty = camera_y
        self.__shake_amount = 0
        self.__sub_shake_amount = 0

        pyxel.init(width, height, fps=self.__fps, quit_key=quit_key)
        pyxel.fullscreen(fullscreen)
        pyxel.mouse(mouse)

        if self.__current_scene.pyxres_path:
            pyxel.load(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), self.__current_scene.pyxres_path))
        pyxel.title(self.__current_scene.title)
        pyxel.screen_mode(self.__current_scene.screen_mode)
        pyxel.colors.from_list(self.__current_scene.palette)

    @property
    def camera_x(self)-> int:
        return self.__cam_x
    
    @property
    def camera_y(self)-> int:
        return self.__cam_y

    @property
    def mouse_x(self)-> int:
        return self.__cam_x + pyxel.mouse_x
    
    @property
    def mouse_y(self)-> int:
        return self.__cam_y + pyxel.mouse_y
    
    @property
    def fps(self)-> int:
        return self.__fps
    
    def set_camera(self, new_camera_x:int, new_camera_y:int):
        self.__cam_x = self.__cam_tx = new_camera_x
        self.__cam_y = self.__cam_ty = new_camera_y

    def move_camera(self, new_camera_x:int, new_camera_y:int):
        self.__cam_tx = new_camera_x
        self.__cam_ty = new_camera_y

    def shake_camera(self, amount:int, sub_amount:float):
        self.__shake_amount = amount
        self.__sub_shake_amount = sub_amount

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

    def change_scene_dither(self, new_scene_id:int, speed:float, transition_color:int, new_camera_x:int=0, new_camera_y:int=0, action=None):
        self.__transition = {
            "type":"dither",
            "direction":1,
            "new_scene_id":new_scene_id,
            "speed":speed,
            "transition_color":transition_color,
            "new_camera_x":new_camera_x,
            "new_camera_y":new_camera_y,
            "dither":0,
            "action":action
        }

    def change_scene_circle(self, new_scene_id:int, speed:int, transition_color:int, new_camera_x:int=0, new_camera_y:int=0, action=None):
        self.__transition = {
            "type":"circle",
            "direction":1,
            "new_scene_id":new_scene_id,
            "speed":speed,
            "transition_color":transition_color,
            "new_camera_x":new_camera_x,
            "new_camera_y":new_camera_y,
            "radius":0,
            "max_radius":((pyxel.width ** 2 + pyxel.height ** 2) ** 0.5) / 2,
            "action":action
        }

    def change_scene_closing_doors(self, new_scene_id:int, speed:int, transition_color:int, new_camera_x:int=0, new_camera_y:int=0, action=None):
        self.__transition = {
            "type":"closing_doors",
            "direction":1,
            "new_scene_id":new_scene_id,
            "speed":speed,
            "transition_color":transition_color,
            "new_camera_x":new_camera_x,
            "new_camera_y":new_camera_y,
            "w":0,
            "x":self.__cam_x + pyxel.width,
            "action":action
        }

    def change_scene_rectangle_right_left(self, new_scene_id:int, speed:int, transition_color:int, new_camera_x:int=0, new_camera_y:int=0, action=None):
        self.__transition = {
            "type":"rectangle_right_left",
            "direction":1,
            "new_scene_id":new_scene_id,
            "speed":speed,
            "transition_color":transition_color,
            "new_camera_x":new_camera_x,
            "new_camera_y":new_camera_y,
            "x":self.__cam_x + pyxel.width,
            "w":0,
            "action":action
        }

    def change_scene_rectangle_left_right(self, new_scene_id:int, speed:int, transition_color:int, new_camera_x:int=0, new_camera_y:int=0, action=None):
        self.__transition = {
            "type":"rectangle_left_right",
            "direction":1,
            "new_scene_id":new_scene_id,
            "speed":speed,
            "transition_color":transition_color,
            "new_camera_x":new_camera_x,
            "new_camera_y":new_camera_y,
            "x":self.__cam_x,
            "w":0,
            "action":action
        }

    def change_scene_outer_circle(self, new_scene_id:int, speed:int, transition_color:int, new_camera_x:int=0, new_camera_y:int=0, action=None):
        self.__transition = {
            "type":"outer_circle",
            "direction":1,
            "new_scene_id":new_scene_id,
            "speed":speed,
            "transition_color":transition_color,
            "new_camera_x":new_camera_x,
            "new_camera_y":new_camera_y,
            "start_end":int(((pyxel.width ** 2 + pyxel.height ** 2) ** 0.5) / 2) + 1,
            "end":int(((pyxel.width ** 2 + pyxel.height ** 2) ** 0.5) / 2) + 1,
            "action":action
        }

    def change_scene_triangle(self, new_scene_id:int, speed:int, transition_color:int, rotation_speed:int, new_camera_x:int=0, new_camera_y:int=0, action=None):
        self.__transition = {
            "type":"triangle",
            "direction":1,
            "new_scene_id":new_scene_id,
            "speed":speed,
            "transition_color":transition_color,
            "rotation_speed":rotation_speed,
            "new_camera_x":new_camera_x,
            "new_camera_y":new_camera_y,
            "size":0,
            "angle":270,
            "action":action
        }

    def apply_palette_effect(self, effect_function, **kwargs):
        pyxel.colors.from_list(effect_function(self.__current_scene.palette, kwargs))

    def reset_palette(self):
        pyxel.colors.from_list(self.__current_scene.palette)

    def handle_transitions(self):

        if self.__transition.get("type") == "dither":
            self.__transition["dither"] += self.__transition["speed"] * self.__transition["direction"]

            if self.__transition["dither"] > 1 and self.__transition["direction"] == 1:
                self.__transition["direction"] = -1
                self.change_scene(self.__transition["new_scene_id"], self.__transition["new_camera_x"], self.__transition["new_camera_y"], self.__transition["action"])
            if self.__transition["dither"] < 0 and self.__transition["direction"] == -1:
                self.__transition = {}
                return
            pyxel.dither(self.__transition["dither"])
            pyxel.rect(self.__cam_x, self.__cam_y, pyxel.width, pyxel.height, self.__transition["transition_color"])
            pyxel.dither(1)

        elif self.__transition.get("type") == "circle":
            self.__transition["radius"] += self.__transition["speed"] * self.__transition["direction"]

            if self.__transition["radius"] > self.__transition["max_radius"] and self.__transition["direction"] == 1:
                self.__transition["direction"] = -1
                self.change_scene(self.__transition["new_scene_id"], self.__transition["new_camera_x"], self.__transition["new_camera_y"], self.__transition["action"])
            if self.__transition["radius"] < 0 and self.__transition["direction"] == -1:
                self.__transition = {}
                return
            pyxel.circ(self.__cam_x + pyxel.width / 2, self.__cam_y + pyxel.height / 2, self.__transition["radius"], self.__transition["transition_color"])

        elif self.__transition.get("type") == "closing_doors":
            self.__transition["w"] += self.__transition["speed"] * self.__transition["direction"]
            self.__transition["x"] -= self.__transition["speed"] * self.__transition["direction"]

            if self.__transition["w"] > pyxel.width // 2 and self.__transition["direction"] == 1:
                self.__transition["direction"] = -1
                self.change_scene(self.__transition["new_scene_id"], self.__transition["new_camera_x"], self.__transition["new_camera_y"], self.__transition["action"])
            if self.__transition["w"] < 0 and self.__transition["direction"] == -1:
                self.__transition = {}
                return
            pyxel.rect(self.__cam_x, self.__cam_y, self.__transition["w"], pyxel.height, self.__transition["transition_color"])
            pyxel.rect(self.__transition["x"], self.__cam_y, self.__transition["w"], pyxel.height, self.__transition["transition_color"])

        elif self.__transition.get("type") == "rectangle_right_left":
            self.__transition["w"] += self.__transition["speed"] * self.__transition["direction"]
            if self.__transition["direction"] == 1:
                self.__transition["x"] -= self.__transition["speed"]

            if self.__transition["w"] > pyxel.width and self.__transition["direction"] == 1:
                self.__transition["direction"] = -1
                self.change_scene(self.__transition["new_scene_id"], self.__transition["new_camera_x"], self.__transition["new_camera_y"], self.__transition["action"])
            if self.__transition["w"] < 0 and self.__transition["direction"] == -1:
                self.__transition = {}
                return
            pyxel.rect(self.__transition["x"], self.__cam_y, self.__transition["w"], pyxel.height, self.__transition["transition_color"])

        elif self.__transition.get("type") == "rectangle_left_right":
            self.__transition["w"] += self.__transition["speed"] * self.__transition["direction"]
            if self.__transition["direction"] == -1:
                self.__transition["x"] += self.__transition["speed"]

            if self.__transition["w"] > pyxel.width and self.__transition["direction"] == 1:
                self.__transition["direction"] = -1
                self.change_scene(self.__transition["new_scene_id"], self.__transition["new_camera_x"], self.__transition["new_camera_y"], self.__transition["action"])
            if self.__transition["w"] < 0 and self.__transition["direction"] == -1:
                self.__transition = {}
                return
            pyxel.rect(self.__transition["x"], self.__cam_y, self.__transition["w"], pyxel.height, self.__transition["transition_color"])

        elif self.__transition.get("type") == "outer_circle":
            self.__transition["end"] -= self.__transition["speed"] * self.__transition["direction"]

            if self.__transition["end"] < 0 and self.__transition["direction"] == 1:
                self.__transition["direction"] = -1
                self.change_scene(self.__transition["new_scene_id"], self.__transition["new_camera_x"], self.__transition["new_camera_y"], self.__transition["action"])
            if self.__transition["end"] > self.__transition["start_end"] and self.__transition["direction"] == -1:
                self.__transition = {}
                return
            
            for radius in range(self.__transition["start_end"], self.__transition["end"], -1):
                pyxel.ellib(self.__cam_x + pyxel.width / 2 - radius, self.__cam_y + pyxel.height / 2 - radius, radius * 2, radius * 2, self.__transition["transition_color"])
                pyxel.ellib(self.__cam_x + pyxel.width / 2 - radius + 1, self.__cam_y + pyxel.height / 2 - radius, radius * 2, radius * 2, self.__transition["transition_color"])

        elif self.__transition.get("type") == "triangle":
            self.__transition["size"] += self.__transition["speed"] * self.__transition["direction"]
            self.__transition["angle"] += self.__transition["rotation_speed"] * self.__transition["direction"]

            if self.__transition["size"] / 2.5 > max(pyxel.width, pyxel.height) and self.__transition["direction"] == 1:
                self.__transition["direction"] = -1
                self.change_scene(self.__transition["new_scene_id"], self.__transition["new_camera_x"], self.__transition["new_camera_y"], self.__transition["action"])
            if self.__transition["size"] < 0 and self.__transition["direction"] == -1:
                self.__transition = {}
                return
            d = math.sqrt(3) / 3 * self.__transition["size"]
            x1, y1 = self.__cam_x + pyxel.width / 2 + d * math.cos(math.radians(0 + self.__transition["angle"])), self.__cam_y + pyxel.height / 2 + d * math.sin(math.radians(0 + self.__transition["angle"]))
            x2, y2 = self.__cam_x + pyxel.width / 2 + d * math.cos(math.radians(120 + self.__transition["angle"])), self.__cam_y + pyxel.height / 2 + d * math.sin(math.radians(120 + self.__transition["angle"]))
            x3, y3 = self.__cam_x + pyxel.width / 2 + d * math.cos(math.radians(240 + self.__transition["angle"])), self.__cam_y + pyxel.height / 2 + d * math.sin(math.radians(240 + self.__transition["angle"]))
            pyxel.tri(x1, y1, x2, y2, x3, y3, self.__transition["transition_color"])

    def update(self):
        self.__cam_x += (self.__cam_tx - self.__cam_x) * 0.1
        self.__cam_y += (self.__cam_ty - self.__cam_y) * 0.1

        if self.__shake_amount > 0:
            amount = int(self.__shake_amount)
            pyxel.camera(self.__cam_x + random.uniform(-amount, amount), self.__cam_y + random.uniform(-amount, amount))
            self.__shake_amount -= self.__sub_shake_amount
        else:
            pyxel.camera(self.__cam_x, self.__cam_y)

        if not self.__transition.get("type"):
            self.__current_scene.update()

    def draw(self):
        self.__current_scene.draw()
        if self.__transition:
            self.handle_transitions()

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
