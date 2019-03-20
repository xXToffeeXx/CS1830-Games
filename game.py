try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from vector import Vector
import math, random
    
CANVAS_WIDTH = 540
CANVAS_HEIGHT = 540
GAME_STARTED = False
GAME_ENDED = False
LEVEL = 1
SCORE = 0
KILLED = 0
TIME = 0
BULLETS = []

### ENEMY CONSTANTS ###
ENEMIES = []
ENEMY_SPEED = 20
ENEMY_GAP = 40
ENEMY_JUMP = 30
ESX = 50
ESY = 50
E_ROWS = 3
E_COLS = 6
E_BULLETS = []
BULLET_SPEED = 2
counter = 0
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
        if key == simplegui.KEY_MAP['s']:
            BULLETS.append(Bullet(self.p1.getPosition(), "UP"))
        if key == simplegui.KEY_MAP['k']:
            BULLETS.append(Bullet(self.p2.getPosition(), "UP"))

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
    #LIVES = 3
    velocity = 0.75
    startpos = Vector(CANVAS_WIDTH/2, CANVAS_HEIGHT-50)
    
    def __init__(self):
        super(Player,self).__init__('https://i.imgur.com/9e6rcxM.png', 75, 75, self.startpos)
        
    def update(self):
        new_pos = self.pos.copy()
        new_pos.add(self.vel)
        if (new_pos.x > self.margin) and (new_pos.x < (CANVAS_WIDTH - self.margin)):
            self.pos = new_pos.copy()
            self.vel.multiply(self.velocity)
        else:
            self.vel.multiply(0)

    def getPosition(self):
        return self.pos


class Bullet(Sprite):
    direction = None
    startpos = Vector(CANVAS_WIDTH/2, CANVAS_HEIGHT-50)
    
    def __init__(self, pos, direction):
        super(Bullet,self).__init__('https://i.imgur.com/alE94NY.png', 10, 3, self.startpos)
        self.pos = pos
        if direction == "UP":
            self.direction = Vector(0,-2)
        else:
            self.direction = Vector(0,2)
        
    def update(self):
        self.pos.add(self.direction)


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
                self.downright = 0

        elif not self.right:
            self.pos.subtract(Vector(ENEMY_JUMP, 0))
            self.downleft -= 1

            if self.downleft == 0:
                self.move_down()
                self.downleft = ENEMY_MAX_MOVES

    def move_down(self):
        self.pos.y += 25
        if self.right:
            self.pos.x += -25
            self.right = False
        elif not self.right:
            self.pos.x += 25
            self.right = True

    def shoot(self):
        if (random.randint(1, 750)) == 1:
            b = Vector(self.pos.x, self.pos.y)
            E_BULLETS.append(EnemyBullet(b))

    def die(self):
        ENEMIES.remove(self)

    def get_pos_x(self):
        return self.pos.x


class EnemyBullet(Sprite):
    def __init__(self, pos):
        self.pos = pos
        super(EnemyBullet, self).__init__('https://i.imgur.com/9t4g4Ey.png', 16, 16, self.pos)
        self.speed = BULLET_SPEED

    def move(self):
        self.pos.y += self.speed
        if self.pos.y > CANVAS_HEIGHT - 10:
            E_BULLETS.remove(self)

#class Game:

playerOne = Player()
playerTwo = Player()
controls = Controls(playerOne, playerTwo)

def make_enemies():
    for row in range(E_ROWS):
        for col in range(E_COLS):
            pos_v = Vector(ESX + (col * ENEMY_GAP), ESY + (row * ENEMY_GAP))
            ENEMIES.append(Enemy(pos_v))

def draw(canvas):
    global counter
    counter += 1

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

make_enemies()

frame = simplegui.create_frame('Interactions', CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_canvas_background('#2C6A6A')
frame.set_draw_handler(draw)
frame.set_keydown_handler(controls.keyDown)
frame.set_keyup_handler(controls.keyUp)
frame.start()    