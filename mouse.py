from pynput.mouse import Button, Controller
#-------------------------------------------------------------------72->

mouse = Controller()
mode = 0
def setmode(m):
    global mode
    mode = m
def getmode():
    from pynput.mouse import Button
    return Button.left if mode == 0 else Button.middle if mode == 1 else \
        Button.right if mode == 2 else Button.left

def mousepress():
    mouse.press(getmode())

def mouserelease():
    mouse.release(getmode())

def mouseclick():
    mouse.click(getmode())

def mousemove(x, y):
    debug = False
    if debug:
        print(x, y)
        #return
    global mouse
    try: mouse.position = (x[1], y[1])
    except: print("mouse move error") 