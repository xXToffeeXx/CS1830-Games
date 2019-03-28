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
musicDecider = 0

inversion = False

### GAME CONSTANTS ###
CANVAS_WIDTH = 700
CANVAS_HEIGHT = 1250
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

#extrasAmbience = simplegui.load_sound\
            #("https://storage.googleapis.com/cs1830/The%20Show%20Must%20Be%20Go.mp3")
#extrasAmbience.set_volume(gameVolume)

#optionsAmbience = simplegui.load_sound \
    #("https://commondatastorage.googleapis.com/cs1830/Angels%20We%20Have%20Heard%20(piano).mp3")
#optionsAmbience.set_volume(gameVolume)

#music = simplegui.load_sound("")

if rainOrNo <= 1: #SUMMER
    pass#music = simplegui.load_sound\
        #("https://commondatastorage.googleapis.com/cs1830/Beachfront%20Celebration%20(1).mp3")
    #music.set_volume(gameVolume)

else: #RAINFOREST
    pass#music = simplegui.load_sound\
        #("https://commondatastorage.googleapis.com/cs1830/462774__lg__20180616-tropical-rain-thailand-02.wav")
    #music.set_volume(gameVolume)

#buttonSoundSplash = simplegui.load_sound\
    #("https://commondatastorage.googleapis.com/cs1830/439746__inspectorj__soprano-recorder-staccato-c.wav")
#buttonSoundSplash.set_volume(gameVolume)

#buttonOnPress = simplegui.load_sound\
    #("https://commondatastorage.googleapis.com/cs1830/243020__plasterbrain__game-start.ogg")
#buttonOnPress.set_volume(gameVolume)

#musicLibrary = [music, optionsAmbience, extrasAmbience]

#TODO:
#1: Make the credits screen actually display something
#2: Make all of this code below a lot neater by placing it into lists n shit
class Keyboard:
    def __init__(self, p1, p2):
        self.down = False
        self.up = False
        self.enter = False
        self.p1_right = False
        self.p1_left = False
        self.p2_right = False
        self.p2_left = False
        self.p1 = p1
        self.p2 = p2
        self.p1_last = counter
        self.p2_last = counter
        self.cooldown = 40

    if gamePlay:
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

    else:
        def keyDown(self, key):
            if key == simplegui.KEY_MAP['down'] or key == simplegui.KEY_MAP['s']:
                self.down = True

            if key == simplegui.KEY_MAP['up'] or key == simplegui.KEY_MAP['w']:
                self.up = True

            if key == simplegui.KEY_MAP['space'] or key == simplegui.KEY_MAP['e']:
                self.enter = True

        def keyUp(self, key):
            global buttonState, easterEggCounter, rainOrNo, musicDecider, \
                gameVolume, keybLeft, keybRight, wasdLeft, wasdRight, inversion

            # KEYMAP FOR MAIN MENU
            if mainMenu:
                if key == simplegui.KEY_MAP['down'] or key == simplegui.KEY_MAP['s']:
                    self.down = False
                    buttonState += 1
                    if buttonState > 4:
                        buttonState = 0
                    print(buttonState)
                    easterEggCounter += 1
                    print(easterEggCounter)
                    # buttonSoundSplash.pause()
                    # buttonSoundSplash.rewind()
                    # buttonSoundSplash.play()
                    time.sleep(0.1)

                if key == simplegui.KEY_MAP['up'] or key == simplegui.KEY_MAP['w']:
                    self.up = False
                    buttonState -= 1
                    if buttonState < 0:
                        buttonState = 4
                    print(buttonState)
                    # buttonSoundSplash.pause()
                    # buttonSoundSplash.rewind()
                    # buttonSoundSplash.play()
                    easterEggCounter = 0
                    time.sleep(0.1)

                if key == simplegui.KEY_MAP['space'] or key == simplegui.KEY_MAP['e']:
                    if buttonState == 0:
                        print(gameButtonhandler())
                        if rainOrNo <= 1:
                            pass  # musicLibrary[0].pause()
                        # buttonOnPress.pause()
                        # buttonOnPress.rewind()
                        # buttonOnPress.play()
                        # easterEgg()
                    if buttonState == 1:
                        print(multigameButtonhandler())
                        if rainOrNo <= 1:
                            pass  # musicLibrary[0].pause()
                        # buttonOnPress.pause()
                        # buttonOnPress.rewind()
                        # buttonOnPress.play()
                        # easterEgg()
                    if buttonState == 2:
                        print(optionsHandler())
                        if rainOrNo <= 1:
                            pass  # musicLibrary[0].pause()
                        # buttonOnPress.pause()
                        # buttonOnPress.rewind()
                        # buttonOnPress.play()
                        # easterEgg()
                    if buttonState == 3:
                        print(extrasHandler())
                        if rainOrNo <= 1:
                            pass  # musicLibrary[0].pause()
                        # buttonOnPress.pause()
                        # buttonOnPress.rewind()
                        # buttonOnPress.play()
                        # easterEgg()
                    if buttonState == MENU_OPTIONS:
                        if rainOrNo <= 1:
                            pass  # musicLibrary[0].pause()

                        # buttonOnPress.pause()
                        # buttonOnPress.rewind()
                        # buttonOnPress.play()
                        sys.exit()
            # KEYMAP FOR OPTIONS
            elif options:
                if key == simplegui.KEY_MAP['down'] or key == simplegui.KEY_MAP['s']:
                    self.down = False
                    buttonState += 1
                    if buttonState > 2:
                        buttonState = 0
                    print(buttonState)
                    # buttonSoundSplash.pause()
                    # buttonSoundSplash.rewind()
                    # buttonSoundSplash.play()
                    time.sleep(0.1)

                if key == simplegui.KEY_MAP['up'] or key == simplegui.KEY_MAP['w']:
                    self.up = False
                    buttonState -= 1
                    if buttonState < 0:
                        buttonState = 2
                    print(buttonState)
                    # buttonSoundSplash.pause()
                    # buttonSoundSplash.rewind()
                    # buttonSoundSplash.play()
                    time.sleep(0.1)

                if key == simplegui.KEY_MAP['space'] or key == simplegui.KEY_MAP['e']:
                    if buttonState == 0:
                        print("Volume")
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
                        # buttonOnPress.pause()
                        # buttonOnPress.rewind()
                        # buttonOnPress.play()
                    if buttonState == 2:
                        if rainOrNo <= 1:
                            # musicLibrary[1].pause()
                            # musicLibrary[1].rewind()
                            pass
                        print(mainMenuHandlerFromOptions())
                        # buttonOnPress.pause()
                        # buttonOnPress.rewind()
                        # buttonOnPress.play()

                if key == simplegui.KEY_MAP[wasdRight] or key == simplegui.KEY_MAP[keybRight]:

                    if buttonState == 0:
                        gameVolume = volumeHandler(1, gameVolume)
                        print("Game volume is now: ", (int)(gameVolume * 10))
                        # buttonSoundSplash.pause()
                        # buttonSoundSplash.rewind()
                        # buttonSoundSplash.play()
                    # musicLibrary[0].set_volume(gameVolume), #musicLibrary[1].set_volume(gameVolume), #musicLibrary[2].set_volume(gameVolume),
                    # buttonSoundSplash.set_volume(gameVolume ), buttonOnPress.set_volume(gameVolume )

                if key == simplegui.KEY_MAP[wasdLeft] or key == simplegui.KEY_MAP[keybLeft]:
                    if buttonState == 0:
                        gameVolume = volumeHandler(2, gameVolume)
                        print("Game volume is now: ", (int)(gameVolume * 10))
                        # buttonSoundSplash.pause()
                        # buttonSoundSplash.rewind()
                        # buttonSoundSplash.play()

                    if gameVolume >= 0.0:
                        # musicLibrary[0].set_volume(gameVolume), #musicLibrary[1].set_volume(gameVolume), #musicLibrary[2].set_volume(gameVolume),
                        # buttonSoundSplash.set_volume(gameVolume), buttonOnPress.set_volume(gameVolume)
                        pass
                    elif gameVolume < 0.0:
                        # musicLibrary[0].set_volume(0.0), #musicLibrary[1].set_volume(0.0), #musicLibrary[2].set_volume(
                        # 0.0),
                        # buttonSoundSplash.set_volume(0.0), buttonOnPress.set_volume(0.0)
                        gameVolume = 0.0

            elif extras:
                if key == simplegui.KEY_MAP['down'] or key == simplegui.KEY_MAP['s']:
                    self.down = False
                    buttonState += 1
                    if buttonState > 2:
                        buttonState = 0
                    print(buttonState)
                    # buttonSoundSplash.pause()
                    # buttonSoundSplash.rewind()
                    # buttonSoundSplash.play()
                    time.sleep(0.1)

                if key == simplegui.KEY_MAP['up'] or key == simplegui.KEY_MAP['w']:
                    self.up = False
                    buttonState -= 1
                    if buttonState < 0:
                        buttonState = 2
                    print(buttonState)
                    # buttonSoundSplash.pause()
                    # buttonSoundSplash.rewind()
                    # buttonSoundSplash.play()
                    time.sleep(0.1)

                if key == simplegui.KEY_MAP['space'] or key == simplegui.KEY_MAP['e']:
                    if buttonState == 0:
                        # musicLibrary[0].pause()
                        # musicLibrary[0].rewind()
                        # musicLibrary[1].pause()
                        # musicLibrary[1].rewind()
                        # musicLibrary[2].pause()
                        # musicLibrary[2].rewind()
                        # if musicDecider >= len(#musicLibrary)-1:
                        # musicDecider = 0
                        # else:
                        # musicDecider += 1
                        # LIST INDEX OUT OF RANGE
                        # musicLibrary[musicDecider].play()
                        print("Song number ", musicDecider, " is being played.")

                    if buttonState == 1:
                        print("Credits")
                        if rainOrNo == 2:
                            pass
                            # musicLibrary[0].play()
                        else:
                            pass
                            # musicLibrary[0].pause()
                            # musicLibrary[1].pause()
                            # musicLibrary[2].play()

                    if buttonState == 2:
                        if rainOrNo <= 1:
                            pass  # musicLibrary[2].pause()
                            # musicLibrary[2].rewind()

                        print(mainMenuHandlerFromExtras())
                    # buttonOnPress.pause()
                    # buttonOnPress.rewind()
                    # buttonOnPress.play()

    def update(self):
        if self.p1_right:
            self.p1.vel.add(Vector(1, 0))
        if self.p1_left:
            self.p1.vel.add(Vector(-1, 0))
        if self.p2_right:
            self.p2.vel.add(Vector(1, 0))
        if self.p2_left:
            self.p2.vel.add(Vector(-1, 0))

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

    '''
def easterEgg():
    if easterEggCounter == 100:
        #musicLibrary[0].pause()
        print("You found an Easter Egg!")
        easterEggSong = simplegui.load_sound("https://commondatastorage.googleapis.com/cs1830/Spazzmatica%20Polka.mp3")
        easterEggSong.set_volume(gameVolume)
        easterEggSong.play()
    else:
        pass
'''
'''
LOADING IN ALL ASSETS STORED ON GOOGLE CLOUD SERVICES
AT SOME POINT I SHALL ORGANISE THIS IN TO LISTS
BUT TODAY IS NOT THAT DAY
'''
genricbackground_image = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/GameBackground.png")
homemenubackground_image = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/GameBackgroundMenu.png")
genericbackground_raining = simplegui.load_image\
    ("https://commondatastorage.googleapis.com/cs1830/GameBackgroundRaining.png")
homebackground_raining = simplegui.load_image\
    ("https://commondatastorage.googleapis.com/cs1830/GameBackgroundMenuRaining.png")
gameBackground_image = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/PlainBackground.png")

#IMPORTING HOME MENU BUTTONS
startgamebutton_image = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/StartGame.png")
optionsbutton_image = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/Options.png")
twoplayerbutton_image = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/Multiplayer.png")
extrasbutton_image = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/Extras.png")
exitbutton_image = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/Exit.png")

#IMPORTING CONTROLS
arrowKeys_image = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/ArrowKeys.png")

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

#IMPORTING ITEMS FOR THE EXTRAS SCREEN
credits_image = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/Credits.png")
cyclemusic_image = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/CycleMusic.png")

credits_image_selected = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/CreditsSelected.png")
cyclemusic_image_selected = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/CycleMusicSelected.png")

#IMPORTING TITLES
optionstitle_image = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/OptionsTITLE.png")
extrastitle_image = simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/ExtrasTITLE.png")

loadingGIF = [simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/LoadingOne.png"),
              simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/LoadingTwo.png"),
              simplegui.load_image("https://commondatastorage.googleapis.com/cs1830/LoadingThree.png")]

'''
ASSIGNING ALL CONSTANTS FOR VALUES USED IN CANVAS DRAWING
'''

BACKGROUND_SIZE = [CANVAS_WIDTH, CANVAS_HEIGHT]
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

CONTROLS_CENTER = [455, 1100]

TITLE_CENTER = [350, 230]

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


class Player(Sprite):
    # Specific player CONSTANTS
    LIVES = 3
    velocity = 0.75
    startpos = Vector(CANVAS_WIDTH / 2, CANVAS_HEIGHT - 700)

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

        # print(self.pos.y)

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
        # power_up = random.choice(['BULLETS'] * 5 + ['LIFE'] * 5 + ['NONE'] * 90)
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
                    # self.eList.remove(enemy)  # remove or lower health?
                    enemy.die()
                    if bullet in BULLETS: BULLETS.remove(bullet)
                    # increase score
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

            # print('Player One lives: ' + str(playerOne.LIVES))
            # print('Player Two lives: ' + str(playerTwo.LIVES))

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
        # canvas.draw_image(simplegui.load_image('https://i.imgur.com/JH6xdz6.png'), (7.5, 7.5), (15, 15),
        #                  (CANVAS_WIDTH - 175, 13), (15, 15))

        canvas.draw_text("P2 Lives:", (CANVAS_WIDTH - (CANVAS_WIDTH / 5), 18), 20, 'White', 'sans-serif')
        canvas.draw_text(str(playerTwo.LIVES), (CANVAS_WIDTH - (CANVAS_WIDTH / 9.2), 18), 20, 'Red', 'sans-serif')
        # canvas.draw_image(simplegui.load_image('https://i.imgur.com/JH6xdz6.png'), (7.5, 7.5), (15, 15),
        #                  (CANVAS_WIDTH - 35, 13), (15, 15))

        # canvas.draw_text("Time: " + str(ti), ((CANVAS_WIDTH - 400), 18), 20, 'White', 'sans-serif')

        # if KILLED == (E_ROWS * E_COLS):
        if KILLED == (E_ROWS * E_COLS):
            playerOne.stop()
            playerTwo.stop()

            game_over(canvas, 'win')


playerOne = Player('https://i.imgur.com/XEhhit6.png')
playerTwo = Player('https://i.imgur.com/JSEeuYR.png')
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




'''METHOD USED TO CONTROL VOLUME SLIDER'''
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
- USE THESE TO CONNECT THE BUTTONS IN THE MENU TO THE GAMEPLAY ELEMENT
'''

def gameButtonhandler():
    global mainMenu
    global gamePlay

    print("Game open button pressed.")
    mainMenu = False
    gamePlay = True

    #musicLibrary[0].pause(), #musicLibrary[0].rewind()
    #musicLibrary[1].pause(), #musicLibrary[1].rewind()
    #musicLibrary[2].pause(), #musicLibrary[2].rewind()


    #musicLibrary[0].set_volume(gameVolume), #musicLibrary[1].set_volume(gameVolume), #musicLibrary[2].set_volume(gameVolume),
    #buttonSoundSplash.set_volume(gameVolume), buttonOnPress.set_volume(gameVolume)

def multigameButtonhandler():
    global mainMenu
    global multiGamePlay


    print("Game open for multiplayer button pressed.")
    mainMenu = False
    multiGamePlay = True

    #musicLibrary[0].set_volume(gameVolume), #musicLibrary[1].set_volume(gameVolume), #musicLibrary[2].set_volume(gameVolume),
    #buttonSoundSplash.set_volume(gameVolume), buttonOnPress.set_volume(gameVolume)

def optionsHandler():
    global mainMenu, buttonState, rainOrNo, options

    print("Options screen opened.")
    mainMenu = False
    options = True
    # RESET BUTTON STATE
    buttonState = 0
    if rainOrNo == 2:
        pass
    elif rainOrNo <= 1:
        pass
        #musicLibrary[0].pause()
        #musicLibrary[0].rewind()
        #musicLibrary[1].play()

    #musicLibrary[0].set_volume(gameVolume), #musicLibrary[1].set_volume(gameVolume), #musicLibrary[2].set_volume(gameVolume),
    #buttonSoundSplash.set_volume(gameVolume), buttonOnPress.set_volume(gameVolume)

def extrasHandler():
    global mainMenu
    global extras
    global buttonState
    global rainOrNo

    #TODO write the code for opening game and switching to a screen for options
    print("Extras screen opened.")
    mainMenu = False
    extras = True

    # RESET BUTTON STATE
    buttonState = 0
    if rainOrNo == 2:
        pass
    elif rainOrNo <= 1:
        pass
        #musicLibrary[0].pause()
        #musicLibrary[0].rewind()
        #musicLibrary[2].play()

    #musicLibrary[0].set_volume(gameVolume), #musicLibrary[1].set_volume(gameVolume), #musicLibrary[2].set_volume(gameVolume),
    #buttonSoundSplash.set_volume(gameVolume), buttonOnPress.set_volume(gameVolume)

def mainMenuHandlerFromOptions():
    global mainMenu ,buttonState ,rainOrNo\
    ,options


    print("Main Menu opened")

    options = False
    mainMenu = True

    buttonState = 0
    if rainOrNo == 2:
        pass
    elif rainOrNo <= 1:
        pass
        #musicLibrary[0].play()

    #musicLibrary[0].set_volume(gameVolume), #musicLibrary[1].set_volume(gameVolume), #musicLibrary[2].set_volume(gameVolume),
    #buttonSoundSplash.set_volume(gameVolume), buttonOnPress.set_volume(gameVolume)

def mainMenuHandlerFromExtras():
    global mainMenu, buttonState, rainOrNo \
        ,extras

    print("Main Menu opened")

    extras = False
    mainMenu = True

    buttonState = 0
    if rainOrNo == 2:
        pass
    elif rainOrNo <= 1:
        pass
        #musicLibrary[0].play()

    #musicLibrary[0].set_volume(gameVolume), #musicLibrary[1].set_volume(gameVolume), #musicLibrary[2].set_volume(gameVolume),
    #buttonSoundSplash.set_volume(gameVolume), buttonOnPress.set_volume(gameVolume)

#code for drawing onto canvas
def draw(canvas):
    global counter, countera, counterb, mainMenu, assetLoading
    #TODO LOADING SCREEN DON'T FORGET

    if mainMenu:
        #DRAW IN THE BUTTONS and the MENU SCREEN
        if rainOrNo <= 1:
            canvas.draw_image(homemenubackground_image, BACKGROUND_CENTER, BACKGROUND_SIZE, BACKGROUND_CENTER, BACKGROUND_SIZE)
            canvas.draw_image(arrowKeys_image, GENBUTTON_CENTER, BUTTON_WIDTH, CONTROLS_CENTER, BUTTON_WIDTH)
        elif rainOrNo == 2:
            canvas.draw_image(homebackground_raining, BACKGROUND_CENTER, BACKGROUND_SIZE, BACKGROUND_CENTER, BACKGROUND_SIZE)
            canvas.draw_image(arrowKeys_image, GENBUTTON_CENTER, BUTTON_WIDTH, CONTROLS_CENTER, BUTTON_WIDTH)
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
        canvas.draw_image(optionstitle_image, GENBUTTON_CENTER, BUTTON_WIDTH, TITLE_CENTER,
                          BUTTON_WIDTH)

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

        canvas.draw_image(extrastitle_image, GENBUTTON_CENTER, BUTTON_WIDTH, TITLE_CENTER,
                          BUTTON_WIDTH)

        if buttonState == 0:
            canvas.draw_image(cyclemusic_image_selected, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONONE_CENTER,
                              BUTTON_WIDTH)
            canvas.draw_image(credits_image, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONTWO_CENTER, BUTTON_WIDTH)
            canvas.draw_image(BacktoMenu_image, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONTHREE_CENTER, BUTTON_WIDTH)

        if buttonState == 1:
            canvas.draw_image(cyclemusic_image, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONONE_CENTER, BUTTON_WIDTH)
            canvas.draw_image(credits_image_selected, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONTWO_CENTER,
                              BUTTON_WIDTH)
            canvas.draw_image(BacktoMenu_image, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONTHREE_CENTER, BUTTON_WIDTH)

        if buttonState == 2:
            canvas.draw_image(cyclemusic_image, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONONE_CENTER, BUTTON_WIDTH)
            canvas.draw_image(credits_image, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONTWO_CENTER, BUTTON_WIDTH)
            canvas.draw_image(BacktoMenu_image_selected, GENBUTTON_CENTER, BUTTON_WIDTH, BUTTONTHREE_CENTER,
                              BUTTON_WIDTH)
    elif gamePlay:
        canvas.draw_image(gameBackground_image, BACKGROUND_CENTER, BACKGROUND_SIZE, BACKGROUND_CENTER,
                              BACKGROUND_SIZE)
        counter += 1
        inter.update()
        explo.draw(canvas)
        kbd.update()
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

        # if not ENEMIES:
        #   game_over(canvas, 'lose')

        if gameover:
            game_over(canvas, 'lose')


    elif multiGamePlay:
        canvas.draw_image(gameBackground_image, BACKGROUND_CENTER, BACKGROUND_SIZE, BACKGROUND_CENTER,
                          BACKGROUND_SIZE)
        #TODO: DRAW IN GAME PLAY ASSETS


make_walls()
make_enemies()
incount = 0

def set_up():
    global LEVEL
    LEVEL = LEVEL + 1
    reset()
    make_enemies()
    make_walls()

def reset():
    global E_ROWS
    global E_COLS
    global ENEMY_SPEED
    global incount
    playerOne.LIVES = 3
    playerTwo.LIVES = 3
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


# create frame
frame = simplegui.create_frame("This Game Has Bugs!", BACKGROUND_SIZE[0], BACKGROUND_SIZE[1])
kbd = Keyboard(playerOne, playerTwo)
# set draw handler and canvas background using custom HTML color
frame.set_draw_handler(draw)
frame.set_canvas_background("Black")
frame.set_keydown_handler(kbd.keyDown)
frame.set_keyup_handler(kbd.keyUp)


set_up()
make_walls()

# initialize counter for animation and start frame
counter = 0
countera = 2
counterb = 3

frame.start()
#musicLibrary[0].play()