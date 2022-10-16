#!/usr/bin/python3.10
## Packages
import sys
from os import path
import json

## Local dependencies
from controllers.Logger import Logger
from controllers.KeyboardController import KeyboardController
from controllers.MouseController import MouseController
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
    base_path_config = path.dirname(__file__) + "/config"
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
            base_path_log = arg.replace('--base=', '')
            base_path_config = arg.replace('--base=', '')

        elif "--base-log=" in arg:
            base_path_log = arg.replace('--base-log=', '')

        elif "--base-config=" in arg:
            base_path_config = arg.replace('--base-config=', '')

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
    

    mod = __import__(f'action_controllers.{ctrl_name}.ActionController', fromlist=['ActionController'])
    ActionController = getattr(mod, 'ActionController')

    keyboardCtrl = KeyboardController(debug = debug_keyboard, config_path = config, base_path = base_path_config, logger = logger)
    mouseCtrl = MouseController(debug = debug_mouse, config_path = config, base_path = base_path_config, logger = logger)
    actionCtrl = ActionController(debug = debug_actions, keyboard_ctrl = keyboardCtrl, mouse_ctrl = mouseCtrl, logger = action_logger)

    keyboardCtrl.ACTION_CTRL = actionCtrl
    mouseCtrl.ACTION_CTRL = actionCtrl


    
    ## Check if there are kill switches for mouse and keyboard before starting them
    kill_switch = None
    kill_switch_keyboard = None
    kill_switch_mouse = None

    f = open(path.join(base_path_config, config), "r")
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



## TODO:
## - Make bind config key "hold_time". This will make it so hold will only fire when it has been held for given amount of time.
## - Research making the script a command in windows registry
## - Research creating windows tray icons that when clicked will show buttons for "pause"/"start" and "kill" for mouse, keyboard and both
## - Create a package installer helper function in ScriptController that will install the needed packages automatically. ActionController should come with a requirements.txt file.
## - Make the shared functions between keyboard and mouse controllers into a seperate script so there isn't any duplicated code that need to be changed twice.
## - Update main script to find ActionController based on path in string
## - Make hold_start and hold_stop instead of only hold action
## - New command arguments 
##      - "print-keys": Enable printing keys in console for easy access to names for action configuration
##      - "print-buttons": Enable printing buttons in console for easy access to names for action configuration

## - Add new config key "event_type" which will take in the values "once"/"toggle"/"until_release"/"sequence"
##      This key will tell the script if an action should be fired once, until button/key is released or until the button/key is pressed again.
##      The until_release will obviously only be for "hold_start" actions
##      "sequence" is for when it is an array of keys instead of a single key. This means the action will happen if the order of keys pressed are the same is in the list.
##          This means the ActionController (ScriptController should be updated to hold a history of keys pressed for easy access. Maybe an events array holding objects of the eventtype, timestamp, and key. Only save hold_start & hold_stop events.)



## DONE:
## - Create Simple Keyboard Listener that prints out different key presses and events and closes on Key.esc
## - Create ActionController that will take in KeyboardController as parameter
## - Create actionHandler function that will take in controller and action string as parameters and call the correct action function
## - Create action that will handle terminating keyboard listener
## - Create action that will toggle the keyboard listener on/off
## - Update KeyboardController to be a class instead
## - Update KeyboardController to read in keyboard bindings from a json config file
## - Clean up KeyboardController so there isn't so much duplicated code and checks.
## - Create Logger and make it as a dynamic class that can do the very basic of checking if the path and file exist, if not then create it and then log message with datetime timestamps
## - Create MouseController and make it like the KeyboardController since the same library can create mouse listener as well. 
##      It shall only handle button down and up events for now. Update later with hold/dragging? events
## - Make Keyboard and MouseController threaded. So both of them can run at the same time.
## - Create action that will kill MouseController
## - Create action that will toggle MouseController
## - Create action that will kill both Mouse and KeyboardController
## - Create action that will toggle both Mouse and KeyboardController
## - Refactor Controller names to reflect classnames
## - Update ActionController to new logic:
##      ActionController should be a parent ActionController (ScriptController) which holds the actions for pausing/resuming/killing the listeners/script entirely.
##      A new ActionController class should be created that is derived from the ScriptController. 
##      So it has all the parent functions for handling the script and then custom ActionControllers can be written to handle custom actions like Terraria macros, RuneScape macros and all that fun stuff ;)
## - Create different command arguments 
##      - "help": Display a help menu that explain how the script works and what it expects in arguments
##      - "debug": Enable debugging all controllers
##      - "debug-keyboard": Enable debugging keyboard
##      - "debug-mouse": Enable debugging mouse
##      - "disable-keyboard": Disable the keyboard listener if only mouse is desired
##      - "disable-mouse": Disable the mouse listener if only keyboard is desired
## - Helper functions and better descriptions for the arguments and parameters in the different classes
## - Prevent user from starting script if no kill switch has been given
## - Update actionHandler to take in only action as a parameter, instead of controller and action
## - Update keybindings to be either a string or an array of strings. This will make it so multiple keys can do the same action. And in the long run make it so you can write actions like commands, but anywhere!?
## - Make config argument to take in only name of config and then import ActionController based on this config key as well as json.
## - Refactor main script name to something like mhkos.py = "MyHotKeys-OnSteroids"

## Usage:
# .\AutoHotKey-OS\mhk-os.py [ --config=terraria | default=default ]
# Args:
#   - "--base=": Will make this the base path for both logfiles and config files. Default is path this script is located in.
#   - "--base-log=": Will make this the base path for logfiles only. Default is path this script is located in + "/logs"
#   - "--log=": Filename for log and relative path compared to base path for log files. Default is "main.log".
#   - "--base-config=": Will make this the base path for config files only. Default is path this script is located in + "/config"
#   - "--config=": Name for config file and ActionController to use. So this has to match the name of a json file in the config path AND it has to match the name of a folder for an ActionController