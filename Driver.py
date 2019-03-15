try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

import math
import time
import random
import sys


#TODO Refactor my shit ass spaghetti code
'''
OKAY SO BASICALLY:
1. BOOLEANS TO DETERMINE WHICH SCREEN THE GAME SHOULD BE SHOWING
2. ASSIGN BOOLEANS IN METHODS CALLED BY PRESS OF SPACE OR e
3. THIS CHANGES WHAT IS DRAWN IN DRAW()
'''

'''
Booleans determine which buttons are selected
'''
mainMenu = True
gamePlay = False
multiGamePlay = False
options = False
extras = False

gameVolume = 0.8

inversion = False

'''
Below determines key mappings
'''
wasdRight = "d"
wasdLeft = "a"

keybRight = "right"
keybLeft = "left"

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

extrasAmbience = simplegui.load_sound\
            ("https://storage.googleapis.com/cs1830/The%20Show%20Must%20Be%20Go.mp3")
extrasAmbience.set_volume(gameVolume)

ambientMusic = simplegui.load_sound \
    ("https://commondatastorage.googleapis.com/cs1830/Angels%20We%20Have%20Heard%20(piano).mp3")
ambientMusic.set_volume(gameVolume)

music = simplegui.load_sound("")

if rainOrNo <= 1: #SUMMER
    music = simplegui.load_sound\
        ("https://commondatastorage.googleapis.com/cs1830/Beachfront%20Celebration%20(1).mp3")
    music.set_volume(gameVolume)

else: #RAINFOREST
    music = simplegui.load_sound\
        ("https://commondatastorage.googleapis.com/cs1830/462774__lg__20180616-tropical-rain-thailand-02.wav")
    music.set_volume(gameVolume)

buttonSoundSplash = simplegui.load_sound\
    ("https://commondatastorage.googleapis.com/cs1830/439746__inspectorj__soprano-recorder-staccato-c.wav")
buttonSoundSplash.set_volume(gameVolume)

buttonOnPress = simplegui.load_sound\
    ("https://commondatastorage.googleapis.com/cs1830/243020__plasterbrain__game-start.ogg")
buttonOnPress.set_volume(gameVolume)


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
        global buttonState,easterEggCounter,rainOrNo,\
        gameVolume, normalisedVolume, keybLeft, keybRight, wasdLeft, wasdRight, inversion

        #KEYMAP FOR MAIN MENU
        if mainMenu:
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
                    if rainOrNo <=1:
                        music.pause()
                    buttonOnPress.play()
                    easterEgg()
                if buttonState == 1:
                    print(multigameButtonhandler())
                    if rainOrNo <= 1:
                        music.pause()
                    buttonOnPress.play()
                    easterEgg()
                if buttonState == 2:
                    print(optionsHandler())
                    if rainOrNo <= 1:
                        music.pause()
                    buttonOnPress.play()
                    easterEgg()
                if buttonState == 3:
                    print(extrasHandler())
                    if rainOrNo <= 1:
                        music.pause()
                    buttonOnPress.play()
                    easterEgg()
                if buttonState == MENU_OPTIONS:
                    if rainOrNo <= 1:
                        music.pause()
                    buttonOnPress.play()
                    sys.exit()
        #KEYMAP FOR OPTIONS
        elif options:
            if key == simplegui.KEY_MAP['down'] or key == simplegui.KEY_MAP['s']:
                self.down = False
                buttonState+=1
                if buttonState>2:
                    buttonState = 0
                print(buttonState)
                buttonSoundSplash.play()
                time.sleep(0.1)

            if key == simplegui.KEY_MAP['up']or key == simplegui.KEY_MAP['w']:
                self.up = False
                buttonState-=1
                if buttonState<0:
                    buttonState = 2
                print(buttonState)
                buttonSoundSplash.play()
                time.sleep(0.1)

            if key == simplegui.KEY_MAP['space'] or key == simplegui.KEY_MAP['e']:
                if buttonState == 0:
                    print("Volume")
                    buttonOnPress.play()
                if buttonState == 1:
                    print("Invert Horizontal")
                    tempwasd = wasdLeft
                    tempkeyb = keybLeft

                    wasdLeft = wasdRight
                    keybLeft = keybRight

                    wasdRight = tempwasd
                    keybRight = tempkeyb

                    if inversion:
                        inversion = False
                    else:
                        inversion = True
                    print("Left movements now dictated by: ", wasdLeft, " and ", keybLeft)

                    buttonOnPress.play()
                if buttonState == 2:
                    if rainOrNo <= 1:
                        ambientMusic.pause()
                        ambientMusic.rewind()
                    print(mainMenuHandlerFromOptions())
                    buttonOnPress.play()

            if key == simplegui.KEY_MAP[wasdRight] or key == simplegui.KEY_MAP[keybRight]:

                if buttonState==0:
                    gameVolume = volumeHandler(1, gameVolume)
                    print("Game volume is now: ", (int)(gameVolume * 10))

                music.set_volume(gameVolume), ambientMusic.set_volume(gameVolume), extrasAmbience.set_volume(gameVolume),
                buttonSoundSplash.set_volume(gameVolume ), buttonOnPress.set_volume(gameVolume )

            if key == simplegui.KEY_MAP[wasdLeft] or key == simplegui.KEY_MAP[keybLeft]:
                if buttonState==0:
                    gameVolume = volumeHandler(2, gameVolume)
                    print("Game volume is now: ", (int)(gameVolume * 10))

                music.set_volume(gameVolume), ambientMusic.set_volume(gameVolume), extrasAmbience.set_volume(gameVolume),
                buttonSoundSplash.set_volume(gameVolume), buttonOnPress.set_volume(gameVolume)


def easterEgg():
    if easterEggCounter == 100:
        music.pause()
        print("You found an Easter Egg!")
        easterEggSong = simplegui.load_sound("https://commondatastorage.googleapis.com/cs1830/Spazzmatica%20Polka.mp3")
        easterEggSong.set_volume(gameVolume)
        easterEggSong.play()
    else:
        pass

'''
LOADING IN ALL ASSETS STORED ON GOOGLE CLOUD SERVICES
'''
genricbackground_image = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/GameBackground.png")
homemenubackground_image = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/GameBackgroundMenu.png")
genericbackground_raining = simplegui.load_image\
    ("https://commondatastorage.googleapis.com/cs1830/GameBackgroundRaining.png")
homebackground_raining = simplegui.load_image\
    ("https://commondatastorage.googleapis.com/cs1830/GameBackgroundMenuRaining.png")

#IMPORTING HOME MENU BUTTONS
startgamebutton_image = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/StartGame.png")
optionsbutton_image = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/Options.png")
twoplayerbutton_image = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/Multiplayer.png")
extrasbutton_image = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/Extras.png")
exitbutton_image = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/Exit.png")

#IMPORTING SELECTED HOME MENU BUTTONS
startgamebutton_image_selected = simplegui.load_image\
    ("https://commondatastorage.googleapis.com/cs1830/StartGameSelected.png")
optionsbutton_image_selected = simplegui.load_image\
    ("https://commondatastorage.googleapis.com/cs1830/OptionsSelected.png")
twoplayerbutton_image_selected = simplegui.load_image\
    ("https://commondatastorage.googleapis.com/cs1830/MultiplayerSelected.png")
extrasbutton_image_selected = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/ExtrasSelected.png")
exitbutton_image_selected = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/ExitSelected.png")

#IMPORTING THE RAIN SPRITESHEETS
rain = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/ezgif.com-gif-maker.png")
rain2 = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/ezgif.com-gif-maker.png")
rain3 = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/ezgif.com-gif-maker.png")

shimmerGIF = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/shimmerGIF.png")

#IMPORTING OPTIONS SCREEN BUTTONS
soundFX_image = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/SoundFX.png")
BacktoMenu_image = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/BackToMenu.png")
invertlr_image = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/InvertHorizontal.png")

#IMPORTING SELECTED BUTTONS FOR OPTIONS SCREEN
soundFX_image_selected = simplegui.load_image\
    ("https://commondatastorage.googleapis.com/cs1830/SoundFXSelected.png")
BacktoMenu_image_selected = simplegui.load_image\
    ("https://commondatastorage.googleapis.com/cs1830/BackToMenuSelected.png")
invertlr_image_selected = simplegui.load_image\
    ("https://commondatastorage.googleapis.com/cs1830/InvertHorizontalSelected.png")

onImage = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/Numbers/ON.png")
offImage = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/Numbers/OFF.png")

numbersList = [(simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/Numbers/0.png")),
               (simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/Numbers/1.png")),
               (simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/Numbers/2.png")),
               (simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/Numbers/3.png")),
               (simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/Numbers/4.png")),
               (simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/Numbers/5.png")),
               (simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/Numbers/6.png")),
               (simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/Numbers/7.png")),
               (simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/Numbers/8.png")),
               (simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/Numbers/9.png")),
               (simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/Numbers/10.png"))
               ]


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

ARROW_WIDTH = [150,150]
ARROW_LEFT_CENTER = [505, 430]
ARROW_RIGHT_CENTER = [625, 430]
GENARROW_CENTER = [75, 75]

NUMBER_CENTER = [600, 430]
ONOFF_CENTER = [600, 530]


def volumeHandler(decider, gameVolume):
    temp = gameVolume
    if decider == 1:
        temp = gameVolume+0.1
        if temp > 1.0:
            gameVolume = 1.0
        else:
            gameVolume+=0.1
    elif decider == 2:
        gameVolume -= 0.1
        if temp < 0.0:
            gameVolume = 0.0

    return gameVolume

'''
BUTTONHANDLERS ACTIVATED WHEN SPACEBAR OR e IS PRESSED ON GAMESTATE
'''

def gameButtonhandler():
    global mainMenu
    global gamePlay 

    print("Game open button pressed.")
    mainMenu = False
    gamePlay = True

    music.set_volume(gameVolume), ambientMusic.set_volume(gameVolume), extrasAmbience.set_volume(gameVolume),
    buttonSoundSplash.set_volume(gameVolume), buttonOnPress.set_volume(gameVolume)

def multigameButtonhandler():
    global mainMenu
    global multiGamePlay


    print("Game open for multiplayer button pressed.")
    mainMenu = False
    multiGamePlay = True

    music.set_volume(gameVolume), ambientMusic.set_volume(gameVolume), extrasAmbience.set_volume(gameVolume),
    buttonSoundSplash.set_volume(gameVolume), buttonOnPress.set_volume(gameVolume)

def optionsHandler():
    global mainMenu, buttonState, rainOrNo \
    ,options, ambientMusic

    print("Options screen opened.")
    mainMenu = False
    options = True
    # RESET BUTTON STATE
    buttonState = 0
    if rainOrNo == 2:
        pass
    elif rainOrNo <= 1:
        music.pause()
        music.rewind()
        ambientMusic.play()

    music.set_volume(gameVolume), ambientMusic.set_volume(gameVolume), extrasAmbience.set_volume(gameVolume),
    buttonSoundSplash.set_volume(gameVolume), buttonOnPress.set_volume(gameVolume)

def extrasHandler():
    global mainMenu
    global extras
    global buttonState
    global rainOrNo
    global extrasAmbience

    #TODO write the code for opening game and switching to a screen for options
    print("Extras screen opened.")
    mainMenu = False
    extras = True

    # RESET BUTTON STATE
    buttonState = 0
    if rainOrNo == 2:
        pass
    elif rainOrNo <= 1:
        music.pause()
        music.rewind()
        extrasAmbience.play()

    music.set_volume(gameVolume), ambientMusic.set_volume(gameVolume), extrasAmbience.set_volume(gameVolume),
    buttonSoundSplash.set_volume(gameVolume), buttonOnPress.set_volume(gameVolume)

def mainMenuHandlerFromOptions():
    global mainMenu ,buttonState ,rainOrNo\
    ,options ,ambientMusic


    print("Main Menu opened")

    options = False
    mainMenu = True

    buttonState = 0
    if rainOrNo == 2:
        pass
    elif rainOrNo <= 1:
        music.play()

    music.set_volume(gameVolume), ambientMusic.set_volume(gameVolume), extrasAmbience.set_volume(gameVolume),
    buttonSoundSplash.set_volume(gameVolume), buttonOnPress.set_volume(gameVolume)

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

        '''MAIN MENU DRAWING--------------------------------------------------------------------------------------------------'''
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
        '''MAIN MENU DRAWING DONE---------------------------------------------------------------------------------------------'''


    elif options:
        global numbersList
        #DRAW IN THE BUTTONS and the MENU SCREEN
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
                              [RAIN_CENTER [0] + rain_index3[0] * RAIN_SIZE[0],
                               RAIN_CENTER [1] + rain_index3[1] * RAIN_SIZE[1]],
                               RAIN_SIZE, RAIN_CENTERTHREE, RAIN_SIZE)
            counterb = (counterb + 1) % (RAIN_DIM[0] * RAIN_DIM[1])
            '''CODE FOR RAIN ENDS HERE, SPRITE SHEET AND THE SORT'''

            '''DRAWING IN THE OPTIONS MENU ----------------------------'''
        if buttonState == 0:

            canvas.draw_image(soundFX_image_selected, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONONE_CENTER,
                              BUTTON_WIDTH)
            n = (int)(gameVolume * 10)
            canvas.draw_image(numbersList[n], GENBUTTON_CENTER, BUTTON_WIDTH, NUMBER_CENTER,
                                  BUTTON_WIDTH)

            canvas.draw_image(invertlr_image, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONTWO_CENTER, BUTTON_WIDTH)
            canvas.draw_image(BacktoMenu_image, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONTHREE_CENTER, BUTTON_WIDTH)

        if buttonState == 1:
            canvas.draw_image(soundFX_image, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONONE_CENTER, BUTTON_WIDTH)
            canvas.draw_image(invertlr_image_selected, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONTWO_CENTER,
                              BUTTON_WIDTH)
            if inversion:
                canvas.draw_image(onImage, GENBUTTON_CENTER, BUTTON_WIDTH, ONOFF_CENTER,
                                  BUTTON_WIDTH)

            else:
                canvas.draw_image(offImage, GENBUTTON_CENTER, BUTTON_WIDTH, ONOFF_CENTER,
                                  BUTTON_WIDTH)

            canvas.draw_image(BacktoMenu_image, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONTHREE_CENTER, BUTTON_WIDTH)

        if buttonState == 2:
            canvas.draw_image(soundFX_image, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONONE_CENTER, BUTTON_WIDTH)
            canvas.draw_image(invertlr_image, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONTWO_CENTER, BUTTON_WIDTH)
            canvas.draw_image(BacktoMenu_image_selected, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONTHREE_CENTER,
                              BUTTON_WIDTH)

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