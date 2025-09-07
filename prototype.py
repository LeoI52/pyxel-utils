import pyxel

pyxel.init(128, 128)
pyxel.mouse(True)

def update():
    pass

def draw():
    pyxel.cls(0)
    
pyxel.run(update, draw)