#!/usr/bin/python

#-------------------------------------------------------------------72->
# your configuration:
settings = {}
def forward_declaration():
    global settings
    settings = {
        "padlock": unassigned,
        "padenter": unassigned,
        "pad1": unassigned,
        "pad2": down,
        "pad3": unassigned,
        "pad4": left,
        "pad5": reset_center,
        "pad6": right,
        "pad7": unassigned,
        "pad8": up,
        "pad9": unassigned,
        "pad0": hold_click,
        "paddot": release_click,
        "padplus": click,
        "padslash": set_left,
        "padstar": set_middle,
        "padminus": set_right,
    }
#-------------------------------------------------------------------72->
import sys
import math
from PyQt5 import QtWidgets
from pynput import keyboard
from pynput.mouse import Button, Controller
mouse = Controller()
#-------------------------------------------------------------------72->
log = 2
mode = 0
def getmode():
    from pynput.mouse import Button
    return Button.left if mode == 0 else Button.middle if mode == 1 else \
        Button.right if mode == 2 else Button.left
def getboundries():
    global app
    rect = app.primaryScreen().availableGeometry()
    w, h = rect.width(), rect.height()
    return (w, h)

def mousemove():
    debug = False
    if debug:
        print(x, y)
        #return
    global mouse
    try: mouse.position = (x[1], y[1])
    except: print("error") 

def qt():
    global app
    app = QtWidgets.QApplication(sys.argv)

    screen = app.primaryScreen()
    print('Screen: %s' % screen.name())
    size = screen.size()
    print('Size: %d x %d' % (size.width(), size.height()))
    rect = screen.availableGeometry()
    print('Available: %d x %d' % (rect.width(), rect.height()))

    app.exec()

#-------------------------------------------------------------------72->
x, y = (0, 0, 0), (0, 0, 0)
def center():
    global x, y
    w, h = getboundries()
    w -= 1; h -= 1
    x = (0, w//2, w)
    y = (0, h//2, h)

# v stands for vector, p/q to scale, d for direction
def scaler(v, d, p=1, q=2):
    # a: lower bound b: current value  c: upper bound  
    a, b, c = v
    if (a == c): return v
    # total discrete choices
    n = c - a + 1
    # total d.c on left side to discard
    l = b - a + (1 if a != b else 0) # if they are same, we dont want to count
    # t.d.c on right side to discard
    r = c - b + (1 if c != b else 0) # them twice in discreate math
    # discard choices according to the direction
    a = a + max(0, l * d)
    c = c + min(0, r * d)
    if d == -1:
        c = max(a, c)
        a = min(a, c)
    else:
        a = min(a, c)
        c = max(a, c)
    debug = False
    if debug:
        print(f"left:{l}  right:{r}  a:{a}  c:{c}")
    # place b according to the scaling factor and between a, c
    n = c - a + 1
    b = math.floor(a + n * p / q)
    if debug:
        print(f"a:{a}  b:{b}  c:{c}")
    return (a, b, c)

def increase(v, log):
    return scaler(v, 1, 1, log)

def decrease(v, log):
    return scaler(v, -1, 1, log)

#-------------------------------------------------------------------72->
def print_location():
    print(x)

def unassigned():
    debug = True
    if debug:
        print("doom!")

def left_down():
    global x, y, log
    x = decrease(x, log)
    y = increase(y, log)
    mousemove()
    print("left down")

def down():
    global x, y, log
    y = increase(y, log)
    mousemove()
    print("down")

def right_down():
    global x, y, log
    x = increase(x, log)
    y = increase(y, log)
    mousemove()
    print("right down")

def left():
    global x, y, log
    x = decrease(x, log)
    mousemove()
    print("left")

def set_origin():
    global x, y
    w, h = getboundries()
    x = (0, x[1], w)
    y = (0, y[1], h)
    print("set origin")

def right():
    global x, y, log
    x = increase(x, log)
    mousemove()
    print("right")

def left_up():
    global x, y, log
    x = decrease(x, log)
    y = decrease(y, log)
    mousemove()
    print("left up")

def up():
    global x, y, log
    y = decrease(y, log)
    mousemove()
    print("up")

def right_up():
    global x, y, log
    x = increase(x, log)
    y = decrease(y, log)
    mousemove()
    print("right up")

def click():
    mouse.press(getmode())
    mouse.release(getmode())
    #try: pyautogui.click(button=getmode())
    #except pyautogui.FailSafeException: stupidsafe()

def hold_click():
    mouse.press(getmode())
    

def release_click():
    mouse.release(getmode())

def set_left(): 
    global mode
    mode = 0
    print("mode is set to "+getmode())

def set_middle():
    global mode
    mode = 2
    print("mode is set to "+getmode())

def set_right():
    global mode
    mode = 1
    print("mode is set to "+getmode())

def reset_center():
    print("reset to center")
    global x, y, log
    debug = False
    if debug:
        a, b, c = (0, 0, 7)
        x = (a, (c - a) // 2, c)
    else:
        center()
    mousemove()

forward_declaration()
#-------------------------------------------------------------------72->
def key_on_release(key):
    vk = None
    char = None
    try: vk = key.vk
    except: pass
    try: char = key.char
    except: pass
    print(vk, char, sep=" ")

    #settings["padenter"]()
    if char == "1": settings["pad1"]()
    elif char == "2": settings["pad2"]()
    elif char == "3": settings["pad3"]()
    elif char == "4": settings["pad4"]()
    elif vk == 65437: settings["pad5"]()
    elif char == "6": settings["pad6"]()
    elif char == "7":settings["pad7"]()
    elif char == "8":settings["pad8"]()
    elif char == "9":settings["pad9"]()
    elif char == "0":settings["pad0"]()
    elif char == ".":settings["paddot"]()
    #settings["padlock"]()
    elif char == "/":settings["padslash"]()
    elif char == "*":settings["padstar"]()
    elif char == "-":settings["padminus"]()
    elif char == "+":settings["padplus"]()

listener = keyboard.Listener(
    #on_press=key_on_press,
    on_release=key_on_release)
listener.start()

qt()