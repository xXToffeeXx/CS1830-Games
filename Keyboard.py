try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

import Vector
import main

class Keyboard:

    def __init__(self):
        self.left = False
        self.right = False

    def keydown(self, key):
        if key == simplegui.KEY_MAP["left"]:
            self.left = True
        elif key == simplegui.KEY_MAP["right"]:
            self.right = True

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