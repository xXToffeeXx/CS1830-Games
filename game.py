try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

import math, random, sys, time

from vector import Vector

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
GAME_STARTED = False
GAME_ENDED = False
LEVEL = 1
SCORE = 0
KILLED = 0
TIME = 0
BULLETS = []
BULLET_SPEED = 7
POWER_UPS = []
POWER_UP_SPEED = 7

### ENEMY CONSTANTS ###
ENEMIES = []
ENEMY_SPEED = 60
ENEMY_GAP = 35
ENEMY_JUMP = 21
ENEMY_JUMP_DOWN = 40
ENEMY_JUMP_ADJUST = 15
ESX = 50
ESY = 75
E_ROWS = 4
E_COLS = 9
E_BULLETS = []
E_BULLET_SPEED = 5
counter = 0
WALLS = []
gameover = False
magic = 2000

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
    
    def get_height(self):
        return self.display_size[1]

    def get_width(self):
        return self.display_size[0]

    def is_overlapping(self, other):
        if (self.pos.y + self.get_height() // 2 + 2 > other.pos.y - other.get_height() // 2) and (
                    self.pos.y - self.get_height() // 2 - 2 < other.pos.y + other.get_height() // 2):
            if (self.pos.x + self.get_width() // 2 + 2 > other.pos.x - other.get_width() // 2) and (
                        self.pos.x - self.get_width() // 2 - 2 < other.pos.x + other.get_width() // 2):
                return True
            else:
                return False
        else:
            return False


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
        self.image = image
        super(Player, self).__init__(image, 40, 40, self.startpos)
        self.display_size = (40, self.source_size[1] * (self.display_size[0] / self.source_size[0]))
        self.disable = False

    def update(self):
        new_pos = self.pos.copy()
        new_pos.add(self.vel)
        if not self.disable:
            if (new_pos.x > self.margin) and (new_pos.x < (CANVAS_WIDTH - self.margin)):
                self.pos = new_pos.copy()
                self.vel.multiply(self.velocity)
            else:
                self.vel.multiply(0)
        elif self.disable:
            self.vel.multiply(0)

    def stop(self):
        self.disable = True

    def getPosition(self):
        return self.pos

class Bullet(Sprite):
    direction = None
    startpos = Vector(CANVAS_WIDTH / 2, CANVAS_HEIGHT - 50)

    def __init__(self, pos, direction):
        super(Bullet, self).__init__('https://i.imgur.com/n08NeaE.png', 10, 10, self.startpos)
        self.pos = pos

        if direction == "UP":
            self.direction = Vector(0, -BULLET_SPEED)
        else:
            self.direction = Vector(0, BULLET_SPEED)

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

        #print(self.pos.y)

        if self.pos.y >= CANVAS_HEIGHT - 50:
            global gameover
            playerOne.stop()
            playerTwo.stop()
            gameover = True

    def move_down(self):
        self.pos.y += ENEMY_JUMP_DOWN
        if self.right:
            self.pos.x += -ENEMY_JUMP_DOWN + ENEMY_JUMP_ADJUST
            self.right = False
        elif not self.right:
            self.pos.x += ENEMY_JUMP_DOWN - ENEMY_JUMP_ADJUST
            self.right = True


    def shoot(self):
        global magic
        if len(ENEMIES) <= ((E_ROWS * E_COLS) - E_COLS):
            magic = 1250
        if len(ENEMIES) <= ((E_ROWS * E_COLS) - E_COLS * 2):
            magic = 750
        if len(ENEMIES) <= ((E_ROWS * E_COLS) - E_COLS * 3):
            magic = 500
        if (random.randint(1, magic)) == 1:
            b = Vector(self.pos.x, self.pos.y)
            E_BULLETS.append(EnemyBullet(b))

    def die(self):
        global explo
        get_pos = (self.pos.x, self.pos.y)
        ENEMIES.remove(self)
        explo = Explosion(get_pos, True)
        #power_up = random.choice(['BULLETS'] * 5 + ['LIFE'] * 5 + ['NONE'] * 90)
        power_up = random.choice(['BULLETS'] * 50 + ['LIFE'] * 50 + ['NONE'] * 0)
        if power_up == 'BULLETS':
            POWER_UPS.append(FasterBullets(self.pos))
        if power_up == 'LIFE':
            POWER_UPS.append(ExtraLife(self.pos))


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
        if self.truth:
            if self.now >= counter:
                canvas.draw_image(self.death_img, (12.5, 12.5), (25, 25), self.pos, (25, 25))
            else:
                self.truth = False


class EnemyBullet(Sprite):
    def __init__(self, pos):
        self.pos = pos
        super(EnemyBullet, self).__init__('https://i.imgur.com/9t4g4Ey.png', 16, 16, self.pos)
        self.speed = E_BULLET_SPEED

    def move(self):
        self.pos.y += self.speed
        if self.pos.y > CANVAS_HEIGHT - 10:
            E_BULLETS.remove(self)

class PowerUp(Sprite):
    def __init__(self, image_url, pos):
        self.pos = pos
        super(PowerUp, self).__init__(image_url, 20, 20, self.pos)
        self.display_size = (20, self.source_size[1] * (self.display_size[0] / self.source_size[0]))
        self.speed = POWER_UP_SPEED

    def move(self):
        self.pos.y += self.speed
        if self.pos.y > CANVAS_HEIGHT + 50:
            POWER_UPS.remove(self)
    
    def trigger(self, player):
        pass

class ExtraLife(PowerUp):
    def __init__(self, pos):
        self.pos = pos
        super(ExtraLife, self).__init__("https://i.imgur.com/L36Lvzl.png", self.pos)
    
    def trigger(self, player):
        player.LIVES += 1

class FasterBullets(PowerUp):
    def __init__(self, pos):
        self.pos = pos
        super(FasterBullets, self).__init__("https://i.imgur.com/04UFt8J.png", self.pos)
    
    def trigger(self, player):
        global BULLET_SPEED
        BULLET_SPEED += 1

class Walls(Sprite):
    def __init__(self, pos):
        self.pos = pos
        super(Walls, self).__init__('https://i.imgur.com/zVKPBzx.png', 64, 72, self.pos)

    def update(self):
        pass


class Interaction:
    def __init__(self, EBULLETS, BULLETS, playerOne, playerTwo, eList, wList):
        self.E_BULLETS = EBULLETS
        self.BULLETS = BULLETS
        self.playerOne = playerOne
        self.playerTwo = playerTwo
        self.eList = eList
        self.wList = wList

    def update(self):
            global KILLED
            for bullet in BULLETS:
                for enemy in self.eList:
                    if bullet.is_overlapping(enemy):
                        #self.eList.remove(enemy)  # remove or lower health?
                        enemy.die()
                        if bullet in BULLETS: BULLETS.remove(bullet)
                        #increase score
                        KILLED = KILLED + 1

            for bullet in E_BULLETS:
                if bullet.is_overlapping(playerOne):
                    if playerOne.LIVES > 0:
                        playerOne.LIVES = playerOne.LIVES - 1
                    if bullet in E_BULLETS: E_BULLETS.remove(bullet)
                if bullet.is_overlapping(playerTwo):
                    if playerTwo.LIVES > 0:
                        playerTwo.LIVES = playerTwo.LIVES - 1
                    if bullet in E_BULLETS: E_BULLETS.remove(bullet)

                if playerOne.LIVES == 0 and playerTwo.LIVES == 0:
                    global gameover
                    gameover = True
                    # sys.exit('Both players ran out of lives')
                elif playerOne.LIVES == 0:
                    playerOne.stop()
                elif playerTwo.LIVES == 0:
                    playerTwo.stop()

                #print('Player One lives: ' + str(playerOne.LIVES))
                #print('Player Two lives: ' + str(playerTwo.LIVES))
            
            for power_up in POWER_UPS:
                if power_up.is_overlapping(playerOne):
                    power_up.trigger(playerOne)
                    if power_up in POWER_UPS: POWER_UPS.remove(power_up)
                if power_up.is_overlapping(playerTwo):
                    power_up.trigger(playerTwo)
                    if power_up in POWER_UPS: POWER_UPS.remove(power_up)

            for bullet in E_BULLETS:
                for wall in self.wList:
                    if bullet.is_overlapping(wall):
                        if bullet in E_BULLETS: E_BULLETS.remove(bullet)
                        WALLS.remove(wall)


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

        #canvas.draw_text("Time: " + str(ti), ((CANVAS_WIDTH - 400), 18), 20, 'White', 'sans-serif')

        #if KILLED == (E_ROWS * E_COLS):
        if KILLED == (E_ROWS * E_COLS):
            playerOne.stop()
            playerTwo.stop()

            game_over(canvas, 'win')

# class Game:


playerOne = Player('https://i.imgur.com/XEhhit6.png')
playerTwo = Player('https://i.imgur.com/JSEeuYR.png')
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
    inter.update()

    for enemy in ENEMIES:
        enemy.draw(canvas)
        if counter % (100 - ENEMY_SPEED) == 0:
            enemy.update()
        enemy.shoot()
    inter.update()

    for bullet in E_BULLETS:
        bullet.draw(canvas)
        bullet.move()
    inter.update()

    for power_up in POWER_UPS:
        power_up.draw(canvas)
        power_up.move()
    inter.update()

    for wall in WALLS:
        wall.draw(canvas)
    inter.update()

    info.draw(canvas)

    #if not ENEMIES:
    #   game_over(canvas, 'lose')

    if gameover:
        game_over(canvas, 'lose')


make_walls()
make_enemies()
incount = 0


def game_over(canvas, cond):
    global incount
    if gameover:
        cond = 'lose'
    if cond == 'win':
        canvas.draw_text("You Win!", (CANVAS_WIDTH / 2.75, CANVAS_HEIGHT / 2), 50, 'White', 'sans-serif')
        canvas.draw_text("Score: " + str(KILLED), (CANVAS_WIDTH / 2.55, CANVAS_HEIGHT / 1.75), 40, 'White',
                         'sans-serif')
        if incount >= 200:
            sys.exit()
        incount += 1
    if cond == 'lose':
        canvas.draw_polygon([[0, 0], [0, CANVAS_HEIGHT], [CANVAS_WIDTH, CANVAS_HEIGHT], [CANVAS_WIDTH, 0]], 12,
                                'Black', 'Black')
        canvas.draw_text("You Lose!", (CANVAS_WIDTH / 2.75, CANVAS_HEIGHT / 2), 50, 'White', 'sans-serif')
        canvas.draw_text("Score: " + str(KILLED), (CANVAS_WIDTH / 2.55, CANVAS_HEIGHT / 1.75), 40, 'White', 'sans-serif')
        if incount >= 200:
            sys.exit()
        incount += 1


inter = Interaction(E_BULLETS, BULLETS, playerOne, playerTwo, ENEMIES, WALLS)

frame = simplegui.create_frame('Interactions', CANVAS_WIDTH, CANVAS_HEIGHT)
frame._set_canvas_background_image(simplegui.load_image('https://imgur.com/JW464Qp.png'))
frame.set_draw_handler(draw)
frame.set_keydown_handler(controls.keyDown)
frame.set_keyup_handler(controls.keyUp)
frame.start()