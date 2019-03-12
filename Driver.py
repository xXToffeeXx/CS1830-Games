import simpleguitk as simplegui
import math
import time
'''                                                                                   
THIS CODE BELOW ACTUALLY FUCKING WORKS IN CODESKULPTOR BUT NOT IN PYCHARM, FUCK       
'''

music = simplegui.load_sound("https://commondatastorage.googleapis.com/cs1830/Beachfront%20Celebration%20(1).mp3")
music.set_volume(0.3)

buttonState = 0
buttonSoundSplash = simplegui.load_sound("https://commondatastorage.googleapis.com/cs1830/439746__inspectorj__soprano-recorder-staccato-c.wav")

buttonOnPress = simplegui.load_sound("https://commondatastorage.googleapis.com/cs1830/243020__plasterbrain__game-start.ogg")
buttonOnPress.set_volume(0.6)

class Keyboard:
    def __init__(self):
        self.down = False
        self.up = False
        self.enter = False

    def keyDown(self, key):
        if key == simplegui.KEY_MAP['down'] or key == simplegui.KEY_MAP['s']:
            self.down = True

        if key == simplegui.KEY_MAP['up'] or key == simplegui.KEY_MAP['w']:
            self.up = True

        if key == simplegui.KEY_MAP['space'] or key == simplegui.KEY_MAP['e']:
             self.enter = True

    def keyUp(self, key):
        global buttonState

        if key == simplegui.KEY_MAP['down'] or key == simplegui.KEY_MAP['s']:
            self.down = False
            buttonState+=1
            if buttonState>3:
                buttonState = 0
            print(buttonState)
            buttonSoundSplash.play()
            time.sleep(0.1)

        if key == simplegui.KEY_MAP['up']or key == simplegui.KEY_MAP['w']:
            self.up = False
            buttonState-=1
            if buttonState<0:
                buttonState = 3
            print(buttonState)
            buttonSoundSplash.play()
            time.sleep(0.1)

        if key == simplegui.KEY_MAP['space'] or key == simplegui.KEY_MAP['e']:
            if buttonState == 0:
                print(gameButtonhandler())
                music.pause()
                buttonOnPress.play()
            if buttonState == 1:
                print(multigameButtonhandler())
                music.pause()
                buttonOnPress.play()
            if buttonState == 2:
                print(optionsHandler())
                music.pause()
                buttonOnPress.play()
            if buttonState == 3:
                print(extrasHandler())
                music.pause()        
                buttonOnPress.play() 

# loading background images and button shiz
genricbackground_image = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/GameBackground.png")
homemenubackground_image = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/GameBackgroundMenu.png")

MEMU_OPTIONS = 4
startgamebutton_image = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/StartGame.png")
optionsbutton_image = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/Options.png")
twoplayerbutton_image = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/Multiplayer.png")
extrasbutton_image = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/Extras.png")

startgamebutton_image_selected = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/StartGameSelected.png")
optionsbutton_image_selected = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/OptionsSelected.png")
twoplayerbutton_image_selected = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/MultiplayerSelected.png")
extrasbutton_image_selected = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/ExtrasSelected.png")

BACKGROUND_SIZE = [700, 1250]
BACKGROUND_CENTER = [350, 625]

#Creating the sizes for buttons
BUTTON_WIDTH = [400,150]
BUTTONONE_CENTER = [295,430]
BUTTONTWO_CENTER = [295,530]
BUTTONTHREE_CENTER = [295,630]
BUTTONFOUR_CENTER = [295, 730]
GENBUTTON_CENTER = [200, 75]

def gameButtonhandler():

    #TODO write the code for opening game and switching to a screen for gameplay
    print("Game open button pressed.")

def multigameButtonhandler():

    #TODO write the code for opening game and switching to a screen for multiplayer gameplay
    print("Game open for multiplayer button pressed.")

def optionsHandler():

    #TODO write the code for opening game and switching to a screen for options
    print("Options screen opened.")

def extrasHandler():
    #TODO write the code for opening game and switching to a screen for options
    print("Extras screen opened.")


kbd = Keyboard()
#code for drawing onto canvas
def draw(canvas):

    #DRAW IN THE BUTTONS and the MENU SCREEN
    canvas.draw_image(homemenubackground_image, BACKGROUND_CENTER, BACKGROUND_SIZE, BACKGROUND_CENTER, BACKGROUND_SIZE)

    if buttonState == 0:
        canvas.draw_image(startgamebutton_image_selected, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONONE_CENTER, BUTTON_WIDTH)
        canvas.draw_image(twoplayerbutton_image, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONTWO_CENTER, BUTTON_WIDTH)
        canvas.draw_image(optionsbutton_image, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONTHREE_CENTER, BUTTON_WIDTH)
        canvas.draw_image(extrasbutton_image, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONFOUR_CENTER, BUTTON_WIDTH)

    if buttonState == 1:
        canvas.draw_image(startgamebutton_image, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONONE_CENTER, BUTTON_WIDTH)
        canvas.draw_image(twoplayerbutton_image_selected, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONTWO_CENTER, BUTTON_WIDTH)
        canvas.draw_image(optionsbutton_image, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONTHREE_CENTER, BUTTON_WIDTH)
        canvas.draw_image(extrasbutton_image, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONFOUR_CENTER, BUTTON_WIDTH)

    if buttonState == 2:
        canvas.draw_image(startgamebutton_image, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONONE_CENTER, BUTTON_WIDTH)
        canvas.draw_image(twoplayerbutton_image, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONTWO_CENTER, BUTTON_WIDTH)
        canvas.draw_image(optionsbutton_image_selected, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONTHREE_CENTER, BUTTON_WIDTH)
        canvas.draw_image(extrasbutton_image, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONFOUR_CENTER, BUTTON_WIDTH)

    if buttonState == 3:
        canvas.draw_image(startgamebutton_image, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONONE_CENTER, BUTTON_WIDTH)
        canvas.draw_image(twoplayerbutton_image, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONTWO_CENTER, BUTTON_WIDTH)
        canvas.draw_image(optionsbutton_image, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONTHREE_CENTER, BUTTON_WIDTH)
        canvas.draw_image(extrasbutton_image_selected, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONFOUR_CENTER, BUTTON_WIDTH)

# create frame and size frame based on 240x296 pixel sprite
frame = simplegui.create_frame("This Game Has Bugs!", BACKGROUND_SIZE[0], BACKGROUND_SIZE[1])

# set draw handler and canvas background using custom HTML color
frame.set_draw_handler(draw)
frame.set_canvas_background("White")
frame.set_keydown_handler(kbd.keyDown)
frame.set_keyup_handler(kbd.keyUp)


# initialize counter for animation and start frame
counter = 0
frame.start()
music.play()