'''
Main class for both single Enemies and Enemies as a group. Includes a player sprite
(with some basic left-right movement) and keyboard class for testing purposes.

Press 'P' to properly exit the game, as currently SimpleGUI likes to inform you that
there is still a timer running when you exit, which I need to fix.

TO-DO:
- Sort what from Enemy class is needed in Enemies class
- Further add to Enemies class (ability to be hit individually, ability to shoot bullets etc.)
- General code clean-up (probably in accordance with PEP 8
'''

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from VectorHandler import Vector
from PlayerHandler import *
from FrameRate import FPS
import time

# CONSTANTS
WIN_WIDTH = 800
WIN_HEIGHT = 600
PLAYER_SPEED = 0.9
ENEMY_SPEED = 10
counter = 0

ENEMY_IMG_SIZE = (48, 48)
ENEMY_IMG_CENTER = (24, 24)
ENEMY_IMG_ROTATION = 0
ENEMY_MAX_MOVES = 22

e_x = 85
ENEMY_START_X = 60
ENEMY_START_Y = 70
ENEMIES_GAP = 50

enemy = simplegui.load_image("https://imgur.com/fI8cyfM.png")


class Enemy:
    def __init__(self, pos):
        self.pos = pos
        self.vel = Vector(0, 0)
        self.radius = 15
        self.mRight = True
        self.down = False

    def draw(self, canvas):
        #canvas.draw_circle(self.pos.getP(), self.radius, 1, 'white', 'white')
        canvas.draw_image(enemy, ENEMY_IMG_CENTER, ENEMY_IMG_SIZE, self.pos.getP(), ENEMY_IMG_SIZE, ENEMY_IMG_ROTATION)

    def move(self):
        if self.mRight:
            self.pos.add(Vector(20, 0))
        elif not self.mRight:
            self.pos.subtract(Vector(20, 0))
        if self.down:
            self.moveDown()
            self.down = False

    def moveDown(self):
        self.pos.y += 25
        if self.mRight:
            self.pos.x += -15
            self.mRight = False
        elif not self.mRight:
            self.pos.x += 15
            self.mRight = True

    def animate(self, canvas):
        self.draw(canvas)
        self.move()


class Enemies:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols


eList = []
x = e_x
moved = 0
t = 0


def make_enemies():
    for row in range(3):
        for col in range(6):
            posv= Vector(ENEMY_START_X + (col * ENEMIES_GAP), ENEMY_START_Y + (row * ENEMIES_GAP))
            en = Enemy(posv)
            eList.append(en)


'''for n in range(6):
    x = x + 50
    y = 100
    posi = Vector(x,y)
    e = Enemy(posi)
    enemies.append(e)'''


def move_objects():
    global counter, t

    counter += 1

    # make enemies move faster
    if counter % ENEMY_SPEED == 0:
        for enemy in eList:
            enemy.move()
            if counter % (ENEMY_SPEED * ENEMY_MAX_MOVES) == 0:
                enemy.moveDown()


#print(enemies)
def draw(canvas):
    player.animate(canvas)
    keyboard.update()
    for enemy in eList:
        enemy.draw(canvas)
        #enemy.move()
    fps.draw_fct(canvas)


make_enemies()

fps = FPS()

# Frame creation
frame = simplegui.create_frame("Main", WIN_WIDTH, WIN_HEIGHT)
frame.set_keydown_handler(keyboard.keydown)
frame.set_keyup_handler(keyboard.keyup)
frame.set_draw_handler(draw)

timer = simplegui.create_timer(60, move_objects)
timer.start()
fps.start()
frame.start()