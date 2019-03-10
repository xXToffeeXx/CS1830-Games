try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

import VectorHandler
import main

class KB:

    def __init__(self):
        self.player = main.player
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
            self.player.vel.subtract(VectorHandler.Vector(main.PLAYER_SPEED, 0))
        if self.right:
            self.player.vel.add(VectorHandler.Vector(main.PLAYER_SPEED, 0))