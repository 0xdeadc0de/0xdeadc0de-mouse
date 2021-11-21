#!/usr/bin/python

#-------------------------------------------------------------------72->
# your configuration:
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
def padenter():
    print(x)

def pad1():
    global x, y, log
    x = decrease(x, log)
    y = increase(y, log)
    mousemove()
    print("left down")

def pad2():
    global x, y, log
    y = increase(y, log)
    mousemove()
    print("down")

def pad3():
    global x, y, log
    x = increase(x, log)
    y = increase(y, log)
    mousemove()
    print("right down")

def pad4():
    global x, y, log
    x = decrease(x, log)
    mousemove()
    print("left")

def pad5():
    global x, y
    w, h = getboundries()
    x = (0, x[1], w)
    y = (0, y[1], h)
    print("set origin")

def pad6():
    global x, y, log
    x = increase(x, log)
    mousemove()
    print("right")

def pad7():
    global x, y, log
    x = decrease(x, log)
    y = decrease(y, log)
    mousemove()
    print("left up")

def pad8():
    global x, y, log
    y = decrease(y, log)
    mousemove()
    print("up")

def pad9():
    global x, y, log
    x = increase(x, log)
    y = decrease(y, log)
    mousemove()
    print("right up")

def pad0():
    pyautogui.click(button=getmode())

def padlock(): print("padlock")
def padslash(): 
    global mode
    mode = 0
    print("mode is set to "+getmode())

def padstar():
    global mode
    mode = 2
    print("mode is set to "+getmode())

def padminus():
    global mode
    mode = 1
    print("mode is set to "+getmode())

def padplus():
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
        print(x, y)

def laptop_numlock(value):
    if value == 69: padlock()
    elif value == 71: pad7() 
    elif value == 72: pad8() 
    elif value == 73: pad9() 
    elif value == 74: padminus() 
    elif value == 75: pad4() 
    elif value == 76: pad5() 
    elif value == 77: pad6() 
    elif value == 78: padplus() 
    elif value == 79: pad1() 
    elif value == 80: pad2() 
    elif value == 81: pad3() 
    elif value == 82: pad0() 
    elif value == 156: padenter()
    elif value == 181: padslash()
    elif value == 55: padstar()

def keyboard_numlock(value):
    # this is the numlock base keycode it starts from numlock and goes like:
    # numlock / * - + enter 1 2 3 4 5 6 7 8 9 0 .

    b = 458835
    enter= 5
    if value < b or value > b + enter + 10:
        return

    value -= (b + enter)
    if value == 0: padenter()
    elif value == 1: pad1()
    elif value == 2: pad2()
    elif value == 3: pad3()
    elif value == 4: pad4()
    elif value == 5: pad5()
    elif value == 6: pad6()
    elif value == 7: pad7()
    elif value == 8: pad8()
    elif value == 9: pad9()
    elif value == 10: pad0()
    elif value == -6: padlock()
    elif value == -4: padslash()
    elif value == -3: padstar()
    elif value == -2: padminus()
    elif value == -1: padplus()

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
