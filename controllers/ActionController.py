## Packages
import os, sys

## Local dependencies
from controllers.ScriptController import ScriptController

# sys.path.append(os.path.dirname(__file__))
# from shared import *
from actions.firstAction import firstAction


dir_path = os.path.dirname(os.path.abspath(__file__))
files_in_dir = [f[:-3] for f in os.listdir(dir_path)
                if f.endswith('.py') and f != '__init__.py']
print("Dirname:", dir_path)
print("Files in dir:", files_in_dir)

class ActionController(ScriptController):
    def __init__(self, keyboard_ctrl, mouse_ctrl, debug, logger):
        super().__init__(keyboard_ctrl, mouse_ctrl, debug, logger)
    
    def __str__(self):
        return f"""
        {super().__str__()}
        Custom ActionController:
            Nothing
        """

    def handleAction(self, action):
        keep_alive = super().handleAction(action)
        if (not keep_alive is None): # There was an action that was handled by Parent Script Controller
            return keep_alive
        
        firstAction(self)
        ## Write custom Action Handler code and functions here
        self.debug(f"Handle Custom Action from this awesome new action controller: {action}")