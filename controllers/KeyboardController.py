## Packages
from os import path
import sys
import threading
import json
from datetime import datetime
from pynput.keyboard import Listener

## Append this directory to path (If append messed change to: sys.path.insert(0, path.dirname(__file__)))
sys.path.append(path.dirname(__file__))
from shared import *

## Local dependencies

class KeyboardController:
    def __init__(self, debug = False, paused = False, base_path = "", config = "", logger = None):
        self.THREAD = None
        self.DEBUG = debug
        self.PAUSED = paused
        self.CONFIG_PATH = path.join(base_path, "config", config)

        self.LOGGER = logger
        self.LISTENER = None
        self.ACTION_CTRL = None
        self.KEYBINDS = []
        self.EVENTS_UP = []
        self.EVENTS_DOWN = []
        self.EVENTS_HOLD = []
        self.LAST_KEY = None
        self.HOLD = False
        self.RELEASED = True

        # self.load_keybinds()
        load_keybinds(self, "keyboard")
    
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
        log(self, "KeyboardController Started...")

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
        
        if (isinstance(keep_alive, bool)):
            return keep_alive
        if ("kill" in keep_alive):
            ## TODO: Make it kill both mouse and keyboard
            return False
        else:
            return True


    def key_down(self, key):
        keep_alive = True
        # self.debug(f"{key} down")
        debug(self, f"{key} down")

        # self.addEventToHistory(key, "down")
        addEventToHistory(self, key, "down")
        # self.doActionIfThereIsOne(key, self.EVENTS_DOWN)
        keep_alive = doActionIfThereIsOne(self, key, self.EVENTS_DOWN)

        self.LAST_KEY = key
        return keep_alive

    def key_hold(self, key):
        keep_alive = True
        # self.debug(f"{key} hold")
        debug(self, f"{key} hold")

        # self.addEventToHistory(key, "hold")
        addEventToHistory(self, key, "hold")
        # self.doActionIfThereIsOne(key, self.EVENTS_HOLD)
        keep_alive = doActionIfThereIsOne(self, key, self.EVENTS_HOLD)

        return keep_alive

    def key_up(self, key):
        keep_alive = True
        # self.debug(f"{key} up")
        debug(self, f"{key} up")
        
        # self.addEventToHistory(key, "up")
        addEventToHistory(self, key, "up")
        # self.doActionIfThereIsOne(key, self.EVENTS_UP)
        keep_alive = doActionIfThereIsOne(self, key, self.EVENTS_UP)
        
        return keep_alive

    
## Usage:
# keyboardCtrl = KeyboardController(debug = True, config = "keybindings.json", base_path = "D:\Folders\Configs", logger = logger)
# actionCtrl = ActionController(keyboard_ctrl = keyboardCtrl, logger = logger)
# keyboardCtrl.ACTION_CTRL = actionCtrl
# keyboardCtrl.start_listener()