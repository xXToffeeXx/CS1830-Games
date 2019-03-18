from vector import Vector
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

import random
    
CANVAS_WIDTH = 540
CANVAS_HEIGHT = 540
GAME_STARTED = False
GAME_ENDED = False
LEVEL = 1
SCORE = 0
KILLED = 0
TIME = 0
BULLETS = []

class Sprite:
    def __init__(self, image, height, width):
        self.pos = Vector(CANVAS_WIDTH/2, CANVAS_HEIGHT-50)
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
    
    def __init__(self):
        super(Player,self).__init__('https://i.imgur.com/9e6rcxM.png', 75, 75)
        
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
    
    def __init__(self, pos, direction):
        super(Bullet,self).__init__('https://i.imgur.com/alE94NY.png', 10, 3)
        self.pos = pos
        if direction == "UP":
            self.direction = Vector(0,-2)
        else:
            self.direction = Vector(0,2)
        
    def update(self):
        self.pos.add(self.direction)

    
#class Game:

playerOne = Player()
playerTwo = Player()
controls = Controls(playerOne, playerTwo)

def draw(canvas):
    controls.update()
    playerOne.update()
    playerTwo.update()
    for bullet in BULLETS:
        bullet.update()
        bullet.draw(canvas)
    playerOne.draw(canvas)
    playerTwo.draw(canvas)

frame = simplegui.create_frame('Interactions', CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_canvas_background('#2C6A6A')
frame.set_draw_handler(draw)
frame.set_keydown_handler(controls.keyDown)
frame.set_keyup_handler(controls.keyUp)
frame.start()    