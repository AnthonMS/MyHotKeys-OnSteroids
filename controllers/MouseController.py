## Packages
import sys
from os import path
import threading
import json
from datetime import datetime
from pynput.mouse import Listener

## Local dependencies
from controllers.InputController import InputController

class MouseController(InputController):
    def __init__(self, debug = False, paused = False, base_path = "", config = "", logger = None):
        super().__init__(debug, paused, base_path, config, logger, "mouse")
        self.LAST_BUTTON = None
        self.CURRENT_BUTTON = None
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
        keep_alive = True
        if (pressed):
            keep_alive = self.button_down(button, x, y)
        else:
            keep_alive = self.button_up(button, x, y)

        if (keep_alive is None):
            return True # Keep alive
        if (isinstance(keep_alive, bool)):
            return keep_alive

        if (not keep_alive or "kill" in keep_alive):
            ## TODO: Make it kill both mouse and keyboard
            return False
        else:
            return True
            

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

## Usage:
# mouseCtrl = MouseController(debug = True, config_path = "mousebindings.json", base_path = "D:\Folders\Configs", logger = logger)
# actionCtrl = ActionController(mouse_ctrl = mouseCtrl, logger = logger)
# mouseCtrl.ACTION_CTRL = actionCtrl
# mouseCtrl.start_listener()