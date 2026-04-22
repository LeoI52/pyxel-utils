import math
import pyxel

class Vine:
    def __init__(
        self,
        points,
        segment_length=4,
        gravity=0.3,
        damping=0.999,
        constraint_iters=4
    ):
        """
        points: list of (x, y) initial positions
        """
        self.segment = segment_length
        self.gravity = gravity
        self.damping = damping
        self.constraint_iters = constraint_iters

        self.points = []
        for x, y in points:
            self.points.append({
                "x": x,
                "y": y,
                "old_x": x,
                "old_y": y
            })

        # Anchors: list of dicts
        # { index, get_pos(), strength }
        self.anchors = []

    def add_anchor(self, index, get_pos, strength=1.0):
        """
        get_pos: function returning (x, y)
        strength: 1.0 = rigid, <1.0 = elastic
        """
        self.anchors.append({
            "i": index,
            "get_pos": get_pos,
            "strength": strength
        })

    def update(self):
        self._integrate()
        for _ in range(self.constraint_iters):
            self._solve_segments()
            self._solve_anchors()

    def _integrate(self):
        for p in self.points:
            vx = (p["x"] - p["old_x"]) * self.damping
            vy = (p["y"] - p["old_y"]) * self.damping

            p["old_x"] = p["x"]
            p["old_y"] = p["y"]

            p["x"] += vx
            p["y"] += vy + self.gravity

    def _solve_segments(self):
        for i in range(len(self.points) - 1):
            p1 = self.points[i]
            p2 = self.points[i + 1]

            dx = p2["x"] - p1["x"]
            dy = p2["y"] - p1["y"]
            dist = math.hypot(dx, dy) or 0.0001

            diff = (dist - self.segment) / dist
            offx = dx * 0.5 * diff
            offy = dy * 0.5 * diff

            p1["x"] += offx
            p1["y"] += offy
            p2["x"] -= offx
            p2["y"] -= offy

    def _solve_anchors(self):
        for a in self.anchors:
            p = self.points[a["i"]]
            ax, ay = a["get_pos"]()

            dx = ax - p["x"]
            dy = ay - p["y"]

            p["x"] += dx * a["strength"]
            p["y"] += dy * a["strength"]

    def apply_impulse(self, x, y, radius=8, strength=0.3):
        for p in self.points:
            dx = p["x"] - x
            dy = p["y"] - y
            d2 = dx * dx + dy * dy

            if d2 < radius * radius:
                p["x"] += dx * strength
                p["y"] += dy * strength

    def draw(self, color=11):
        for i in range(len(self.points) - 1):
            p1 = self.points[i]
            p2 = self.points[i + 1]
            pyxel.line(p1["x"], p1["y"], p2["x"], p2["y"], color)

pyxel.init(128, 128)
pyxel.mouse(True)

points = [(80, i * 4) for i in range(32)]
vine = Vine(points)

# Static anchors
vine.add_anchor(0, lambda: (40, 0), strength=1.0)

def update():
    vine.update()
    vine.apply_impulse(pyxel.mouse_x, pyxel.mouse_y, 8, 0.5)

def draw():
    pyxel.cls(0)
    vine.draw()

pyxel.run(update, draw)