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

import cts
from VectorHandler import Vector
from PlayerHandler import *
from FrameRate import FPS
import math, random

# CONSTANTS
ENEMY_SPEED = 10
ENEMY_JUMPS = 16
counter = 0
bullets = []
row = 3
col = 6

EIX = 48
EIY = EIX
ENEMY_IMG_SIZE = (EIX, EIY)
ENEMY_IMG_CENTER = (EIX / 2, EIY / 2)
ENEMY_IMG_ROTATION = 0

BULLET_SPEED = 15

ENEMY_MAX_MOVES = ((WIN_WIDTH / ENEMY_JUMPS) / 2)
if ENEMY_MAX_MOVES > int(ENEMY_MAX_MOVES):
    ENEMY_MAX_MOVES = math.ceil(ENEMY_MAX_MOVES * 1.1)
else:
    ENEMY_MAX_MOVES = int(ENEMY_MAX_MOVES)
# EMM allows for scaling for both a change in the window width, or a change in the number of jumps we want.

e_x = 85
ENEMY_START_X = WIN_WIDTH / 10
ENEMY_START_Y = WIN_HEIGHT / 10
ENEMIES_GAP = 50

enemy = simplegui.load_image("https://imgur.com/fI8cyfM.png")


class Enemy:
    def __init__(self, pos):
        self.pos = pos
        self.vel = Vector(0, 0)
        self.mRight = True
        self.down = False

    def draw(self, canvas):
        canvas.draw_image(enemy, ENEMY_IMG_CENTER, ENEMY_IMG_SIZE, self.pos.getP(), ENEMY_IMG_SIZE, ENEMY_IMG_ROTATION)

    def move(self):
        if self.mRight:
            self.pos.add(Vector(ENEMY_JUMPS, 0))
        elif not self.mRight:
            self.pos.subtract(Vector(ENEMY_JUMPS, 0))
        if self.down:
            self.move_down()
            self.down = False

    def move_down(self):
        self.pos.y += 25
        if self.mRight:
            self.pos.x += -15
            self.mRight = False
        elif not self.mRight:
            self.pos.x += 15
            self.mRight = True

    def shoot(self):
        if (random.randint(1, (row * col))) < ((row + col) / 6):
            bullet = Bullet(Vector(self.pos.x, self.pos.y), BULLET_SPEED, 'Red')
            bullets.append(bullet)

    def animate(self, canvas):
        self.draw(canvas)
        self.move()


class Bullet:
    def __init__(self, pos, speed, colour):
        self.pos = pos
        self.speed = speed
        self.color = colour
        self.vel = Vector(0, 0)

    def draw(self, canvas):
        canvas.draw_line((self.pos.x, self.pos.y), (self.pos.x, self.pos.y + 10), 3, 'Red')

    def move(self):
        self.pos.y += self.speed

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


def move_objects():
    global counter, t

    counter += 1

    # make enemies move faster
    if counter % ENEMY_SPEED == 0:
        for enemy in eList:
            enemy.move()
            if counter % (ENEMY_SPEED * ENEMY_MAX_MOVES) == 0:
                enemy.move_down()
            enemy.shoot()

    for bullet in bullets:
        bullet.move()

#print(enemies)
def draw(canvas):
    player.animate(canvas)
    keyboard.update()
    for enemy in eList:
        enemy.draw(canvas)

    for bullet in bullets:
        bullet.draw(canvas)
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