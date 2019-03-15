try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from VectorHandler import Vector

spaceship = simplegui.load_image("https://imgur.com/gudzU5Z.png")

WIN_WIDTH = 800
WIN_HEIGHT = 600
PLAYER_SPEED = 0.9
PLAYER_IMG_SIZE = (100, 100)
PLAYER_IMG_CENTER = (50, 50)
PLAYER_IMG_ROTATION = 0


class Player:
    def __init__(self, pos):
        self.pos = pos
        self.vel = Vector()
        self.radius = 30

    def draw(self, canvas):
        #if Keyboard.left:
         #   canvas.draw_circle(self.pos.getP(), self.radius, 1, 'White', 'White')
        canvas.draw_image(spaceship, PLAYER_IMG_CENTER, PLAYER_IMG_SIZE , self.pos.getP(), PLAYER_IMG_SIZE , PLAYER_IMG_ROTATION)

    def move(self):
        self.pos.add(self.vel)
        self.vel.multiply(PLAYER_SPEED)
        if self.pos == Vector(0, WIN_WIDTH):
            self.stop()
        if not self.is_stationary() and self.vel.length() < 0.1:
            self.stop()

        if self.pos.x >= WIN_WIDTH:
            self.stop()
        elif self.pos.x <= 0:
            self.stop()

    def stop(self):
        self.vel = Vector()

    def is_stationary(self):
        return self.vel.length() == 0

    def hit_left(self):
        return self.pos.x - self.radius

    def hit_right(self):
        return self.pos.x + self.radius

    def animate(self, canvas):
        self.move()
        self.draw(canvas)


class Keyboard:
    def __init__(self):
        self.player = player
        self.left = False
        self.right = False

    def keydown(self, key):
        if key == simplegui.KEY_MAP["left"]:
            self.left = True
        elif key == simplegui.KEY_MAP["right"]:
            self.right = True
        #if key == simplegui.KEY_MAP["p"]:
        #    timer.stop()
        #    frame.stop()

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


player = Player(Vector(WIN_WIDTH/2, WIN_HEIGHT/1.1))
keyboard = Keyboard()