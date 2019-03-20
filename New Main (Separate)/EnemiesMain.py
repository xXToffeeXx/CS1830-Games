try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from VectorHandler import Vector
import math, random

CANVAS_WIDTH = 540
CANVAS_HEIGHT = 540
ENEMY_JUMP = 30  # Used to calc max moves
ESX = 50  # Enemy starting X coord
ESY = 50  # Enemy starting Y coord
ENEMIES = []
ENEMY_SPEED = 20  # Time when to update enemy movement
ENEMY_GAP = 40  # Pixel distance between each enemy sprite
rows = 3  # Number of enemy rows to spawn
columns = 6  # Number of enemy columns to spawn
counter = 0  # Time counter
BULLET_SPEED = 2  # Bullet distance coverage
BULLETS = []

# Calculate number of moves enemies should make before moving down the screen
ENEMY_MAX_MOVES = ((CANVAS_WIDTH / ENEMY_JUMP) / 2)
if ENEMY_MAX_MOVES > int(ENEMY_MAX_MOVES):
    ENEMY_MAX_MOVES = math.ceil(ENEMY_MAX_MOVES * 1.1)
else:
    ENEMY_MAX_MOVES = int(ENEMY_MAX_MOVES)

class Sprite:
    def __init__(self, image, height, width, pos):
        self.pos = pos
        self.vel = Vector()
        self.image = simplegui.load_image(image)
        self.margin = width / 2
        self.display_size = (width, height)
        self.source_size = (self.image.get_width(), self.image.get_height())
        self.source_center = (self.image.get_width() / 2, self.image.get_height() / 2)

    def draw(self, canvas):
        canvas.draw_image(self.image, self.source_center, self.source_size, self.pos.getP(), self.display_size)

    def update(self):
        pass

class Enemy(Sprite):
    def __init__(self, pos):
        self.pos = pos
        super(Enemy, self).__init__('https://i.imgur.com/2e24IN1.png', 26, 26, self.pos)
        self.right = True
        self.downright = 0
        self.downleft = ENEMY_MAX_MOVES

    def update(self):
        global ENEMY_MAX_MOVES

        if self.right:
            self.pos.add(Vector(ENEMY_JUMP, 0))
            self.downright += 1

            if self.downright == ENEMY_MAX_MOVES:
                self.move_down()

        elif not self.right:
            self.pos.subtract(Vector(ENEMY_JUMP, 0))

            self.downleft = self.downleft - 1

            if self.downleft == 0:
                self.move_down()

    def move_down(self):
        self.pos.y += 25
        if self.right:
            self.pos.x += -15
            self.right = False
        elif not self.right:
            self.pos.x += 15
            self.right = True

    def shoot(self):
        #if (random.randint(1, (rows * columns))) < ((rows + columns) / 6):
        if (random.randint(1, 750)) == 1:
            b = Vector(self.pos.x, self.pos.y)
            BULLETS.append(Bullet(b))

    def get_pos_x(self):
        return self.pos.x

class Bullet(Sprite):
    def __init__(self, pos):
        self.pos = pos
        super(Bullet, self).__init__('https://i.imgur.com/9t4g4Ey.png', 16, 16, self.pos)
        self.speed = BULLET_SPEED

    def move(self):
        self.pos.y += self.speed
        if self.pos.y > CANVAS_HEIGHT - 10:
            BULLETS.remove(self)


def make_enemies():
    for row in range(rows):
        for col in range(columns):
            posv = Vector(ESX + (col * ENEMY_GAP), ESY + (row * ENEMY_GAP))
            ENEMIES.append(Enemy(posv))

def draw(canvas):
    global counter

    counter += 1

    for enemy in ENEMIES:
        enemy.draw(canvas)
        if counter % (100 - ENEMY_SPEED) == 0:
            enemy.update()
        enemy.shoot()

    for bullet in BULLETS:
        bullet.draw(canvas)
        bullet.move()


make_enemies()

frame = simplegui.create_frame("Main", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_draw_handler(draw)

frame.start()
