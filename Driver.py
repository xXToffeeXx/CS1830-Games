import simpleguitk as simplegui
import math
import time
import random
import sys

'''
OKAY SO BASICALLY:
1. BOOLEANS TO DETERMINE WHICH SCREEN THE GAME SHOULD BE SHOWING
2. ASSIGN BOOLEANS IN METHODS CALLED BY PRESS OF SPACE OR e
3. THIS CHANGES WHAT IS DRAWN IN DRAW()
'''
mainMenu = True
gamePlay = False
multiGamePlay = False
options = False
extras = False

'''                                                                                   
THIS CODE BELOW ACTUALLY FUCKING WORKS IN CODESKULPTOR BUT NOT IN PYCHARM, FUCK       
'''

#assorted values determining fun stuff!
buttonState = 0
easterEggCounter = 0

'''
CODE BELOW USED TO DETERMINE THE BACKGROUND FOR THE HOME SCREEN
WEIGHTED HEAVILY IN FAVOUR OF SUMMER BACKGROUND BUT RAIN APPEARS ABOUT 1/3
'''
rainOrNo = random.randint(0,2)

if rainOrNo <= 1:   #SUMMER
    music = simplegui.load_sound\
        ("https://commondatastorage.googleapis.com/cs1830/Beachfront%20Celebration%20(1).mp3")
    music.set_volume(0.3)
else:                #RAINFOREST
    music = simplegui.load_sound\
        ("https://commondatastorage.googleapis.com/cs1830/462774__lg__20180616-tropical-rain-thailand-02.wav")
    music.set_volume(0.3)

buttonSoundSplash = simplegui.load_sound\
    ("https://commondatastorage.googleapis.com/cs1830/439746__inspectorj__soprano-recorder-staccato-c.wav")

buttonOnPress = simplegui.load_sound\
    ("https://commondatastorage.googleapis.com/cs1830/243020__plasterbrain__game-start.ogg")
buttonOnPress.set_volume(0.6)

ambient = simplegui.load_sound("https://commondatastorage.googleapis.com/cs1830/Forest%20at%20dawn.wav")
ambient.set_volume(0.2)

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
        global easterEggCounter

        if key == simplegui.KEY_MAP['down'] or key == simplegui.KEY_MAP['s']:
            self.down = False
            buttonState+=1
            if buttonState>4:
                buttonState = 0
            print(buttonState)
            easterEggCounter+=1
            print(easterEggCounter)
            buttonSoundSplash.play()
            time.sleep(0.1)

        if key == simplegui.KEY_MAP['up']or key == simplegui.KEY_MAP['w']:
            self.up = False
            buttonState-=1
            if buttonState<0:
                buttonState = 4
            print(buttonState)
            buttonSoundSplash.play()
            easterEggCounter =0
            time.sleep(0.1)

        if key == simplegui.KEY_MAP['space'] or key == simplegui.KEY_MAP['e']:
            if buttonState == 0:
                print(gameButtonhandler())
                music.pause()
                buttonOnPress.play()
                easterEgg()
            if buttonState == 1:
                print(multigameButtonhandler())
                music.pause()
                buttonOnPress.play()
                easterEgg()
            if buttonState == 2:
                print(optionsHandler())
                music.pause()
                buttonOnPress.play()
                easterEgg()
            if buttonState == 3:
                print(extrasHandler())
                music.pause()
                buttonOnPress.play()
                easterEgg()
            if buttonState == MENU_OPTIONS:
                music.pause()
                buttonOnPress.play()
                sys.exit()

def easterEgg():
    if easterEggCounter == 100:
        music.pause()
        print("You found an Easter Egg!")
        easterEggSong = simplegui.load_sound("https://commondatastorage.googleapis.com/cs1830/Spazzmatica%20Polka.mp3")
        easterEggSong.play()
    else:
        pass

'''
LOADING IN ALL ASSETS STORED ON GOOGLE CLOUD SERVICES
'''
genricbackground_image = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/GameBackground.png")
homemenubackground_image = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/GameBackgroundMenu.png")

genericbackground_raining = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/GameBackgroundRaining.png")
homebackground_raining = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/GameBackgroundMenuRaining.png")


startgamebutton_image = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/StartGame.png")
optionsbutton_image = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/Options.png")
twoplayerbutton_image = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/Multiplayer.png")
extrasbutton_image = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/Extras.png")
exitbutton_image = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/Exit.png")


startgamebutton_image_selected = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/StartGameSelected.png")
optionsbutton_image_selected = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/OptionsSelected.png")
twoplayerbutton_image_selected = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/MultiplayerSelected.png")
extrasbutton_image_selected = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/ExtrasSelected.png")
exitbutton_image_selected = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/ExitSelected.png")


rain = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/ezgif.com-gif-maker.png")
rain3 = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/ezgif.com-gif-maker.png")
rain2 = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/ezgif.com-gif-maker.png")

'''
ASSIGNING ALL CONSTANTS FOR VALUES USED IN CANVAS DRAWING
'''

BACKGROUND_SIZE = [700, 1250]
BACKGROUND_CENTER = [350, 625]

MENU_OPTIONS = 4

#Creating the sizes for buttons
BUTTON_WIDTH = [400,150]
BUTTONONE_CENTER = [295,430]
BUTTONTWO_CENTER = [295,530]
BUTTONTHREE_CENTER = [295,630]
BUTTONFOUR_CENTER = [295, 730]
BUTTONFIVE_CENTER = [295, 830]
GENBUTTON_CENTER = [200, 75]

#Size for Rain GIF
RAIN_CENTER = [500, 225]
RAIN_SIZE = [1000, 450]
RAIN_DIM = [8,1]

RAIN_CENTERONE = [300, 350]
RAIN_CENTERTW0 = [350, 675]
RAIN_CENTERTHREE = [400, 1050]


def volumeHandler(decider, volume):
    if decider == True:
        volume+=0.1
        if volume > 1:
            volume = 1
    elif decider == False:
        volume-=0.1
        if volume < 0:
            volume = 0
    return volume


'''
BUTTONHANDLERS ACTIVATED WHEN SPACEBAR OR e IS PRESSED ON GAMESTATE
'''
def gameButtonhandler():
    global mainMenu
    global gamePlay 
    #TODO write the code for opening game and switching to a screen for gameplay
    print("Game open button pressed.")
    mainMenu = False
    gamePlay = True

def multigameButtonhandler():
    global mainMenu
    global multiGamePlay

    #TODO write the code for opening game and switching to a screen for multiplayer gameplay
    print("Game open for multiplayer button pressed.")
    mainMenu = False
    multiGamePlay = True

def optionsHandler():
    global mainMenu
    global options

    #TODO write the code for opening game and switching to a screen for options
    print("Options screen opened.")
    mainMenu = False
    options = True

def extrasHandler():
    global mainMenu
    global extras

    #TODO write the code for opening game and switching to a screen for options
    print("Extras screen opened.")
    mainMenu = False
    extras = True

#code for drawing onto canvas
def draw(canvas):
    global counter, countera, counterb
    if mainMenu:
        #DRAW IN THE BUTTONS and the MENU SCREEN
        if rainOrNo <= 1:
            canvas.draw_image(homemenubackground_image, BACKGROUND_CENTER, BACKGROUND_SIZE, BACKGROUND_CENTER, BACKGROUND_SIZE)
        elif rainOrNo == 2:
            canvas.draw_image(homebackground_raining, BACKGROUND_CENTER, BACKGROUND_SIZE, BACKGROUND_CENTER, BACKGROUND_SIZE)
            '''
            Sprite Work in the menus for some rain!
            '''
            rain_index = [counter % RAIN_DIM[0], counter // RAIN_DIM[0]]
            canvas.draw_image(rain,
                              [RAIN_CENTER[0] + rain_index[0] * RAIN_SIZE[0],
                               RAIN_CENTER[1] + rain_index[1] * RAIN_SIZE[1]],
                               RAIN_SIZE, RAIN_CENTER, RAIN_SIZE)
            counter = (counter + 1) % (RAIN_DIM[0] * RAIN_DIM[1])

            rain_index2 = [countera % RAIN_DIM[0], countera // RAIN_DIM[0]]
            canvas.draw_image(rain2,
                              [RAIN_CENTER[0] + rain_index2[0] * RAIN_SIZE[0],
                               RAIN_CENTER[1] + rain_index2[1] * RAIN_SIZE[1]],
                               RAIN_SIZE, RAIN_CENTERTW0, RAIN_SIZE)
            countera = (countera + 1) % (RAIN_DIM[0] * RAIN_DIM[1])

            rain_index3 = [counterb % RAIN_DIM[0], counterb // RAIN_DIM[0]]
            canvas.draw_image(rain3,
                              [RAIN_CENTER [0] + rain_index3[0] * RAIN_SIZE[0],
                               RAIN_CENTER [1] + rain_index3[1] * RAIN_SIZE[1]],
                               RAIN_SIZE, RAIN_CENTERTHREE, RAIN_SIZE)
            counterb = (counterb + 1) % (RAIN_DIM[0] * RAIN_DIM[1])
            '''CODE FOR RAIN ENDS HERE, SPRITE SHEET AND THE SORT'''


        if buttonState == 0:
            canvas.draw_image(startgamebutton_image_selected, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONONE_CENTER, BUTTON_WIDTH)
            canvas.draw_image(twoplayerbutton_image, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONTWO_CENTER, BUTTON_WIDTH)
            canvas.draw_image(optionsbutton_image, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONTHREE_CENTER, BUTTON_WIDTH)
            canvas.draw_image(extrasbutton_image, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONFOUR_CENTER, BUTTON_WIDTH)
            canvas.draw_image(exitbutton_image, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONFIVE_CENTER, BUTTON_WIDTH)

        if buttonState == 1:
            canvas.draw_image(startgamebutton_image, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONONE_CENTER, BUTTON_WIDTH)
            canvas.draw_image(twoplayerbutton_image_selected, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONTWO_CENTER, BUTTON_WIDTH)
            canvas.draw_image(optionsbutton_image, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONTHREE_CENTER, BUTTON_WIDTH)
            canvas.draw_image(extrasbutton_image, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONFOUR_CENTER, BUTTON_WIDTH)
            canvas.draw_image(exitbutton_image, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONFIVE_CENTER, BUTTON_WIDTH)

        if buttonState == 2:
            canvas.draw_image(startgamebutton_image, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONONE_CENTER, BUTTON_WIDTH)
            canvas.draw_image(twoplayerbutton_image, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONTWO_CENTER, BUTTON_WIDTH)
            canvas.draw_image(optionsbutton_image_selected, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONTHREE_CENTER, BUTTON_WIDTH)
            canvas.draw_image(extrasbutton_image, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONFOUR_CENTER, BUTTON_WIDTH)
            canvas.draw_image(exitbutton_image, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONFIVE_CENTER, BUTTON_WIDTH)

        if buttonState == 3:
            canvas.draw_image(startgamebutton_image, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONONE_CENTER, BUTTON_WIDTH)
            canvas.draw_image(twoplayerbutton_image, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONTWO_CENTER, BUTTON_WIDTH)
            canvas.draw_image(optionsbutton_image, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONTHREE_CENTER, BUTTON_WIDTH)
            canvas.draw_image(extrasbutton_image_selected, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONFOUR_CENTER, BUTTON_WIDTH)
            canvas.draw_image(exitbutton_image, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONFIVE_CENTER, BUTTON_WIDTH)

        if buttonState == 4:
            canvas.draw_image(startgamebutton_image, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONONE_CENTER, BUTTON_WIDTH)
            canvas.draw_image(twoplayerbutton_image, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONTWO_CENTER, BUTTON_WIDTH)
            canvas.draw_image(optionsbutton_image, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONTHREE_CENTER, BUTTON_WIDTH)
            canvas.draw_image(extrasbutton_image, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONFOUR_CENTER, BUTTON_WIDTH)
            canvas.draw_image(exitbutton_image_selected, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONFIVE_CENTER, BUTTON_WIDTH)

    elif options:
        #DRAW IN THE BUTTONS and the MENU SCREEN
        if rainOrNo <= 1:
            canvas.draw_image(genricbackground_image, BACKGROUND_CENTER, BACKGROUND_SIZE, BACKGROUND_CENTER, BACKGROUND_SIZE)
        elif rainOrNo == 2:
            canvas.draw_image(genericbackground_raining, BACKGROUND_CENTER, BACKGROUND_SIZE, BACKGROUND_CENTER, BACKGROUND_SIZE)
            '''
            Sprite Work in the menus for some rain!
            '''
            rain_index = [counter % RAIN_DIM[0], counter // RAIN_DIM[0]]
            canvas.draw_image(rain,
                              [RAIN_CENTER[0] + rain_index[0] * RAIN_SIZE[0],
                               RAIN_CENTER[1] + rain_index[1] * RAIN_SIZE[1]],
                               RAIN_SIZE, RAIN_CENTER, RAIN_SIZE)
            counter = (counter + 1) % (RAIN_DIM[0] * RAIN_DIM[1])

            rain_index2 = [countera % RAIN_DIM[0], countera // RAIN_DIM[0]]
            canvas.draw_image(rain2,
                              [RAIN_CENTER[0] + rain_index2[0] * RAIN_SIZE[0],
                               RAIN_CENTER[1] + rain_index2[1] * RAIN_SIZE[1]],
                               RAIN_SIZE, RAIN_CENTERTW0, RAIN_SIZE)
            countera = (countera + 1) % (RAIN_DIM[0] * RAIN_DIM[1])

            rain_index3 = [counterb % RAIN_DIM[0], counterb // RAIN_DIM[0]]
            canvas.draw_image(rain3,
                              [RAIN_CENTER [0] + rain_index3[0] * RAIN_SIZE[0],
                               RAIN_CENTER [1] + rain_index3[1] * RAIN_SIZE[1]],
                               RAIN_SIZE, RAIN_CENTERTHREE, RAIN_SIZE)
            counterb = (counterb + 1) % (RAIN_DIM[0] * RAIN_DIM[1])
            '''CODE FOR RAIN ENDS HERE, SPRITE SHEET AND THE SORT'''

    elif extras:
        # DRAW IN THE BUTTONS and the MENU SCREEN
        if rainOrNo <= 1:
            canvas.draw_image(genricbackground_image, BACKGROUND_CENTER, BACKGROUND_SIZE, BACKGROUND_CENTER,
                              BACKGROUND_SIZE)
        elif rainOrNo == 2:
            canvas.draw_image(genericbackground_raining, BACKGROUND_CENTER, BACKGROUND_SIZE, BACKGROUND_CENTER,
                              BACKGROUND_SIZE)
            '''
            Sprite Work in the menus for some rain!
            '''
            rain_index = [counter % RAIN_DIM[0], counter // RAIN_DIM[0]]
            canvas.draw_image(rain,
                              [RAIN_CENTER[0] + rain_index[0] * RAIN_SIZE[0],
                               RAIN_CENTER[1] + rain_index[1] * RAIN_SIZE[1]],
                              RAIN_SIZE, RAIN_CENTER, RAIN_SIZE)
            counter = (counter + 1) % (RAIN_DIM[0] * RAIN_DIM[1])

            rain_index2 = [countera % RAIN_DIM[0], countera // RAIN_DIM[0]]
            canvas.draw_image(rain2,
                              [RAIN_CENTER[0] + rain_index2[0] * RAIN_SIZE[0],
                               RAIN_CENTER[1] + rain_index2[1] * RAIN_SIZE[1]],
                              RAIN_SIZE, RAIN_CENTERTW0, RAIN_SIZE)
            countera = (countera + 1) % (RAIN_DIM[0] * RAIN_DIM[1])

            rain_index3 = [counterb % RAIN_DIM[0], counterb // RAIN_DIM[0]]
            canvas.draw_image(rain3,
                              [RAIN_CENTER[0] + rain_index3[0] * RAIN_SIZE[0],
                               RAIN_CENTER[1] + rain_index3[1] * RAIN_SIZE[1]],
                              RAIN_SIZE, RAIN_CENTERTHREE, RAIN_SIZE)
            counterb = (counterb + 1) % (RAIN_DIM[0] * RAIN_DIM[1])
            '''CODE FOR RAIN ENDS HERE, SPRITE SHEET AND THE SORT'''


# create frame
frame = simplegui.create_frame("This Game Has Bugs!", BACKGROUND_SIZE[0], BACKGROUND_SIZE[1])
kbd = Keyboard()
# set draw handler and canvas background using custom HTML color
frame.set_draw_handler(draw)
frame.set_canvas_background("White")
frame.set_keydown_handler(kbd.keyDown)
frame.set_keyup_handler(kbd.keyUp)


# initialize counter for animation and start frame
counter = 0
countera = 2
counterb = 3

frame.start()
music.play()
