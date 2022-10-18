## Packages
import sys
from os import path
import threading
import json
from datetime import datetime
from pynput.keyboard import Listener

## Local dependencies
from controllers.InputController import InputController

class KeyboardController(InputController):
    def __init__(self, debug = False, paused = False, base_path = "", config = "", logger = None):
        super().__init__(debug, paused, base_path, config, logger, "keyboard")
        self.INPUT_TYPE = "keyboard"
        self.LAST_KEY = None
        self.HOLD = False
        self.RELEASED = True

        self.load_keybinds()
    
    def __str__(self):
        # print('{0} at {1}'.format('Pressed' if pressed else 'Released',x, y)))
        return f"""
        KeyboardController:
            Debug: {self.DEBUG}
            Config Path: {self.CONFIG_PATH}
            Paused: {self.PAUSED}
            Last Key: {self.LAST_KEY}
            Hold: {self.HOLD}
            Released: {self.RELEASED}
            Keybinds: {self.KEYBINDS}
            Action Ctrl: {"{0}".format("None" if self.ACTION_CTRL is None else "Set")}
        """
    
    def start_listener(self):
        self.THREAD = threading.Thread(target=self.start_listener_thread, name="KeyboardController", args=[])
        self.THREAD.start()
        # self.log("KeyboardController Started...")
        self.log("KeyboardController Started...")

    def start_listener_thread(self):
        if (self.ACTION_CTRL == None):
            print("Action ctrl is None. Can not start keyboard listener.")
            if (self.THREAD.is_alive()):
                self.THREAD.stop()
            return False

        with Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:
            self.LISTENER = listener
            listener.join()
        
        return False # Stopping keyboard thread


    def on_press(self, key):
        keep_alive = True

        if (key == self.LAST_KEY and not self.RELEASED):
            self.HOLD = True
        elif (key != self.LAST_KEY and not self.RELEASED):
            self.HOLD = False

        if (self.HOLD):
            keep_alive = self.key_hold(key)
        else:
            self.RELEASED = False
            keep_alive = self.key_down(key)

        if (keep_alive is None):
            return True # Keep alive
        if (isinstance(keep_alive, bool)):
            return keep_alive

        if (not keep_alive or "kill" in keep_alive):
            ## TODO: Make it kill both mouse and keyboard
            return False
        else:
            return True

    def on_release(self, key):
        keep_alive = True
        self.HOLD = False
        self.RELEASED = True

        keep_alive = self.key_up(key)

        if (keep_alive is None):
            return True # Keep alive
        if (isinstance(keep_alive, bool)):
            return keep_alive 

        if ("kill" in keep_alive):
            ## TODO: Kill both mouse and keyboard
            return False 
        else:
            return True


    def key_down(self, key):
        keep_alive = True
        # self.debug(f"{key} down")
        self.debug(f"{key} down")

        # self.addEventToHistory(key, "down")
        self.addEventToHistory(key, "down")
        # self.doActionIfThereIsOne(key, self.EVENTS_DOWN)
        keep_alive = self.doActionIfThereIsOne(key, self.EVENTS_DOWN)

        self.LAST_KEY = key
        return keep_alive

    def key_hold(self, key):
        keep_alive = True
        # self.debug(f"{key} hold")
        self.debug(f"{key} hold")

        # self.addEventToHistory(key, "hold")
        self.addEventToHistory(key, "hold")
        # self.doActionIfThereIsOne(key, self.EVENTS_HOLD)
        keep_alive = self.doActionIfThereIsOne(key, self.EVENTS_HOLD)

        return keep_alive

    def key_up(self, key):
        keep_alive = True
        # self.debug(f"{key} up")
        self.debug(f"{key} up")
        
        # self.addEventToHistory(key, "up")
        self.addEventToHistory(key, "up")
        # self.doActionIfThereIsOne(key, self.EVENTS_UP)
        keep_alive = self.doActionIfThereIsOne(key, self.EVENTS_UP)
        
        return keep_alive

    
## Usage:
# keyboardCtrl = KeyboardController(debug = True, config = "keybindings.json", base_path = "D:\Folders\Configs", logger = logger)
# actionCtrl = ActionController(keyboard_ctrl = keyboardCtrl, logger = logger)
# keyboardCtrl.ACTION_CTRL = actionCtrl
# keyboardCtrl.start_listener()