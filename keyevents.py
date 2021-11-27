from static import print_verbose
#-------------------------------------------------------------------72->

def released(key, bindings):

    print_verbose(key.to_json(), "released")

    # we only interested in when the key is released
    if key.event_type == "down":
        return

    name = key.name

    # bare num lock = right shift + numlock key
    if name == "bare num lock": bindings["shiftpadlock"]()

    # this check ensures the following keys are pressed from numpad because
    # it could be mistaken with other parts of keyboard like numbers and such
    if key.is_keypad == False:
        return
    
    # we check if panel is enabled after this line because the keys listed below
    # are keys that can send a char or such a key that perform an action like
    # enter key. in order to prevent these happening, we require user to have
    # his/her panel had opened
    if enabled == False:
        return

    #settings["padenter"]()
    if name == "1": bindings["pad1"]()
    elif name == "2": bindings["pad2"]()
    elif name == "3": bindings["pad3"]()
    elif name == "4": bindings["pad4"]()
    elif name == "5": bindings["pad5"]()
    elif name == "6": bindings["pad6"]()
    elif name == "7":bindings["pad7"]()
    elif name == "8":bindings["pad8"]()
    elif name == "9":bindings["pad9"]()
    elif name == "0":bindings["pad0"]()
    elif name == ".":bindings["paddot"]()
    elif name == "÷":bindings["padslash"]()
    elif name == "×":bindings["padstar"]()
    elif name == "-":bindings["padminus"]()
    elif name == "+":bindings["padplus"]()