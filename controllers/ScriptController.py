## Packages
import os, sys
from pynput import mouse, keyboard

## Local dependencies


class ScriptController:
    def __init__(self, keyboard_ctrl = None, mouse_ctrl = None, debug = True, logger = None, base_path = ""):
        self.DEBUG = debug
        self.BASE_PATH = base_path
        self.LOGGER = logger
        self.KEYBOARD_CTRL = keyboard_ctrl
        self.MOUSE_CTRL = mouse_ctrl
        self.EVENT_HISTORY = []

        self.ACTIONS = []
        self.importActions()
    
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

        if (action in self.ACTIONS):
            return eval(action + "(self)")


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

            
    def importActions(self):
        all_binds = [*self.KEYBOARD_CTRL.KEYBINDS, *self.MOUSE_CTRL.KEYBINDS]
        all_actions = []
        for bind in all_binds:
            all_actions.append(bind['action'])

        dir_path = os.path.join(self.BASE_PATH, "actions")
        # dir_path = os.path.dirname(os.path.abspath(__file__))
        files_in_dir = [f[:-3] for f in os.listdir(dir_path)
                        if f.endswith('.py') and f != '__init__.py']
        for f in files_in_dir:
            mod = __import__('actions.'+f, fromlist=[f])
            to_import = [getattr(mod, x) for x in dir(mod)]
            ### if isinstance(getattr(mod, x), type)]  # if you need classes only

            for i in to_import:
                try:
                    if i.__name__ in all_actions and not i.__name__ in self.ACTIONS:
                        setattr(sys.modules[__name__], i.__name__, i)
                        self.ACTIONS.append(i.__name__)
                except AttributeError:
                    pass