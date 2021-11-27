from panel import *
from actions import *

#-------------------------------------------------------------------72->
# your configuration:
def get_bindings():
    return {
    "shiftpadlock": toggle,
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