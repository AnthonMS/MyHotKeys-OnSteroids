## Packages

## Local dependencies
from controllers.ScriptController import ScriptController


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
        
        ## Write custom Action Handler code and functions here
        self.debug(f"Handle Custom Action: {action}")