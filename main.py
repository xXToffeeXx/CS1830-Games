try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

import Vector

# GLOBAL CONSTANTS
WIN_WIDTH = 800
WIN_HEIGHT = 600
PLAYER_SPEED = 5

class Player:
    def __init__(self, pos):
        self.pos = pos
        self.vel = Vector()

    def draw(self, canvas):
        canvas.draw_circle(self.pos.getP(), 30, 1, 'White', 'White')

    def update(self):
        self.pos.add(self.vel)
        self.vel.multiply(0.60)
        if not self.isStationary() and self.vel.length() < 0.1:
            self.stop()

    def stop(self):
        self.vel = Vector()

    def isStationary(self):
        return self.vel.length() == 0

    def animate(self, canvas):
        self.update()
        self.draw(canvas)


player = Player(Vector(400,300))

def draw(canvas):
    player.animate()


# Frame creation
frame = simplegui.create_frame("Main", WIN_WIDTH, WIN_HEIGHT)
frame.set_draw_handler(draw)
frame.start()