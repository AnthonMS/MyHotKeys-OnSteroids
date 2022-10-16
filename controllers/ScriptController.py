## Packages
from pynput import mouse, keyboard

## Local dependencies


class ScriptController:
    def __init__(self, keyboard_ctrl = None, mouse_ctrl = None, debug = True, logger = None):
        self.DEBUG = debug
        self.LOGGER = logger
        self.KEYBOARD_CTRL = keyboard_ctrl
        self.MOUSE_CTRL = mouse_ctrl
        self.EVENT_HISTORY = []
    
    def __str__(self):
        return f"""
        ScriptController:
            Debug: {self.DEBUG}
            Keyboard Ctrl: {"None" if self.KEYBOARD_CTRL is None else "Set"}
            Mouse Ctrl: {"None" if self.LOGGER is None else "Set"}
            Logger: {"None" if self.MOUSE_CTRL is None else "Set"}
        """

    def debug(self, str):
        if (self.DEBUG):
            print(str)
            self.log(str)

    def log(self, msg):
        if (self.LOGGER is None):
            return "Logger is None"
        
        self.LOGGER.log(msg)

    
    def getLastEvent(self):
        try:
            return self.EVENT_HISTORY[len(self.EVENT_HISTORY)-1]
        except IndexError:
            return False
    
    def getLastEventKey(self):
        try:
            return str(self.getLastEvent()['key'].char)
        except AttributeError: # Raised if key.char does not exist
            return str(self.getLastEvent()['key'])
        except:
            return False



    def handleAction(self, action):
        if ("kill" in action):
            return self.kill(action)
        elif ("toggle" in action):
            return self.toggle(action)
        elif (action == "test"):
            self.test()
    

    def test(self):
        self.debug("We are testing this button...")


    ## Toggle the keyboard listener on/off
    def toggle(self, action):
        if (action == "toggle"):
            self.KEYBOARD_CTRL.PAUSED = not self.KEYBOARD_CTRL.PAUSED
            self.MOUSE_CTRL.PAUSED = not self.MOUSE_CTRL.PAUSED
            self.debug(f"{'Keyboard Listener Paused' if self.KEYBOARD_CTRL.PAUSED else 'Keyboard Listener Unpaused'}")
            self.debug(f"{'Mouse Listener Paused' if self.MOUSE_CTRL.PAUSED else 'Mouse Listener Unpaused'}")
        elif (action == "toggle_mouse"):
            self.MOUSE_CTRL.PAUSED = not self.MOUSE_CTRL.PAUSED
            self.debug(f"{'Mouse Listener Paused' if self.MOUSE_CTRL.PAUSED else 'Mouse Listener Unpaused'}")
        elif (action == "toggle_keyboard"):
            self.KEYBOARD_CTRL.PAUSED = not self.KEYBOARD_CTRL.PAUSED
            self.debug(f"{'Keyboard Listener Paused' if self.KEYBOARD_CTRL.PAUSED else 'Keyboard Listener Unpaused'}")
        
        return "keep_alive"


    ## Stop the script completely
    def kill(self, action):
        if (action == "kill"):
            # Stop Keyboard listener and kill thread
            if (not self.KEYBOARD_CTRL.LISTENER is None):
                keyboard.Listener.stop(self.KEYBOARD_CTRL.LISTENER)
                self.debug(f"Keyboard Listener Terminated")

            # Stop Mouse listener and kill thread
            if (not self.MOUSE_CTRL.LISTENER is None):
                mouse.Listener.stop(self.MOUSE_CTRL.LISTENER)
                self.debug(f"Mouse Listener Terminated")
            
            ## threads are closed by stopping listeners, but return False to make sure
            return "kill"
        elif (action == "kill_mouse"):
            if (not self.MOUSE_CTRL.LISTENER is None):
                mouse.Listener.stop(self.MOUSE_CTRL.LISTENER)
                self.debug(f"Mouse Listener Terminated")
            
            return "kill"
        elif (action == "kill_keyboard"):
            if (not self.KEYBOARD_CTRL.LISTENER is None):
                keyboard.Listener.stop(self.KEYBOARD_CTRL.LISTENER)
                self.debug(f"Keyboard Listener Terminated")
            
            return "kill"