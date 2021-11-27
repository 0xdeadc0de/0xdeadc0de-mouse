#!/usr/bin/python

#-------------------------------------------------------------------72->
# allow user to terminate program by ctrl+c or +d
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

#-------------------------------------------------------------------72->

#-------------------------------------------------------------------72->

def key_thread():
    from settings import get_bindings
    bindings = get_bindings()
    from keyevents import released
    import keyboard
    keyboard.hook(lambda key: released(key, bindings))

if __name__ == "__main__":
    # execute keyboard listener in separate thread
    import threading
    threading.Thread(target=key_thread).run()
    # execute GUI event listener
    from panel import app
    app.exec_()