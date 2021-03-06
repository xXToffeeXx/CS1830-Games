"""
CS1830 Group 01 Project 'This Game Has Bugs (Galaxy Raiders)
Please check the readme.txt for further information.
"""
# IMPORTS
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

import math, random, sys
from vector import Vector

# CONSTANTS
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
GAME_STARTED = False
GAME_ENDED = False
LEVEL = 0
SCORE = 0
KILLED = 0
TIME = 0
BULLETS = []
ENEMIES = []
BULLET_SPEED = 7
POWER_UPS = []
POWER_UP_SPEED = 7

ENEMIES = []
ENEMY_SPEED = 60
ENEMY_GAP = 35  # Space between each individual enemy sprite
ENEMY_JUMP = 21
ENEMY_JUMP_DOWN = 40  # Distance for the enemies to move down
ENEMY_JUMP_ADJUST = 15
ESX = 50  # Enemy start X
ESY = 75  # Enemy start Y
E_ROWS = 1  # Enemy rows
E_COLS = 1  # Enemy columns
E_BULLETS = []
E_BULLET_SPEED = 7
WALLS = []
gameover = False
counter = 0
magic = 2000


# CLASSES
class Sprite:
    """ Create sprites for various components of the game, such as the Player(s), Bullets, Walls and Enemies.

    This class also handles the animation of a sprite for the two Players, using the provided CS8130 sprite code.

    Some collision detection for the sprites is also handled, returning a boolean if two sprites are found to collide,
    which is later used in the Interaction class. """
    def __init__(self, image, height, width, pos, scale=1.75, duration=20):
        self.pos = pos
        self.vel = Vector()
        self.image = simplegui.load_image(image)
        self.margin = width / 2
        self.display_size = (width, height)
        self.source_size = (self.image.get_width(), self.image.get_height())
        self.source_center = (self.image.get_width() / 2, self.image.get_height() / 2)

        self.dims = (4, 1)
        self.scale = scale
        self.size = (140, 41)
        self.window = (28, 41)
        self.center = (self.window[0] / 2, self.window[1] / 2)
        self.offset = (0, 0)
        self.current = [0, 0]
        self.duration = duration
        self.previousFrame = 0

    def draw(self, canvas):
        if self.source_size == self.size:
            x = self.current[0] * self.window[0]
            y = self.current[1] * self.window[1]
            canvas.draw_image(self.image,
                              (self.center[0] + self.offset[0] + x, self.center[1] + self.offset[1] + y),
                              self.window, self.pos.getP(), (self.window[0] * self.scale, self.window[1] * self.scale))
        else:
            canvas.draw_image(self.image, self.source_center, self.source_size, self.pos.getP(), self.display_size)

    def nextFrame(self):
        self.current[0] = (self.current[0] + 1) % self.dims[0]
        if self.current[0] == 0:
            self.current[1] = (self.current[1] + 1) % self.dims[1]

    def previousFrame(self):
        pass

    def frameJump(self, time):
        frame = time / self.duration
        if (frame - self.previousFrame) >= 1:
            for i in range(round(frame - self.previousFrame)):
                self.nextFrame()
                self.previousFrame = frame

    def update(self):
        pass

    def get_height(self):
        return self.display_size[1]

    def get_width(self):
        return self.display_size[0]

    def is_overlapping(self, other):
        # Check if two sprites are overlapping/colliding
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
    """ Handles all controls that the players use.

    Also determines when a Player bullet is shot, depending on if the player is not disabled (as have run out of lives)
    and if the bullet cool down has elapsed. Cool down uses the counter (updated by 1 per game loop) to limit the
    frequency of bullets shot by a Player."""
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
    """ Create instances of the Player, and update each Player instance individually depending on input from keys.
    If a Player's lives reaches 0, they become disabled and are unable to move until the next level."""
    lives = 3
    velocity = 0.75
    start_pos = Vector(CANVAS_WIDTH / 2, CANVAS_HEIGHT - 50)

    def __init__(self, image):
        self.image = image
        super(Player, self).__init__(image, 40, 40, self.start_pos)
        self.source_size = (self.image.get_width(), self.image.get_height())
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
    """ Create bullets for the Players. Bullet direction is determined by when the Player presses the corresponding key,
    and if bullet cool down has passed. """
    direction = None
    start_pos = Vector(CANVAS_WIDTH / 2, CANVAS_HEIGHT - 50)

    def __init__(self, pos, direction):
        super(Bullet, self).__init__('https://i.imgur.com/n08NeaE.png', 10, 10, self.start_pos)
        self.pos = pos

        if direction == "UP":
            self.direction = Vector(0, -BULLET_SPEED)
        else:
            self.direction = Vector(0, BULLET_SPEED)

    def update(self):
        self.pos.add(self.direction)


class Enemy(Sprite):
    """ Handle Enemies both individually, as well as a group.
    This handles how enemies move left and right, how and when they move down (and then switch direction),
    when they should shoot and what happens when one is hit. """
    def __init__(self, pos):
        self.pos = pos
        self.image = 'https://i.imgur.com/2e24IN1.png'
        super(Enemy, self).__init__(self.image, 34, 34, self.pos)
        self.right = True
        self.down_right = 0
        self.down_left = ENEMY_MAX_MOVES

    def update(self):
        # Based on the maximum enemy moves, move the enemies left or right, and decide when they need to be moved down
        # the screen.
        global ENEMY_MAX_MOVES

        if self.right:
            self.pos.add(Vector(ENEMY_JUMP, 0))
            self.down_right += 1

            if self.down_right == ENEMY_MAX_MOVES:
                self.move_down()
                self.down_right = 0

        elif not self.right:
            self.pos.subtract(Vector(ENEMY_JUMP, 0))
            self.down_left -= 1

            if self.down_left == 0:
                self.move_down()
                self.down_left = ENEMY_MAX_MOVES

        if self.pos.y >= CANVAS_HEIGHT - 50:
            global gameover
            playerOne.stop()
            playerTwo.stop()
            gameover = True

    def move_down(self):
        # Handle the movement down of all the enemies.
        self.pos.y += ENEMY_JUMP_DOWN
        if self.right:
            self.pos.x += -ENEMY_JUMP_DOWN + ENEMY_JUMP_ADJUST
            self.right = False
        elif not self.right:
            self.pos.x += ENEMY_JUMP_DOWN - ENEMY_JUMP_ADJUST
            self.right = True

    def shoot(self):
        # Determine when the enemies should shoot. Shooting is random, but frequency depends on how many enemies exist
        # per level, and how many remain in that level.
        global magic
        removed = (E_COLS * E_ROWS) - len(ENEMIES)
        remaining = (E_ROWS * E_COLS) - removed

        level_inc = 80 - (LEVEL * 5)
        if level_inc <= 10:
            level_inc = 10

        magic = (remaining * level_inc)

        if (random.randint(1, magic)) == 1:
            b = Vector(self.pos.x, self.pos.y)
            E_BULLETS.append(EnemyBullet(b))

    def die(self):
        # Handle when a single enemy is hit by a player bullet, and potentially spawn in a powerup for the Player to
        # catch.
        global explo
        get_pos = (self.pos.x, self.pos.y)
        ENEMIES.remove(self)
        explo = Explosion(get_pos, True)
        power_up = random.choice(['BULLETS'] * 5 + ['LIFE'] * 5 + ['NONE'] * 90)
        if power_up == 'BULLETS':
            POWER_UPS.append(FasterBullets(self.pos))
        if power_up == 'LIFE':
            POWER_UPS.append(ExtraLife(self.pos))


class Explosion:
    """ Simple class to display an explosion effect once an Enemy sprite is hit by a Player bullet. """
    def __init__(self, pos, truth):
        self.pos = pos
        self.truth = truth
        self.cooldown = 20
        self.now = counter + self.cooldown
        self.death_img = simplegui.load_image('https://i.imgur.com/YmWrpV5.png')

    def draw(self, canvas):
        if self.truth:
            if self.now >= counter:
                canvas.draw_image(self.death_img, (12.5, 12.5), (25, 25), self.pos, (25, 25))
            else:
                self.truth = False


class EnemyBullet(Sprite):
    """ Handle enemy bullets, their sprite and their movement."""
    def __init__(self, pos):
        self.pos = pos
        super(EnemyBullet, self).__init__('https://i.imgur.com/9t4g4Ey.png', 16, 16, self.pos)
        self.speed = E_BULLET_SPEED

    def move(self):
        self.pos.y += self.speed
        if self.pos.y > CANVAS_HEIGHT - 10:
            E_BULLETS.remove(self)


class PowerUp(Sprite):
    """ Handles two extras that are spawned randomly on an Enemy's death. """
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
    """ A powerup that provides one Player (if they catch it) one extra life for that level. """
    def __init__(self, pos):
        self.pos = pos
        super(ExtraLife, self).__init__("https://i.imgur.com/L36Lvzl.png", self.pos)

    def trigger(self, player):
        # What the player receives from the powerup.
        player.lives += 1


class FasterBullets(PowerUp):
    """ A powerup that provides both Players an increase in bullet speed for that level."""
    def __init__(self, pos):
        self.pos = pos
        super(FasterBullets, self).__init__("https://i.imgur.com/04UFt8J.png", self.pos)

    def trigger(self, player):
        # What the player receives from the powerup.
        global BULLET_SPEED
        BULLET_SPEED += 3


class Walls(Sprite):
    """ Create instances of a Wall/Barrier that sit at the bottom of the screen (above Players), blocking Enemy and
    Player bullets. Enemy bullets breakdown the barrier and eventually will remove it from the screen if it is hit
    repeatedly. """
    def __init__(self, pos, image, health):
        self.pos = pos
        super(Walls, self).__init__(image, 25, 60, self.pos)
        self.health = health

    def update(self):
        # Change the wall's sprite depending on it's current health, remove if it is 0.
        if self.health == 3:
            temp = self.pos
            temp_health = self.health
            WALLS.remove(self)
            WALLS.append(Walls(temp, 'https://imgur.com/stHhfix.png', temp_health))
        if self.health == 1:
            temp = self.pos
            temp_health = self.health
            WALLS.remove(self)
            WALLS.append(Walls(temp, 'https://imgur.com/sWpz8vX.png', temp_health))
        if self.health <= 0:
            WALLS.remove(self)


class Interaction:
    """ Handle interactions between various Sprite-based elements in the game, mainly the Enemies, Bullets, Players and
    Walls. Per update, it will check the positions of each of these elements in their respective lists, and deal with
    collisions accordingly."""
    def __init__(self, EBULLETS, BULLETS, playerOne, playerTwo, eList, wList):
        self.E_BULLETS = EBULLETS
        self.BULLETS = BULLETS
        self.playerOne = playerOne
        self.playerTwo = playerTwo
        self.eList = eList
        self.wList = wList

    def update(self):
        # Various methods to decide how to handle collisions between multiple objects, such as bullets hitting walls,
        # powerups touching players etc.
        global KILLED
        for bullet in BULLETS:
            for enemy in self.eList:
                if bullet.is_overlapping(enemy):
                    enemy.die()
                    if bullet in BULLETS:
                        BULLETS.remove(bullet)
                    KILLED = KILLED + 1

        for bullet in E_BULLETS:
            if bullet.is_overlapping(playerOne):
                if playerOne.lives > 0:
                    playerOne.lives = playerOne.lives - 1
                if bullet in E_BULLETS:
                    E_BULLETS.remove(bullet)
            if bullet.is_overlapping(playerTwo):
                if playerTwo.lives > 0:
                    playerTwo.lives = playerTwo.lives - 1
                if bullet in E_BULLETS:
                    E_BULLETS.remove(bullet)

            if playerOne.lives == 0 and playerTwo.lives == 0:
                global gameover
                gameover = True
            elif playerOne.lives == 0:
                playerOne.stop()
            elif playerTwo.lives == 0:
                playerTwo.stop()

        for power_up in POWER_UPS:
            if power_up.is_overlapping(playerOne):
                power_up.trigger(playerOne)
                if power_up in POWER_UPS:
                    POWER_UPS.remove(power_up)
            if power_up.is_overlapping(playerTwo):
                power_up.trigger(playerTwo)
                if power_up in POWER_UPS:
                    POWER_UPS.remove(power_up)

        for bullet in E_BULLETS:
            for wall in self.wList:
                if bullet.is_overlapping(wall):
                    if bullet in E_BULLETS:
                        E_BULLETS.remove(bullet)
                        wall.health -= 1
                        if wall.health == 3:
                            temp = wall.pos
                            temp_health = wall.health
                            WALLS.remove(wall)
                            WALLS.append(Walls(temp, 'https://imgur.com/stHhfix.png', temp_health))
                        if wall.health == 1:
                            temp = wall.pos
                            temp_health = wall.health
                            WALLS.remove(wall)
                            WALLS.append(Walls(temp, 'https://imgur.com/sWpz8vX.png', temp_health))
                        if wall.health <= 0:
                            WALLS.remove(wall)

        for bullet in BULLETS:
            for wall in self.wList:
                if bullet.is_overlapping(wall):
                    if bullet in BULLETS:
                        BULLETS.remove(bullet)


class Info:
    """ Display various bits of information to the screen for the Players, such as the score, level and lives left."""
    def __init__(self):
        self.pos = 0

    def draw(self, canvas):
        canvas.draw_line((0, 10), (CANVAS_WIDTH, 10), 30, 'Black')
        canvas.draw_text("Score:", (75, 18), 20, 'White', 'sans-serif')
        canvas.draw_text(str(KILLED), (130, 19), 20, 'Yellow', 'sans-serif')

        canvas.draw_text("P1 lives:", (CANVAS_WIDTH - (CANVAS_WIDTH / 3), 18), 20, 'White', 'sans-serif')
        canvas.draw_text(str(playerOne.lives), (CANVAS_WIDTH - (CANVAS_WIDTH / 4.1), 19), 20, 'Red', 'sans-serif')

        canvas.draw_text("P2 lives:", (CANVAS_WIDTH - (CANVAS_WIDTH / 5), 18), 20, 'White', 'sans-serif')
        canvas.draw_text(str(playerTwo.lives), (CANVAS_WIDTH - (CANVAS_WIDTH / 9.1), 19), 20, 'Red', 'sans-serif')

        canvas.draw_text("Level: ", (CANVAS_WIDTH - (CANVAS_WIDTH / 1.3), 18), 20, 'White', 'sans-serif')
        canvas.draw_text(str(LEVEL), (CANVAS_WIDTH - (CANVAS_WIDTH / 1.42), 18), 20, 'Orange', 'sans-serif')

        if not ENEMIES:  # if ENEMIES is empty
            playerOne.stop()
            playerTwo.stop()

            Game.game_over(Game, canvas, 'win')


# INSTANCE DECLARATION
playerOne = Player('https://imgur.com/Fv4pWIo.png')
playerTwo = Player('https://imgur.com/7NQXsfx.png')
controls = Controls(playerOne, playerTwo)
info = Info()
explo = Explosion((0, 0), False)
inter = Interaction(E_BULLETS, BULLETS, playerOne, playerTwo, ENEMIES, WALLS)
incount = 0
start = False


# GAME LOOP
class Game:
    """ Main loop for the game where calls are handled.

    First, the game is set up, and if it is the first time then
    helpful control information is displayed. Walls and enemies are created, and the draw function begins drawing to the
    screen. When a level is completed, a screen appears momentarily displaying level completion and current score.
    Levels increase in difficulty, adding increased enemy numbers, speed and bullet frequency. The game is reset per
    level except for these constants which are added to. Once both Players die, another screen appears with the score,
    then the game exits."""
    def __init__(self):
        self.p = 1

    def set_up(self):
        global LEVEL, start
        LEVEL = LEVEL + 1
        if LEVEL == 1:
            start = True
        self.reset()
        self.make_enemies()
        self.make_walls()

    def start(self, canvas):
        # Only displayed on the first level at the start of the game.
        global incount, start
        canvas.draw_text("Player 1: A = left, D = right, S = shoot", (CANVAS_WIDTH / 4.5, CANVAS_HEIGHT / 2), 30,
                         'White', 'sans-serif')
        canvas.draw_text("Player 2: J = left, L = right, K = shoot", (CANVAS_WIDTH / 4.4, CANVAS_HEIGHT / 1.75), 30,
                         'White', 'sans-serif')

        if incount >= 400:
            incount = 0
            start = False
        incount += 1

    def reset(self):
        # Reset the canvas on level increase.
        global E_ROWS
        global E_COLS
        global ENEMY_SPEED
        global incount
        global ENEMY_MAX_MOVES
        playerOne.lives = 3
        playerTwo.lives = 3
        playerOne.disable = False
        playerTwo.disable = False
        BULLETS.clear()
        E_BULLETS.clear()
        ENEMIES.clear()
        WALLS.clear()
        E_ROWS = 4
        E_COLS = 4 + LEVEL
        ENEMY_SPEED = 50 + (LEVEL * 5)
        incount = 0
        ENEMY_MAX_MOVES = (43 + E_COLS) - (E_ROWS * E_COLS) + LEVEL

    def make_walls(self):
        # Create a list of walls to be displayed on canvas.
        x = 150
        for i in range(3):
            wall = Vector(x, 475)
            WALLS.append(Walls(wall, 'https://imgur.com/XxwRdFl.png', 4))
            x = x + 250

    def make_enemies(self):
        # Create a list of enemies to be displayed on canvas.
        ENEMIES.clear()
        for row in range(E_ROWS):
            for col in range(E_COLS):
                pos_v = Vector(ESX + (col * ENEMY_GAP), ESY + (row * ENEMY_GAP))
                ENEMIES.append(Enemy(pos_v))

    def draw(self, canvas):
        # Draw the various elements to the screen, including their movements.
        global counter
        counter += 1

        if start:
            self.start(canvas)

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
        playerOne.frameJump(counter)
        playerTwo.frameJump(counter)

        for enemy in ENEMIES:
            enemy.draw(canvas)
            if counter % (100 - ENEMY_SPEED) == 0:
                enemy.update()
            enemy.shoot()

        for bullet in E_BULLETS:
            bullet.draw(canvas)
            bullet.move()

        for power_up in POWER_UPS:
            power_up.draw(canvas)
            power_up.move()

        for wall in WALLS:
            wall.draw(canvas)

        info.draw(canvas)

        if gameover:
            self.game_over(canvas, 'lose')

    def game_over(self, canvas, cond):
        # Handle the various game over conditions (as well as moving to the next level if all enemies are defeated).
        global incount
        if gameover:
            cond = 'lose'
        if cond == 'win':
            canvas.draw_text("Level " + str(LEVEL) + " cleared!", (CANVAS_WIDTH / 3, CANVAS_HEIGHT / 2), 50, 'White',
                             'sans-serif')
            canvas.draw_text("Score: " + str(KILLED), (CANVAS_WIDTH / 3, CANVAS_HEIGHT / 1.75), 40, 'White',
                             'sans-serif')
            if incount >= 200:
                game.set_up()
            incount += 1
        if cond == 'lose':
            canvas.draw_polygon([[0, 0], [0, CANVAS_HEIGHT], [CANVAS_WIDTH, CANVAS_HEIGHT], [CANVAS_WIDTH, 0]], 12,
                                'Black', 'Black')
            canvas.draw_text("You Lose!", (CANVAS_WIDTH / 2.75, CANVAS_HEIGHT / 2), 50, 'White', 'sans-serif')
            canvas.draw_text("Score: " + str(KILLED), (CANVAS_WIDTH / 2.55, CANVAS_HEIGHT / 1.75), 40, 'White',
                             'sans-serif')
            if incount >= 200:
                sys.exit()
            incount += 1

    def main(self):
        global game
        game.set_up()

        frame = simplegui.create_frame('This Game Has Bugs (Galaxy Raiders)', CANVAS_WIDTH, CANVAS_HEIGHT)
        frame._set_canvas_background_image(simplegui.load_image('https://imgur.com/JW464Qp.png'))
        frame.set_draw_handler(self.draw)
        frame.set_keydown_handler(controls.keyDown)
        frame.set_keyup_handler(controls.keyUp)
        frame.start()


game = Game()
game.main()
