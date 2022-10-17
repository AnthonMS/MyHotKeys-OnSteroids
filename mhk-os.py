#!/usr/bin/python3.10
## Packages
import sys
from os import path
import json

## Local dependencies
from controllers.Logger import Logger
from controllers.KeyboardController import KeyboardController
from controllers.MouseController import MouseController
from controllers.ActionController import ActionController
# from action_controllers.terraria.ActionController import ActionController

def displayHelp():
    print(f"""
    MHK-OS Help Menu\n
        Welcome to the MyHotKeys-OnSteroids help menu. This is my take on creating a program for easily configuring hotkeys and shortcuts. Where your HotKeys are configured 
        in json and your actions are written in Python. The fact that your actions are written in python, gives you full control to 
        do whatever you want to, when a key or button is pressed down, up, held or any of the other event types available.
        For now mouse only accept up/down events.
        For now the hold actions will be fired constantly until key is released.

        Arguments:
            help                Display this help menu and terminate script
            --base              Base path for both logfiles and config files. 
                                Default is path this script is located in + "/logs" or "/config" accordingly.
            --base-log          Base path for log files only. 
                                Default is path this script is located in + "/logs"
            --log               Filename for log and relative path compared to log base path. 
                                Default is "main.log".
            --base-config       Base path for config files only. 
                                Default is path this script is located in + "/config"
            --config            Name for config file and ActionController to use. So this has to match the name of a json file in the config path AND it has to match the name of a folder for an ActionController
                                Required!
            disable-keyboard    Disable the keyboard listener
            disable-mouse       Disable the mouse listener

    """)

if __name__ == "__main__":
    base_path_log = path.dirname(__file__) + "/logs"
    base_path = path.dirname(__file__)
    config = ""
    ctrl_name = ""
    log = "main.log"
    help = False
    debug_keyboard = False
    debug_mouse = False
    debug_actions = False
    disable_keyboard = False
    disable_mouse = False


    for arg in sys.argv:
        #sys.stdout.write(arg + "\r\n")
        if "help" in arg:
            help = True

        elif "debug" in arg:
            if (arg == "debug"):
                debug_keyboard = True
                debug_mouse = True
                debug_actions = True
            elif (arg == "debug-keyboard"):
                debug_keyboard = True
            elif (arg == "debug-mouse"):
                debug_mouse = True
            elif (arg == "debug-actions"):
                debug_actions = True
        
        elif "disable" in arg:
            if(arg == "disable-keyboard"):
                disable_keyboard = True
            elif (arg == "disable-mouse"):
                disable_mouse = True

        elif "--base=" in arg:
            base_path = arg.replace('--base=', '')

        elif "--base-log=" in arg:
            base_path_log = arg.replace('--base-log=', '')

        elif "--config=" in arg:
            config = arg.replace('--config=', '') + ".json"
            ctrl_name = arg.replace('--config=', '')

        elif "--log=" in arg:
            log = arg.replace('--log=', '')


    if (help):
        displayHelp()
        sys.exit()
    
    if (config == ""):
            config = "default.json"
            ctrl_name = "default"

    ## Start the script
    logger = Logger(base_path = base_path_log, log = log)
    action_logger = Logger(base_path = base_path_log, log = log)
    logger.clear()
    action_logger.clear()
    
    try:
        mod = __import__(f'action_controllers.{ctrl_name}.ActionController', fromlist=['ActionController'])
        ActionControllerDynamic = getattr(mod, 'ActionController')
    except ModuleNotFoundError:
        pass

    keyboardCtrl = KeyboardController(debug = debug_keyboard, config = config, base_path = base_path, logger = logger)
    mouseCtrl = MouseController(debug = debug_mouse, config = config, base_path = base_path, logger = logger)
    actionCtrl = ActionController(debug = debug_actions, keyboard_ctrl = keyboardCtrl, mouse_ctrl = mouseCtrl, logger = action_logger)

    keyboardCtrl.ACTION_CTRL = actionCtrl
    mouseCtrl.ACTION_CTRL = actionCtrl


    
    ## Check if there are kill switches for mouse and keyboard before starting them
    kill_switch = None
    kill_switch_keyboard = None
    kill_switch_mouse = None

    f = open(path.join(base_path, "config", config), "r")
    config_data = json.load(f)
    f.close()
    for bind in config_data['binds']:
        if (bind['action'] == "kill"):
            kill_switch = bind['key']
        elif (bind['action'] == "kill_keyboard"):
            kill_switch_keyboard = bind['key']
        elif (bind['action'] == "kill_mouse"):
            kill_switch_mouse = bind['key']

    if (not disable_keyboard and (not kill_switch is None or not kill_switch_keyboard is None)):
        keyboardCtrl.start_listener()
    else:
        if (not kill_switch is None or not kill_switch_keyboard is None):
            print("Keyboard listener not started because it could not find a kill switch for the script or the keyboard.")
            logger.log("Keyboard listener not started because it could not find a kill switch for the script or the keyboard.")

    if (not disable_mouse and (not kill_switch is None or not kill_switch_mouse is None)):
        mouseCtrl.start_listener()
    else:
        if (not kill_switch is None or not kill_switch_mouse is None):
            print("Mouse listener not started because it could not find a kill switch for the script or the mouse.")
            logger.log("Mouse listener not started because it could not find a kill switch for the script or the mouse.")