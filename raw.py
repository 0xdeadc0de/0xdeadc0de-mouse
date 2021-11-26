#!/usr/bin/python

#-------------------------------------------------------------------72->
# your configuration:
auto_center = True
settings = {}
def forward_declaration():
    global settings
    settings = {
        "padlock": show,
        "padenter": lambda: print("enter"),
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
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)
#-------------------------------------------------------------------72->
import sys
import math
import time
#-------------------------------------------------------------------72->
from pynput import keyboard
from pynput.mouse import Button, Controller
mouse = Controller()
log = 2
mode = 0
def getmode():
    from pynput.mouse import Button
    return Button.left if mode == 0 else Button.middle if mode == 1 else \
        Button.right if mode == 2 else Button.left

def mousemove():
    debug = False
    if debug:
        print(x, y)
        #return
    global mouse
    try: mouse.position = (x[1], y[1])
    except: print("error") 
    global q
    q.progress.emit()
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
    hide()
    mouse.press(getmode())
    mouse.release(getmode())
    if auto_center:
        time.sleep(0.002)
        reset_center()

def hold_click():
    hide()
    mouse.press(getmode())
    q.show()
    

def release_click():
    hide()
    mouse.release(getmode())

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
    global x, y, log
    global q
    q.reset.emit()
    debug = False
    if debug:
        a, b, c = (0, 0, 7)
        x = (a, (c - a) // 2, c)
    else:
        center()
    mousemove()

#-------------------------------------------------------------------72->
import keyboard
def key_on_release(key):

    if key.event_type == "down":
        return

    if key.name == "num lock":
        settings["padlock"]()
        return

    if key.is_keypad == False:
        return
    if enabled == False:
        return
    
    char = key.name
    #settings["padenter"]()
    if char == "1": settings["pad1"]()
    elif char == "2": settings["pad2"]()
    elif char == "3": settings["pad3"]()
    elif char == "4": settings["pad4"]()
    elif char == "5": settings["pad5"]()
    elif char == "6": settings["pad6"]()
    elif char == "7":settings["pad7"]()
    elif char == "8":settings["pad8"]()
    elif char == "9":settings["pad9"]()
    elif char == "0":settings["pad0"]()
    elif char == ".":settings["paddot"]()
    elif char == "/":settings["padslash"]()
    elif char == "*":settings["padstar"]()
    elif char == "-":settings["padminus"]()
    elif char == "+":settings["padplus"]()

#-------------------------------------------------------------------72->

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt

app = QtWidgets.QApplication(sys.argv)

screen = app.primaryScreen()
print('Screen: %s' % screen.name())
size = screen.size()
print('Size: %d x %d' % (size.width(), size.height()))
rect = screen.availableGeometry()
print('Available: %d x %d' % (rect.width(), rect.height()))
w, h = rect.width(), rect.height()
ow, oh = rect.width() - size.width(), rect.height() - size.height()
class Main(QtWidgets.QMainWindow):
    progress = QtCore.pyqtSignal()
    reset = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.progress.connect(self.draw)
        self.reset.connect(self.clear)
#        self.setGeometry(0, 0, w, h)

        self.canvas = QtGui.QPixmap(w, h)
        self.label = QtWidgets.QLabel()
        self.label.setPixmap(self.canvas)
        self.setCentralWidget(self.label)
        self.setWindowOpacity(0.5)

    def draw(self):
        self.clear()
        self.painter = QtGui.QPainter(self.label.pixmap())
        #self.painter.begin()
        self.painter.setPen(Qt.red)
        global x, y
        self.painter.drawLine(x[0]-ow, y[1]+oh, x[2]-ow, y[1]+oh)
        self.painter.drawLine(x[1]-ow, y[0]+oh, x[1]-ow, y[2]+oh)
        self.painter.end()
        self.update()
    
    def clear(self):
        self.canvas = QtGui.QPixmap(w, h)
        self.label.setPixmap(self.canvas)
        self.update()

q = Main()

enabled = False
def hide():
    global q
    global enabled
    enabled = False
    q.hide()
    time.sleep(0.002)

def show():
    global q
    global enabled
    enabled = True
    q.showMaximized()

def getboundries():
    global app
    global w, h
    rect = app.primaryScreen().availableGeometry()
    w, h = rect.width(), rect.height()
    return (w, h)

#-------------------------------------------------------------------72->
import threading
forward_declaration()
def key_thread():
    keyboard.hook(key_on_release)
    #keyboard.wait()
threading.Thread(target=key_thread).run()
app.exec_()