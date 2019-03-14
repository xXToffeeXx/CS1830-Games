try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from VectorHandler import Vector
#from Keyboard import KB
import time

# CONSTANTS
WIN_WIDTH = 800
WIN_HEIGHT = 600
PLAYER_SPEED = 0.9
ENEMY_SPEED = 10
counter = 0

pi_size = (100, 100)
pi_center = (50, 50)
pi_rotation = 0

ei_size = (48, 48)
ei_center = (24, 24)
ei_rotation = 0
e_x = 85

spaceship = simplegui.load_image("https://imgur.com/gudzU5Z.png")
enemy = simplegui.load_image("https://imgur.com/fI8cyfM.png")

class Player:
    def __init__(self, pos):
        self.pos = pos
        self.vel = Vector()
        self.radius = 30

    def draw(self, canvas):
        #canvas.draw_circle(self.pos.getP(), self.radius, 1, 'White', 'White')
        canvas.draw_image(spaceship, pi_center, pi_size, self.pos.getP(), pi_size, pi_rotation)

    def move(self):
        self.pos.add(self.vel)
        self.vel.multiply(PLAYER_SPEED)
        if self.pos == Vector(0, WIN_WIDTH):
            self.stop()
        if not self.isStationary() and self.vel.length() < 0.1:
            self.stop()

    def stop(self):
        self.vel = Vector()

    def isStationary(self):
        return self.vel.length() == 0

    def hitL(self):
        return self.pos.x - self.radius

    def hitR(self):
        return self.pos.x + self.radius

    def animate(self, canvas):
        self.move()
        self.draw(canvas)


class Enemy:
    def __init__(self, pos):
        self.pos = pos
        self.vel = Vector(0, 0)
        self.radius = 15
        self.mRight = True
        self.down = False

    def draw(self, canvas):
        #canvas.draw_circle(self.pos.getP(), self.radius, 1, 'white', 'white')
        canvas.draw_image(enemy, ei_center, ei_size, self.pos.getP(), ei_size, ei_rotation)

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


player = Player(Vector(WIN_WIDTH/2, WIN_HEIGHT/1.1))
keyboard = KB()
enemies = []
x = e_x
moved = 0
t = 0

for n in range(6):
    x = x + 50
    y = 100
    posi = Vector(x,y)
    e = Enemy(posi)
    enemies.append(e)

x = e_x
for n in range(6):
    x = x + 50
    y = 150
    posi = Vector(x, y)
    e = Enemy(posi)
    enemies.append(e)

def move_objects():
    global counter, t

    counter +=1

    #make enemies move faster
    if counter % ENEMY_SPEED == 0:
        for enemy in enemies:
            enemy.move()
            #if enemy.pos.x > 700:
             #   enemy.moveDown()
            if counter % (ENEMY_SPEED * 15) == 0:
                enemy.moveDown()


def draw(canvas):
    player.animate(canvas)
    keyboard.update()
    for enemy in enemies:
        enemy.draw(canvas)
        #enemy.move()

# Frame creation
frame = simplegui.create_frame("Main", WIN_WIDTH, WIN_HEIGHT)
frame.set_keydown_handler(keyboard.keydown)
frame.set_keyup_handler(keyboard.keyup)
frame.set_draw_handler(draw)

timer = simplegui.create_timer(60, move_objects)
timer.start()

frame.start()