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
        "padminus": set_left,
        "padstar": set_middle,
        "padminus": set_right,
    }
"""
To findout your keyboard browse /dev/input/ folder and look either by-id/
or by-path/ folders to locate your keyboard. To verify use
$ sudo cat /dev/input/YOUR_KEYBOARD
command to type a key on keyboard and expect to see some random characters
popping up in the shell screen.
"""
keyboards = [
    "/dev/input/by-id/usb-Logitech_USB_Receiver-if02-event-kbd",
    "/dev/input/by-id/usb-COMPANY_2.4G_Device-event-kbd"
]
laptops = [
    "/dev/input/by-path/platform-i8042-serio-0-event-kbd"
]
"""
For arch/linux:
to run: sudo python this.py
to install:
    sudo python -m pip install pyautogui
    sudo pacman -S tk

if xliberrors with authorization, you may need to execute the following command:
$ xhost +
"""
#-------------------------------------------------------------------72->
import pyautogui
import struct
import sys
import math

#-------------------------------------------------------------------72->
log = 2
mode = 0
x, y = (0, 0, 0), (0, 0, 0)
def getmode():
    return "LEFT" if mode == 0 else "RIGHT" if mode == 2 else "MIDDLE" \
        if mode == 1 else "PRIMARY"
def getboundries():
    w, h = pyautogui.size()
    return (w, h)
def mousemove():
    debug = False
    if debug:
        return
    pyautogui.moveTo(x[1], y[1])


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
    pyautogui.click(button=getmode())

def hold_click():
    pyautogui.mouseDown(button=getmode())

def release_click():
    pyautogui.mouseUp(button=getmode())

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
    global x, y, log
    debug = False
    if debug:
        a, b, c = (0, 0, 7)
        x = (a, (c - a) // 2, c)
    else:
        w, h = getboundries()
        x, y = pyautogui.position()
        x = (0, w//2, w)
        y = (0, h//2, h)
    mousemove()
    print("reset to center")

forward_declaration()
#-------------------------------------------------------------------72->
justpressed = {}
def raw(code, value, whatever, keyboard):
    if (code != 4):
        return
    global justpressed
    if not keyboard in justpressed:
        justpressed[keyboard] = []
    if not value in justpressed[keyboard]:
        justpressed[keyboard].append(value)
        return
    justpressed[keyboard].remove(value)

    if keyboard in keyboards:
        keyboard_numlock(value)
    elif keyboard in laptops:
        laptop_numlock(value)
    
    debug = False
    if debug:
        print(f"Keycode: {value}")
        print(x, y)

def laptop_numlock(value):
    if value == 69: settings["padlock"]()
    elif value == 71: settings["pad7"]() 
    elif value == 72: settings["pad8"]() 
    elif value == 73: settings["pad9"]() 
    elif value == 74: settings["padminus"]() 
    elif value == 75: settings["pad4"]() 
    elif value == 76: settings["pad5"]() 
    elif value == 77: settings["pad6"]() 
    elif value == 78: settings["padplus"]() 
    elif value == 79: settings["pad1"]() 
    elif value == 80: settings["pad2"]() 
    elif value == 81: settings["pad3"]() 
    elif value == 82: settings["pad0"]() 
    elif value == 83: settings["paddot"]() 
    elif value == 156: settings["padenter"]()
    elif value == 181: settings["padslash"]()
    elif value == 55: settings["padstar"]()

def keyboard_numlock(value):
    # this is the numlock base keycode it starts from numlock and goes like:
    # numlock / * - + enter 1 2 3 4 5 6 7 8 9 0 .

    b = 458835
    enter= 5
    value -= (b + enter)
    if value == 0: settings["padenter"]()
    elif value == 1: settings["pad1"]()
    elif value == 2: settings["pad2"]()
    elif value == 3: settings["pad3"]()
    elif value == 4: settings["pad4"]()
    elif value == 5: settings["pad5"]()
    elif value == 6: settings["pad6"]()
    elif value == 7: settings["pad7"]()
    elif value == 8: settings["pad8"]()
    elif value == 9: settings["pad9"]()
    elif value == 10: settings["pad0"]()
    elif value == 11: settings["paddot"]()
    elif value == -6: settings["padlock"]()
    elif value == -4: settings["padslash"]()
    elif value == -3: settings["padstar"]()
    elif value == -2: settings["padminus"]()
    elif value == -1: settings["padplus"]()

#-------------------------------------------------------------------72->
FORMAT = 'llHHI'
EVENT_SIZE = struct.calcsize(FORMAT)

def watch(X):
    infile_path = X
    in_file = open(infile_path, "rb")

    event = in_file.read(EVENT_SIZE)

    while event:
        (tv_sec, tv_usec, type, code, value) = struct.unpack(FORMAT, event)

        if type != 0 or code != 0 or value != 0:
            raw(code, value, (tv_sec, tv_usec, type), X)

        event = in_file.read(EVENT_SIZE)

    in_file.close()
import threading
ts=[]
for k in keyboards+laptops:
    print(k)
    t=threading.Thread(target=watch, args=(k,))
    t.start()
    ts.append(t)
for t in ts:
    t.join()
