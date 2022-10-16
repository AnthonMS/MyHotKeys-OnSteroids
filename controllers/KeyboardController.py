## Packages
from os import path
import threading
import json
from datetime import datetime
from pynput.keyboard import Listener

## Local dependencies

class KeyboardController:
    def __init__(self, debug = False, paused = False, base_path = "", config_path = "", logger = None):
        self.THREAD = None
        self.DEBUG = debug
        self.PAUSED = paused
        self.CONFIG_PATH = path.join(base_path, config_path)

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
    
    def debug(self, str):
        if (self.DEBUG):
            print(str)
            self.log(str)

    def log(self, msg):
        if (self.LOGGER is None):
            return "Logger is None"
        
        self.LOGGER.log(msg)
    
    def load_keybinds(self):
        f = open(self.CONFIG_PATH, "r")
        data = json.load(f)
        f.close()

        for bind in data['binds']:
            if (bind['peripheral'] == "keyboard"):
                self.KEYBINDS.append(bind)
                if (bind['event'] == "up"):
                    self.EVENTS_UP.append(bind)
                elif (bind['event'] == "down"):
                    self.EVENTS_DOWN.append(bind)
                elif (bind['event'] == "hold"):
                    self.EVENTS_HOLD.append(bind)
    
    def start_listener(self):
        self.THREAD = threading.Thread(target=self.start_listener_thread, name="KeyboardController", args=[])
        self.THREAD.start()
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
        if (key == self.LAST_KEY and not self.RELEASED):
            self.HOLD = True
        elif (key != self.LAST_KEY and not self.RELEASED):
            self.HOLD = False

        if (self.HOLD):
            return self.key_hold(key)
        else:
            self.RELEASED = False
            return self.key_down(key)


    def on_release(self, key):
        self.HOLD = False
        self.RELEASED = True

        return self.key_up(key)


    def key_down(self, key):
        keep_alive = True
        self.debug(f"{key} down")

        self.addEventToHistory(key, "down")
        self.doActionIfThereIsOne(key, self.EVENTS_DOWN)

        self.LAST_KEY = key
        return keep_alive

    def key_hold(self, key):
        keep_alive = True
        self.debug(f"{key} hold")

        self.addEventToHistory(key, "hold")
        self.doActionIfThereIsOne(key, self.EVENTS_HOLD)

        return keep_alive

    def key_up(self, key):
        keep_alive = True
        self.debug(f"{key} up")
        
        self.addEventToHistory(key, "up")
        self.doActionIfThereIsOne(key, self.EVENTS_UP)
        
        return keep_alive

    def doActionIfThereIsOne(self, key, bindings):
        keep_alive = True
        if (len(bindings) > 0):
            bind = self.key_exist_as_bind(key, bindings)
            if (type(bind) is dict):
                if ("toggle" in bind["action"] or "kill" in bind["action"] or not self.PAUSED):
                    keep_alive = self.ACTION_CTRL.handleAction(bind['action'])
        
        return keep_alive

    def addEventToHistory(self, key, event):
        new_event = {
            "key": key,
            "event": event,
            "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S") # dd/mm/YY H:M:S
        }
        if (new_event['event'] == "hold"):
            new_event['event'] = "hold_start"
        
        try:
            last_event = self.ACTION_CTRL.EVENT_HISTORY[len(self.ACTION_CTRL.EVENT_HISTORY)-1]
            if (new_event['key'] == last_event['key'] and new_event['event'] == last_event['event']):
                pass ## Do not save duplicate events
            else:
                if (last_event['event'] == "hold_start" and new_event['event'] == "up"):
                    new_event['event'] = "hold_stop"

                self.ACTION_CTRL.EVENT_HISTORY.append(new_event)
        except IndexError:
                self.ACTION_CTRL.EVENT_HISTORY.append(new_event)
        

    ## Check if the pressed key exist in the given binds list
    def key_exist_as_bind(self, key, binds):
        for bind in binds:
            try: 
                if (str(key.char) == str(bind['key'])):
                    return bind
            except KeyError: # Raised if ['key'] does not exist in bind
                if (str(key.char) in bind['keys']):
                        return bind
            except AttributeError: # Raised if key.char does not exist
                try:
                    if (str(key) == str(bind['key'])):
                        return bind
                except KeyError: # Raised again if ['key'] does not exist in bind
                        if (str(key) in str(bind['keys'])):
                            return bind

                
        return False
    
## Usage:
# keyboardCtrl = KeyboardController(debug = True, config_path = "keybindings.json", base_path = "D:\Folders\Configs", logger = logger)
# actionCtrl = ActionController(keyboard_ctrl = keyboardCtrl, logger = logger)
# keyboardCtrl.ACTION_CTRL = actionCtrl
# keyboardCtrl.start_listener()