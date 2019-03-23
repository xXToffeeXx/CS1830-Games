try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

import math, random, sys
import time

################################################################################
# You need the math library to compute the square root of a number.
# The method to be used is math.sqrt.

import math


################################################################################
# Classes

# The Vector class
class Vector:

    # Initialiser
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    # Returns a string representation of the vector
    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    # Tests the equality of this vector and another
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    # Tests the inequality of this vector and another
    def __ne__(self, other):
        return not self.__eq__(other)

        # Returns a tuple with the point corresponding to the vector

    def getP(self):
        return (self.x, self.y)

    # Returns a copy of the vector
    def copy(self):
        return Vector(self.x, self.y)

    # Adds another vector to this vector
    def add(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __add__(self, other):
        return self.copy().add(other);

    # Negates the vector (makes it point in the opposite direction)
    def negate(self):
        return self.multiply(-1)

    def __neg__(self):
        return self.copy().negate()

    # Subtracts another vector from this vector
    def subtract(self, other):
        return self.add(-other)

    def __sub__(self, other):
        return self.copy().subtract(other)

    # Multiplies the vector by a scalar
    def multiply(self, k):
        self.x *= k
        self.y *= k
        return self

    def __mul__(self, k):
        return self.copy().multiply(k)

    def __rmul__(self, k):
        return self.copy().multiply(k)

    # Divides the vector by a scalar
    def divide(self, k):
        return self.multiply(1 / k)

    def __truediv__(self, k):
        return self.copy().divide(k)

    # Normalizes the vector
    def normalize(self):
        return self.divide(self.length())

    # Returns a normalized version of the vector
    def getNormalized(self):
        return self.copy().normalize()

    # Returns the dot product of this vector with another one
    def dot(self, other):
        return self.x * other.x + self.y * other.y

    # Returns the length of the vector
    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    # Returns the squared length of the vector
    def lengthSquared(self):
        return self.x ** 2 + self.y ** 2

    # Reflect this vector on a normal
    def reflect(self, normal):
        n = normal.copy()
        n.multiply(2 * self.dot(normal))
        self.subtract(n)
        return self

    # Returns the angle between this vector and another one
    # You will need to use the arccosine function:
    # acos in the math library
    def angle(self, other):
        return math.acos(self.dot(other) / (self.length() * other.length()))

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
GAME_STARTED = False
GAME_ENDED = False
LEVEL = 1
SCORE = 0
KILLED = 0
TIME = 0
BULLETS = []

### ENEMY CONSTANTS ###
ENEMIES = []
ENEMY_SPEED = 40
ENEMY_GAP = 35
ENEMY_JUMP = 21
ENEMY_JUMP_DOWN = 30
ESX = 50
ESY = 75
E_ROWS = 4
E_COLS = 9
E_BULLETS = []
BULLET_SPEED = 7
counter = 0
WALLS = []
# Calculate number of moves enemies should make before moving down the screen
ENEMY_MAX_MOVES = ((CANVAS_WIDTH / ENEMY_JUMP) / 2)
if ENEMY_MAX_MOVES > int(ENEMY_MAX_MOVES):
    ENEMY_MAX_MOVES = math.ceil(ENEMY_MAX_MOVES * 1.1)
else:
    ENEMY_MAX_MOVES = int(ENEMY_MAX_MOVES)
###


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


class Controls:

    def __init__(self, p1, p2):
        self.p1_right = False
        self.p1_left = False
        self.p2_right = False
        self.p2_left = False
        self.p1 = p1
        self.p2 = p2
        self.p1_last = counter
        self.p2_last = counter
        self.cooldown = 40

    def keyDown(self, key):
        if key == simplegui.KEY_MAP['d']:
            self.p1_right = True
        if key == simplegui.KEY_MAP['a']:
            self.p1_left = True
        if key == simplegui.KEY_MAP['l']:
            self.p2_right = True
        if key == simplegui.KEY_MAP['j']:
            self.p2_left = True

    def keyUp(self, key):
        if key == simplegui.KEY_MAP['d']:
            self.p1_right = False
        if key == simplegui.KEY_MAP['a']:
            self.p1_left = False
        if key == simplegui.KEY_MAP['l']:
            self.p2_right = False
        if key == simplegui.KEY_MAP['j']:
            self.p2_left = False
        if key == simplegui.KEY_MAP['s'] and self.p1.disable is False:
            now = counter
            if now - self.p1_last >= self.cooldown:
                BULLETS.append(Bullet(self.p1.getPosition(), "UP"))
                self.p1_last = counter
        if key == simplegui.KEY_MAP['k'] and self.p2.disable is False:
            now = counter
            if now - self.p2_last >= self.cooldown:
                BULLETS.append(Bullet(self.p2.getPosition(), "UP"))
                self.p2_last = counter

    def update(self):
        if self.p1_right:
            self.p1.vel.add(Vector(1, 0))
        if self.p1_left:
            self.p1.vel.add(Vector(-1, 0))
        if self.p2_right:
            self.p2.vel.add(Vector(1, 0))
        if self.p2_left:
            self.p2.vel.add(Vector(-1, 0))


class Player(Sprite):
    # Specific player CONSTANTS
    LIVES = 3
    velocity = 0.75
    startpos = Vector(CANVAS_WIDTH / 2, CANVAS_HEIGHT - 50)

    def __init__(self, image):
        # https://i.imgur.com/9e6rcxM.png original sprite
        self.image = image
        super(Player, self).__init__(image, 75, 75, self.startpos)
        self.disable = False

    def update(self):
        new_pos = self.pos.copy()
        new_pos.add(self.vel)
        if not self.disable:
            if (new_pos.x > self.margin) and (new_pos.x < (CANVAS_WIDTH - self.margin)):
                self.pos = new_pos.copy()
                self.vel.multiply(self.velocity)
            else:
                self.vel = Vector(0,0)
        elif self.disable:
            self.vel = Vector(0,0)

    def stop(self):
        self.disable = True

    def getPosition(self):
        return self.pos


class Bullet(Sprite):
    direction = None
    startpos = Vector(CANVAS_WIDTH / 2, CANVAS_HEIGHT - 50)
    # https://i.imgur.com/alE94NY.png original bullet

    def __init__(self, pos, direction):
        super(Bullet, self).__init__('https://i.imgur.com/n08NeaE.png', 10, 10, self.startpos)
        self.pos = pos

        if direction == "UP":
            self.direction = Vector(0, -3.5)
        else:
            self.direction = Vector(0, 3.5)

    def update(self):
        self.pos.add(self.direction)


class Enemy(Sprite):
    def __init__(self, pos):
        self.pos = pos
        self.image = 'https://i.imgur.com/2e24IN1.png'
        super(Enemy, self).__init__(self.image, 34, 34, self.pos)
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
                self.downright = 0

        elif not self.right:
            self.pos.subtract(Vector(ENEMY_JUMP, 0))
            self.downleft -= 1

            if self.downleft == 0:
                self.move_down()
                self.downleft = ENEMY_MAX_MOVES

        if self.pos.y >= playerOne.pos.y - 30:
            # TODO: initiate a game over as players have died
            playerOne.stop()
            playerTwo.stop()

    def move_down(self):
        self.pos.y += ENEMY_JUMP_DOWN
        if self.right:
            self.pos.x += -ENEMY_JUMP_DOWN + 10
            self.right = False
        elif not self.right:
            self.pos.x += ENEMY_JUMP_DOWN - 10
            self.right = True


    def shoot(self):
        if (random.randint(1, 2000)) == 1:
            b = Vector(self.pos.x, self.pos.y)
            E_BULLETS.append(EnemyBullet(b))

    def die(self):
        global explo
        get_pos = (self.pos.x, self.pos.y)
        ENEMIES.remove(self)
        explo = Explosion(get_pos, True)

    def get_pos_x(self):
        return self.pos.x


class Explosion:
    def __init__(self, pos, truth):
        self.pos = pos
        self.truth = truth
        self.cooldown = 40
        self.now = counter + self.cooldown
        self.death_img = simplegui.load_image('https://i.imgur.com/YmWrpV5.png')

    def draw(self, canvas):
        print(self.truth)
        if self.truth:
            if (self.now >= counter):
                canvas.draw_image(self.death_img, (12.5, 12.5), (25, 25), self.pos, (25, 25))
            else:
                self.truth = False


class EnemyBullet(Sprite):
    def __init__(self, pos):
        self.pos = pos
        super(EnemyBullet, self).__init__('https://i.imgur.com/9t4g4Ey.png', 16, 16, self.pos)
        self.speed = BULLET_SPEED

    def move(self):
        self.pos.y += self.speed
        if self.pos.y > CANVAS_HEIGHT - 10:
            E_BULLETS.remove(self)


class Walls(Sprite):
    def __init__(self, pos):
        self.pos = pos
        super(Walls, self).__init__('https://i.imgur.com/zVKPBzx.png', 64, 72, self.pos)

    def update(self):
        pass


class Interaction:
    def __init__(self, EBULLETS, BULLETS, playerOne, playerTwo, eList):
        self.E_BULLETS = EBULLETS
        self.BULLETS = BULLETS
        self.playerOne = playerOne
        self.playerTwo = playerTwo
        self.eList = eList

    def update(self):
            global KILLED
            for bullet in BULLETS:
                for enemy in self.eList:
                    if bullet.pos.y > enemy.pos.y - 26 and bullet.pos.y < enemy.pos.y:
                        if bullet.pos.x > enemy.pos.x and bullet.pos.x < enemy.pos.x + 26:
                            #self.eList.remove(enemy)  # remove or lower health?
                            enemy.die()
                            BULLETS.remove(bullet)
                            #increase score
                            KILLED = KILLED + 1

            for bullet in E_BULLETS:
                if bullet.pos.y > playerOne.pos.y - 60:
                    if bullet.pos.x > playerOne.pos.x and bullet.pos.x < playerOne.pos.x + 75:
                        if playerOne.LIVES > 0:
                            playerOne.LIVES = playerOne.LIVES - 1
                        E_BULLETS.remove(bullet)
                    elif bullet.pos.x > playerTwo.pos.x and bullet.pos.x < playerTwo.pos.x + 75:
                        if playerTwo.LIVES > 0:
                            playerTwo.LIVES = playerTwo.LIVES - 1
                        E_BULLETS.remove(bullet)

                    if playerOne.LIVES == 0 and playerTwo.LIVES == 0:
                        # Game over screen
                        sys.exit('Both players ran out of lives')
                    elif playerOne.LIVES == 0:
                        playerOne.stop()
                    elif playerTwo.LIVES == 0:
                        playerTwo.stop()

                #print('Player One lives: ' + str(playerOne.LIVES))
                #print('Player Two lives: ' + str(playerTwo.LIVES))


class Info:
    def __init__(self):
        self.pos = 0

    def draw(self, canvas):
        canvas.draw_line((0, 10), (CANVAS_WIDTH, 10), 30, 'Black')
        canvas.draw_text("Score:", (75, 18), 20, 'White', 'sans-serif')
        canvas.draw_text(str(KILLED), (125, 18), 20, 'Yellow', 'sans-serif')

        canvas.draw_text("P1 Lives:", (CANVAS_WIDTH - (CANVAS_WIDTH / 3), 18), 20, 'White', 'sans-serif')
        canvas.draw_text(str(playerOne.LIVES), (CANVAS_WIDTH - (CANVAS_WIDTH / 4.2), 18), 20, 'Red', 'sans-serif')
        #canvas.draw_image(simplegui.load_image('https://i.imgur.com/JH6xdz6.png'), (7.5, 7.5), (15, 15),
        #                  (CANVAS_WIDTH - 175, 13), (15, 15))

        canvas.draw_text("P2 Lives:", (CANVAS_WIDTH - (CANVAS_WIDTH / 5), 18), 20, 'White', 'sans-serif')
        canvas.draw_text(str(playerTwo.LIVES), (CANVAS_WIDTH - (CANVAS_WIDTH / 9.2), 18), 20, 'Red', 'sans-serif')
        #canvas.draw_image(simplegui.load_image('https://i.imgur.com/JH6xdz6.png'), (7.5, 7.5), (15, 15),
        #                  (CANVAS_WIDTH - 35, 13), (15, 15))

        if KILLED == (E_ROWS * E_COLS):
            canvas.draw_text("You Win!", (CANVAS_WIDTH/2.75, CANVAS_HEIGHT/2), 50, 'White', 'sans-serif')
            playerOne.stop()
            playerTwo.stop()

# class Game:


playerOne = Player('https://i.imgur.com/9e6rcxM.png')
playerTwo = Player('https://i.imgur.com/4QEvDrL.png')
controls = Controls(playerOne, playerTwo)
info = Info()
explo = Explosion((0, 0), False)


def make_walls():
    x = 200
    for i in range(3):
        wall = Vector(x, 475)
        WALLS.append(Walls(wall))
        x = x + 200


def make_enemies():
    for row in range(E_ROWS):
        for col in range(E_COLS):
            pos_v = Vector(ESX + (col * ENEMY_GAP), ESY + (row * ENEMY_GAP))
            ENEMIES.append(Enemy(pos_v))


def draw(canvas):
    global counter
    counter += 1
    inter.update()
    explo.draw(canvas)
    controls.update()
    playerOne.update()
    playerTwo.update()
    for bullet in BULLETS:
        bullet.update()
        bullet.draw(canvas)
    playerOne.draw(canvas)
    playerTwo.draw(canvas)

    for enemy in ENEMIES:
        enemy.draw(canvas)
        if counter % (100 - ENEMY_SPEED) == 0:
            enemy.update()
        enemy.shoot()

    for bullet in E_BULLETS:
        bullet.draw(canvas)
        bullet.move()

    for wall in WALLS:
        wall.draw(canvas)

    info.draw(canvas)


make_walls()
make_enemies()

inter = Interaction(E_BULLETS, BULLETS, playerOne, playerTwo, ENEMIES)

frame = simplegui.create_frame('Interactions', CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_canvas_background('#2C6A6A')
frame.set_draw_handler(draw)
frame.set_keydown_handler(controls.keyDown)
frame.set_keyup_handler(controls.keyUp)
frame.start()
