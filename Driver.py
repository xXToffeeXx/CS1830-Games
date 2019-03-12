import simpleguitk as simplegui
import math
import time


tempa = (0,0)
tempb = (0,0)
tempc = (0,0)

class Arrow:
    def __init__(self, pointA, pointB, pointC ):
        self.state = 0
        self.pointA = pointA
        self.pointB = pointB
        self.pointC = pointC

        self.pointD = (pointA[0], pointA[1]+100)
        self.pointE = (pointB[0], pointB[1]+100)
        self.pointF = (pointC[0], pointC[1]+100)

        self.pointG = (pointA[0], pointA[1]+200)
        self.pointH = (pointB[0], pointB[1]+200)
        self.pointI = (pointC[0], pointC[1]+200)


    def draw(self, canvas):
        canvas.draw_polygon(((self.pointA), (self.pointB), (self.pointC)), 2, "Black", "Green")

    def update(self):
        global tempa, tempb, tempc

        if self.state == 1:
            tempa = self.pointA
            self.pointA = self.pointD
            self.pointD = tempa

            tempb = self.pointB
            self.pointB = self.pointE
            self.pointE = tempb

            tempc = self.pointC
            self.pointC = self.pointF
            self.pointF = tempc

        if self.state == 2:
            self.pointA = self.pointG
            self.pointB = self.pointH
            self.pointC = self.pointI

        if self.state > 2:
            self.pointA = tempa
            self.pointB = tempb
            self.pointC = tempc

class Keyboard:
    def __init__(self):
        self.down = False

    def keyDown(self, key):
        if key == simplegui.KEY_MAP['down']:
            self.down = True
            print("Key is down")

    def keyUp(self, key):
        if key == simplegui.KEY_MAP['down']:
            self.down = False


class Interaction:
    def __init__(self, arrow, keyboard):
        self.arrow = arrow
        self.keyboard = keyboard

    def update(self):
        if self.keyboard.down:
            print("Keyboard down")
            self.arrow.state+=1
            time.sleep(1.2)


#
# loading background images and button shiz
genricbackground_image = simplegui.load_image("http://funkyimg.com/i/2Segu.png")
homemenubackground_image = simplegui.load_image("http://funkyimg.com/i/2SeFG.png")
startgamebutton_image = simplegui.load_image("http://funkyimg.com/i/2SeKD.png")
optionsbutton_image = simplegui.load_image("http://funkyimg.com/i/2SeD6.png")
twoplayerbutton_image = simplegui.load_image("http://funkyimg.com/i/2SeD5.png")
menuarrow = simplegui.load_image("http://funkyimg.com/i/2Sf3r.png")

BACKGROUND_SIZE = [700, 1250]
BACKGROUND_CENTER = [350, 625]

#Creating the sizes for buttons
BUTTON_WIDTH = [400,150]
BUTTONONE_CENTER = [295,430]
BUTTONTWO_CENTER = [295,530]
BUTTONTHREE_CENTER = [295,630]
GENBUTTON_CENTER = [200, 75]

ARROW_START = [550, 430]
ARROW_CENTER = [69, 75]
ARROW_WIDTH = [139, 150]

def gameButtonhandler():

    #TODO write the code for opening game
    print("Game open button pressed.")


pointer = Arrow((510, 430),(550, 410),(550, 450))
kbd = Keyboard()
inter = Interaction(pointer, kbd)

#code for drawing onto canvas
def draw(canvas):

    #DRAW IN THE BUTTONS and the MENU SCREEN
    canvas.draw_image(homemenubackground_image, BACKGROUND_CENTER, BACKGROUND_SIZE, BACKGROUND_CENTER, BACKGROUND_SIZE)
    canvas.draw_image(startgamebutton_image, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONONE_CENTER, BUTTON_WIDTH)
    canvas.draw_image(twoplayerbutton_image, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONTWO_CENTER, BUTTON_WIDTH)
    canvas.draw_image(optionsbutton_image, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONTHREE_CENTER, BUTTON_WIDTH)
    #canvas.draw_image(menuarrow, ARROW_CENTER, ARROW_WIDTH , ARROW_START, ARROW_WIDTH )

    inter.update()
    pointer.update()
    pointer.draw(canvas)

# create frame and size frame based on 240x296 pixel sprite
frame = simplegui.create_frame("This Game Has Bugs!", BACKGROUND_SIZE[0], BACKGROUND_SIZE[1])

# set draw handler and canvas background using custom HTML color
frame.set_draw_handler(draw)
frame.set_canvas_background("White")
frame.set_keydown_handler(kbd.keyDown)
frame.set_keyup_handler(kbd.keyUp)
'''
THIS CODE BELOW ACTUALLY FUCKING WORKS IN CODESKULPTOR BUT NOT IN PYCHARM, FUCK
'''
#music = simplegui.load_sound("https://commondatastorage.googleapis.com/cs1830/Beachfront%20Celebration%20(1).mp3")
#music.play()

# initialize counter for animation and start frame
counter = 0
frame.start()