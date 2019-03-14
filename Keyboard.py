try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

import VectorHandler
from main import Player

class KB:
    def __init__(self):
        self.player = player
        self.left = False
        self.right = False

    def keydown(self, key):
        if key == simplegui.KEY_MAP["left"]:
            self.left = True
        elif key == simplegui.KEY_MAP["right"]:
            self.right = True
        if key == simplegui.KEY_MAP["p"]:
            timer.stop()
            frame.stop()


    def keyup(self, key):
        if key == simplegui.KEY_MAP["left"]:
            self.left = False
        elif key == simplegui.KEY_MAP["right"]:
            self.right = False

    def update(self):
        if self.left:
            self.player.vel.subtract(Vector(PLAYER_SPEED, 0))
        if self.right:
            self.player.vel.add(Vector(PLAYER_SPEED, 0))