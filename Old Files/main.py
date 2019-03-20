'''
Main class for both single Enemies and Enemies as a group. Includes a player sprite
(with some basic left-right movement) and keyboard class for testing purposes.


TO-DO:
- Sort what from Enemy class is needed in Enemies class
- Further add to Enemies class (ability to be hit individually, ability to shoot bullets etc.)
- General code clean-up (probably in accordance with PEP 8)
'''

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# IMPORTS #
from PlayerHandler import *
from FrameRate import FPS
from Sprite import Sprite
import math, random

# ENEMY CONSTANTS #
ENEMY_SPEED = 10
ENEMY_JUMP = 16
# Dist for enemies to 'hop' left/right (rather than a smooth animation, in keeping with classic S.I)
# JUMP does affect enemy speed at the moment, will need to be changed later.
EIX = 24
EIY = EIX
ENEMY_IMG_SIZE = (EIX, EIY)
ENEMY_IMG_CENTER = (EIX / 2, EIY / 2)
ENEMY_START_X = WIN_WIDTH / 10
ENEMY_START_Y = WIN_HEIGHT / 10
ENEMIES_GAP = 50

BULLET_IMG_SIZE = (16, 16)
BULLET_IMG_CENTER = (8, 8)

#enemy = simplegui.load_image("https://imgur.com/fI8cyfM.png")
enemy = simplegui.load_image("https://i.imgur.com/2e24IN1.png")
bullet = simplegui.load_image("https://i.imgur.com/9t4g4Ey.png")
spritesheet = simplegui.load_image("https://i.imgur.com/glDuLYi.png")

ENEMY_MAX_MOVES = ((WIN_WIDTH / ENEMY_JUMP) / 2)
if ENEMY_MAX_MOVES > int(ENEMY_MAX_MOVES):
    ENEMY_MAX_MOVES = math.ceil(ENEMY_MAX_MOVES * 1.1)
else:
    ENEMY_MAX_MOVES = int(ENEMY_MAX_MOVES)
# EMM allows for scaling for both a change in the window width, or a change in the number of jumps we want.

# OTHER #
eList = []
t = 0
counter = 0
counter2 = 0
bullets = []
sprites = []
rows = 3
columns = 6
BULLET_SPEED = 15
sCount = 1


class Enemy:
    def __init__(self, pos):
        self.image = simplegui.load_image("https://i.imgur.com/MnPWsv8.png")
        self.width = 208
        self.height = 26
        self.pos = pos
        self.vel = Vector(0, 0)
        self.mRight = True
        self.down = False
        self.sCount = 0
        self.frameSize = [26, 26]
        self.frameCenter = [13, 13]

    def draw(self, canvas):

        #for sprite in sprites:
        #    sprite.draw(canvas)

        canvas.draw_image(self.image, (self.frameCenter[0], self.frameCenter[1]),
                         (self.frameSize[0], self.frameSize[1]), self.pos.getP(),
                         (self.frameSize[0], self.frameSize[1]), 0)

        '''if sCount == 1:
            self.frameSize = [26, 26]
            self.frameCenter = [13, 13]
        else:
            self.frameSize = [26 * iteration, 26]
            self.frameCenter = [13 * iteration, 13]

        print (self.frameSize)

        canvas.draw_image(spritesheet, (self.frameCenter),
                         (self.frameSize), self.pos.getP(),
                         (self.frameSize), 0)'''

        '''self.frameCenter[0] += 13
        self.frameSize[0] += 26
        sCount += 1
        if sCount == (rows * columns):
            self.frameCenter[0] = 13
            self.frameSize[0] = 26
            sCount = 1'''

    '''def draw2(self, canvas):
        canvas.draw_image(self.image, (self.frameCenter[0] + 13, self.frameCenter[1]),
                          (self.frameSize[0] + 26, self.frameSize[1]), self.pos.getP(),
                          (self.frameSize[0] + 26, self.frameSize[1]), 0)'''

    '''def cur_sprite(self, canvas):
        global sCount
        print(sCount)
        if sCount <= (rows * columns):
            canvas.draw_image(self.image, (self.frameCenter[0], self.frameCenter[1]),
                              (self.frameSize[0], self.frameSize[1]), self.pos.getP(),
                              (self.frameSize[0], self.frameSize[1]), 0)

            print("center:", self.frameCenter[0])
            print("size:", self.frameSize[0])

            self.frameCenter[0] += 13
            self.frameSize[0] += 26
            sCount += 1
        else:
            #canvas.draw_image(self.image, (self.frameCenter[0], self.frameCenter[1]),
             #                 (self.frameSize[0], self.frameSize[1]), self.pos.getP(),
              #                (self.frameSize[0], self.frameSize[1]), 0)
            self.frameCenter[0] = 0
            self.frameSize[0] = 0
            sCount = 1'''

    def make_sprites(self):
        for row in range(rows):
            for col in range(columns):
                sprite = Sprite([self.pos.x, self.pos.y], 1, 1)
                sprites.append(sprite)


    def kill(self):
        if (random.randint(1, (500))) == 13:
            eList.remove(self)

    def move(self):
        if self.mRight:
            self.pos.add(Vector(ENEMY_JUMP, 0))
        elif not self.mRight:
            self.pos.subtract(Vector(ENEMY_JUMP, 0))
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
        # Calculate a random time to shoot a bullet. Calculations are sorta meaningless, but
        # in theory they scale depending on the desired number of enemy rows and columns.
        # Will likely change how random bullets are spawned later.
        if (random.randint(1, (rows * columns))) < ((rows + columns) / 6):
            bullet = Bullet(Vector(self.pos.x, self.pos.y), BULLET_SPEED, 'Red')
            bullets.append(bullet)

    def animate(self, canvas):
        self.draw(canvas)
        self.move()


class Bullet:
    def __init__(self, pos, speed, colour):
        self.pos = pos
        self.speed = speed
        self.colour = colour
        # self.vel = Vector(0, 0)

    def draw(self, canvas):
        #canvas.draw_line((self.pos.x, self.pos.y), (self.pos.x, self.pos.y + 10), 3, 'Red')
        canvas.draw_image(bullet, BULLET_IMG_CENTER, BULLET_IMG_SIZE, self.pos.getP(), BULLET_IMG_SIZE, 0)

    def move(self):
        self.pos.y += self.speed


def make_enemies():

    for row in range(rows):
        for col in range(columns):
            posv = Vector(ENEMY_START_X + (col * ENEMIES_GAP), ENEMY_START_Y + (row * ENEMIES_GAP))
            en = Enemy(posv)
            eList.append(en)


def move_objects():
    global counter, t

    counter += 1

    # Attempt at using a timer/counter to help deal with enemy speeds.
    if counter % ENEMY_SPEED == 0:
        for enemy in eList:
            enemy.move()
            if counter % (ENEMY_SPEED * ENEMY_MAX_MOVES) == 0:
                # Decides when the enemies should move down the screen. Look at EMM in constants to see how this is
                #  calculated. Enemies should not move down too early or too late, even if screen size is adjusted.
                # However, changing number of columns for enemies DOES cause problems, so needs to be re-done.
                enemy.move_down()
            enemy.shoot()

    for bullet in bullets:
        bullet.move()

    if keyboard.p:
        for enemy in eList:
            enemy.kill()

    if keyboard.q:
        timer.stop()
        fps.stop()
        frame.stop()


def draw(canvas):
    global sCount
    player.animate(canvas)
    keyboard.update()
    #s.make_sprites()

    for enemy in eList:
        enemy.draw(canvas)
        # enemy.kill()
        # Kill currently in testing. Need to work with collisions from player bullets.

    sCount += 1
    if (sCount % 9 == 0):
        sCount = 1
    #print(sCount)
    #else:
     #   sCount += 1
      #  print(sCount)

    for bullet in bullets:
        bullet.draw(canvas)

    fps.draw_fct(canvas)


make_enemies()
fps = FPS()
#s = Sprite()
print(ENEMY_MAX_MOVES)

#sprite1 = Sprite([WIN_WIDTH/2, (WIN_HEIGHT / 2) / 2], 1.5, 0.6)

# Frame creation
frame = simplegui.create_frame("Main", WIN_WIDTH, WIN_HEIGHT)
frame.set_keydown_handler(keyboard.keydown)
frame.set_keyup_handler(keyboard.keyup)
frame.set_draw_handler(draw)

timer = simplegui.create_timer(60, move_objects)
timer.start()
fps.start()
frame.start()
