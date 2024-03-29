## Packages
import sys
from os import path
import threading
import json
from datetime import datetime
from pynput.mouse import Listener

## Local dependencies
## Append this directory to path (If append messed change to: sys.path.insert(0, path.dirname(__file__)))
# sys.path.append(path.dirname(__file__))
# from shared import *

class InputController:
    def __init__(self, debug = False, paused = False, base_path = "", config = "", logger = None, input_type = None):
        self.INPUT_TYPE = input_type ## string value = "keyboard" or "mouse"
        self.THREAD = None
        self.DEBUG = debug
        self.PAUSED = paused
        self.CONFIG_PATH = path.join(base_path, "config", config)

        self.LOGGER = logger
        self.LISTENER = None
        self.ACTION_CTRL = None
        self.KEYBINDS = []
        self.EVENTS_UP = [] # UP_BINDS
        self.EVENTS_DOWN = [] # DOWN_BINDS
        self.EVENTS_HOLD = [] # HOLD_BINDS
        self.BINDS_HOLD_START = []
        self.BINDS_HOLD_STOP = []
    
    def __str__(self):
        return f"""
        InputController:
            Debug: {self.DEBUG}
            Config Path: {self.CONFIG_PATH}
            Paused: {self.PAUSED}
            Keybinds: {self.KEYBINDS}
            Listener: {"{0}".format("None" if self.LISTENER is None else "Started")}
            Action Ctrl: {"{0}".format("None" if self.ACTION_CTRL is None else "Set")}
        """

    def load_keybinds(self):
        f = open(self.CONFIG_PATH, "r")
        data = json.load(f)
        f.close()

        for bind in data['binds']:
            if (bind['peripheral'] == self.INPUT_TYPE):
                self.KEYBINDS.append(bind)
                if (bind['event'] == "up"):
                    self.EVENTS_UP.append(bind)
                elif (bind['event'] == "down"):
                    self.EVENTS_DOWN.append(bind)
                elif (bind['event'] == "hold"):
                    self.EVENTS_HOLD.append(bind)
                elif (bind['event'] == "hold_start"):
                    self.BINDS_HOLD_START.append(bind)
                elif (bind['event'] == "hold_stop"):
                    self.BINDS_HOLD_STOP.append(bind)

    def debug(self, str):
        if (self.DEBUG):
            print(str)
            self.log(str)

    def log(self, msg):
        if (self.LOGGER is None):
            print("Logger is None")
        
        self.LOGGER.log(msg)


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
        
        last_event = self.ACTION_CTRL.getLastEvent()
        if (last_event):
            if (new_event['key'] == last_event['key'] and new_event['event'] == last_event['event']):
                pass ## Do not save duplicate events
            else:
                if (last_event['event'] == "hold_start" and new_event['event'] == "up"):
                    new_event['event'] = "hold_stop"
                self.ACTION_CTRL.EVENT_HISTORY.append(new_event)
        else:
            self.ACTION_CTRL.EVENT_HISTORY.append(new_event)
        
        return new_event

                
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