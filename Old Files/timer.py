try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

timer = 0
time = 0

def time_increment():
    global time
    time = time + 1
    get_time(time)
    print(time)

def get_time(time):
    milliseconds = t % 10
    b = t/10
    minutes = int(b / 60)
    seconds = int(b % 60)
    print(milliseconds)
    print(minutes)
    print(seconds)

time_increment()