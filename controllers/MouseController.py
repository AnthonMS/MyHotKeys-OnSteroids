## Packages
from os import path
import threading
import json
from datetime import datetime
from pynput.mouse import Listener

## Local dependencies

class MouseController:
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
        self.CURRENT_BUTTON = None
        self.LAST_BUTTON = None
        self.PRESSED = False

        self.load_keybinds()
    
    def __str__(self):
        return f"""
        MouseController:
            Debug: {self.DEBUG}
            Config Path: {self.CONFIG_PATH}
            Paused: {self.PAUSED}
            Current Button: {self.CURRENT_BUTTON}
            Last Button: {self.LAST_BUTTON}
            Pressed: {self.PRESSED}
            Keybinds: {self.KEYBINDS}
            Action Ctrl: {"{0}".format("None" if self.ACTION_CTRL is None else "Set")}
        """
    
    def debug(self, str):
        if (self.DEBUG):
            print(str)

    def log(self, msg):
        if (self.LOGGER is None):
            return "Logger is None"
        
        self.LOGGER.log(msg)
    
    def load_keybinds(self):
        f = open(self.CONFIG_PATH, "r")
        data = json.load(f)
        f.close()

        for bind in data['binds']:
            if (bind['peripheral'] == "mouse"):
                self.KEYBINDS.append(bind)
                if (bind['event'] == "up"):
                    self.EVENTS_UP.append(bind)
                elif (bind['event'] == "down"):
                    self.EVENTS_DOWN.append(bind)
                elif (bind['event'] == "hold"):
                    self.EVENTS_HOLD.append(bind)

    def start_listener(self):
        self.THREAD = threading.Thread(target=self.start_listener_thread, name="MouseController", args=[])
        self.THREAD.start()
        self.log("MouseController Started...")
    
    def start_listener_thread(self):
        if (self.ACTION_CTRL == None):
            print("Action handler is None. Can not start mouse listener.")
            if (self.THREAD.is_alive()):
                self.THREAD.stop()
            return False
        
        with Listener(
                on_move=self.on_move,
                on_click=self.on_click,
                on_scroll=self.on_scroll) as listener:
            self.LISTENER = listener
            listener.join()
        
        return False  # Stopping mouse thread

    def on_click(self, x, y, button, pressed):
        if (pressed):
            return self.button_down(button, x, y)
        else:
            return self.button_up(button, x, y)

    def on_move(self, x, y):
        if (False):
            print(f"X: {x} Y: {y}")
    
    def on_scroll(self, x, y, dx, dy):
        if (False):
            print(f"Scroll: {x}/{y}")
    
    
    def button_down(self, button, x, y):
        self.CURRENT_BUTTON = button
        self.PRESSED = True
        keep_alive = True
        self.debug(f"{button} - down - x: {x} y: {y}")

        self.addEventToHistory(button, "down")
        self.doActionIfThereIsOne(button, self.EVENTS_DOWN)

        self.LAST_BUTTON = button
        return keep_alive

    def button_up(self, button, x, y):
        self.PRESSED = False
        keep_alive = True
        self.debug(f"{button} - up - x: {x} y: {y}")

        self.addEventToHistory(button, "up")
        self.doActionIfThereIsOne(button, self.EVENTS_UP)
        
        return keep_alive


    def button_hold(self, button, x, y):
        keep_alive = True
        self.debug(f"{button} - hold - x: {x} y: {y}")

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
# mouseCtrl = MouseController(debug = True, config_path = "mousebindings.json", base_path = "D:\Folders\Configs", logger = logger)
# actionCtrl = ActionController(mouse_ctrl = mouseCtrl, logger = logger)
# mouseCtrl.ACTION_CTRL = actionCtrl
# mouseCtrl.start_listener()