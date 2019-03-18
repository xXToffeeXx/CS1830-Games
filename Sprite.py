# Walking animation
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

import math


# The class for the sprites
class Sprite:
    def __init__(self, pos, duration=1, scale=1):
        self.image = simplegui.load_image('https://imgur.com/glDuLYi.png')
        self.pos = pos
        self.scale = scale
        self.size = (208, 26)
        self.dims = (8, 1)
        self.window = (26, 26)
        self.center = (self.window[0] / 2, self.window[1] / 2)
        self.offset = (0, 0)
        self.current = [0, 0]
        self.duration = duration
        self.previousFrame = 0

    def nextFrame(self):
        self.current[0] = (self.current[0] + 1) % self.dims[0]
        if self.current[0] == 0:
            self.current[1] = (self.current[1] + 1) % self.dims[1]

    def previousFrame(self):
        pass

    def frameJump(self, time):
        frame = time / self.duration
        if (frame - self.previousFrame) >= 1:
            print("Time =", time, "\t", frame)
            for i in range(round(frame - self.previousFrame)):
                self.nextFrame()
                self.previousFrame = frame

    def draw(self, canvas):
        x = self.current[0] * self.window[0]
        y = self.current[1] * self.window[1]
        canvas.draw_image(self.image,
                          (self.center[0] + self.offset[0] + x, self.center[1] + self.offset[1] + y),
                          self.window, self.pos, (self.window[0] * self.scale, self.window[1] * self.scale))


# Function to create the frame
def frame():
    frame = simplegui.create_frame("Walking", 500, 400)
    frame.set_canvas_background('#0000ff')
    frame.set_draw_handler(loop)
    return frame


# Constants
CANVAS_SIZE = [500, 400]
CANVAS_CENTER = [CANVAS_SIZE[0] / 2, CANVAS_SIZE[1] / 2]

# Global variables

# This is the clock we will use, it measures iterations of the game loop
time = 0

# The sprites
# The first argument is a pair with the coordinates of the sprite center on the canvas
# The second argument is the duration of each frame in time units
# The third argument is the scale of the sprite on the canvas
sprite1 = Sprite([CANVAS_CENTER[0], CANVAS_CENTER[1] / 2], 1.5, 0.6)
sprite2 = Sprite([CANVAS_CENTER[0], CANVAS_CENTER[1] * 3 / 2], 0.75, 0.6)

# Stores the sprites
sprites = [sprite1, sprite2]


# Game loop
def loop(canvas):
    # Update the time
    global time
    time = time + 1
    print("Time =", time)

    # Draw the sprites on the canvas
    for sprite in sprites:
        sprite.frameJump(time)
        sprite.draw(canvas)


###################################
#      End of the play zone       #
###################################


# Start the animation
frame().start()

