## Packages
import os, sys

## Local dependencies
from controllers.ScriptController import ScriptController

# sys.path.append(os.path.dirname(__file__))
# from shared import *
# from actions.firstAction import firstAction
# import actions


class ActionController(ScriptController):
    def __init__(self, keyboard_ctrl, mouse_ctrl, debug, logger, base_path):
        super().__init__(keyboard_ctrl, mouse_ctrl, debug, logger, base_path)
    
    def __str__(self):
        return f"""
        {super().__str__()}
        """

    def handleAction(self, actionStr):
        keep_alive = super().handleAction(actionStr)
        if (not keep_alive is None): # There was an action that was handled by Parent Script Controller
            return keep_alive