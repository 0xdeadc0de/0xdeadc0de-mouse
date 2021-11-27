from panel import clear, show, hide, draw, getboundries
from mouse import getmode, setmode, mousemove, mousepress, mouserelease, \
    mouseclick
from recipes import log2increase, log2decrease
#-------------------------------------------------------------------72->
# global state
x, y = (0, 0, 0), (0, 0, 0)

#-------------------------------------------------------------------72->
def mouseafter():
    draw(x, y)

#-------------------------------------------------------------------72->
def center():
    global x, y
    w, h = getboundries()
    w -= 1; h -= 1
    x = (0, w//2, w)
    y = (0, h//2, h)

def print_location():
    print(x)

def unassigned():
    debug = True
    if debug:
        print("doom!")

def left_down():
    global x, y, log
    x = log2decrease(x)
    y = log2increase(y)
    mousemove(x, y)
    mouseafter()
    print("left down")

def down():
    global x, y, log
    y = log2increase(y)
    mousemove(x, y)
    mouseafter()
    print("down")

def right_down():
    global x, y, log
    x = log2increase(x)
    y = log2increase(y)
    mousemove(x, y)
    mouseafter()
    print("right down")

def left():
    global x, y, log
    x = log2decrease(x)
    mousemove(x, y)
    mouseafter()
    print("left")

def set_origin():
    global x, y
    w, h = getboundries()
    x = (0, x[1], w)
    y = (0, y[1], h)
    print("set origin")

def right():
    global x, y, log
    x = log2increase(x)
    mousemove(x, y)
    mouseafter()
    print("right")

def left_up():
    global x, y, log
    x = log2decrease(x)
    y = log2decrease(y)
    mousemove(x, y)
    mouseafter()
    print("left up")

def up():
    global x, y, log
    y = log2decrease(y)
    mousemove(x, y)
    mouseafter()
    print("up")

def right_up():
    global x, y, log
    x = log2increase(x)
    y = log2decrease(y)
    mousemove(x, y)
    mouseafter()
    print("right up")

def click():
    hide()
    mouseclick()

def hold_click():
    hide()
    mousepress()
    show()
    
def release_click():
    hide()
    mouserelease()

def set_left(): 
    global mode
    mode = 0
    print("mode is set to "+str(getmode()))

def set_middle():
    global mode
    mode = 2
    print("mode is set to "+str(getmode()))

def set_right():
    global mode
    mode = 1
    print("mode is set to "+str(getmode()))

def reset_center():
    print("reset to center")
    global x, y
    # center x, y
    center()
    
    clear()
    mousemove(x, y)
    mouseafter()