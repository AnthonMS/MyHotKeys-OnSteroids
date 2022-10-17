# MyHotKeys-OnSteroids
**Welcome to mhk-os**<br>

This first iteration was created in 1 day. So keep that in mind when reading through the code and trying to use it. I know it still lacks a lot of stuff, but I think I will be working on this going forward since I see a massive benefit over this compared to let's say AutoHotKey (Take into consideration; My very limited knowledge about AHK). 
<br> 

This is my take on creating a program for easily configuring hotkeys and shortcuts. Where your HotKeys are configured in json and your actions are written in Python. The fact that your actions are written in python, gives you full control to do whatever you want to, when a key or button is pressed down, up, held or any of the other event types available now or coming later. <br> 

**Disclaimer:** I do not take responsibilty for what people use this for. I did not have malicious intent in mind when creating it. I just wanted something where I could create hotkeys for more advanced actions, that were written in a real and well documented programming language.


## TODO:
- Instead of making a shared.py for the shared functions between input controllers. Make a "InputController" which will be the parent class for both mouse and keyboard. This way they will inherit the functionality instead of importing it.
- Instead of importing different ActionController, we should just have one default ActionController that imports all functions from an "actions" directory where there are files holding actions. One file can hold multiple functions and there can be multiple files in actions folder.
- Make bind config key "hold_time". This will make it so hold will only fire when it has been held for given amount of time.
- Research making the script a command in windows registry
- Research creating windows tray icons that when clicked will show buttons for "pause"/"start" and "kill" for mouse, keyboard and both
- Create a package-installer helper function in ScriptController that will install the needed packages automatically. ActionController should come with a requirements.txt file.
- Make hold_start and hold_stop instead of only hold action
- Add new config key "event_type" which will take in the values "once"/"toggle"/"until_release"/"sequence"
     This key will tell the script if an action should be fired once, until button/key is released or until the button/key is pressed again.
     The until_release will obviously only be for "hold_start" actions
     "sequence" is for when it is an array of keys instead of a single key. This means the action will happen if the order of keys pressed are the same as in the list.



## DONE:
- Create Simple Keyboard Listener that prints out different key presses and events and closes on Key.esc
- Create ActionController that will take in KeyboardController as parameter
- Create actionHandler function that will take in controller and action string as parameters and call the correct action function
- Create action that will handle terminating keyboard listener
- Create action that will toggle the keyboard listener on/off
- Update KeyboardController to be a class instead
- Update KeyboardController to read in keyboard bindings from a json config file
- Clean up KeyboardController so there isn't so much duplicated code and checks.
- Create Logger and make it as a dynamic class that can do the very basic of checking if the path and file exist, if not then create it and then log message with datetimetimestamps
- Create MouseController and make it like the KeyboardController since the same library can create mouse listener as well. 
     It shall only handle button down and up events for now. Update later with hold/dragging? events
- Make Keyboard and MouseController threaded. So both of them can run at the same time.
- Create action that will kill MouseController
- Create action that will toggle MouseController
- Create action that will kill both Mouse and KeyboardController
- Create action that will toggle both Mouse and KeyboardController
- Refactor Controller names to reflect classnames
- Update ActionController to new logic:
     ActionController should be a parent ActionController (ScriptController) which holds the actions for pausing/resuming/killing the listeners/script entirely.
     A new ActionController class should be created that is derived from the ScriptController. 
     So it has all the parent functions for handling the script and then custom ActionControllers can be written to handle custom actions like Terraria macros, RuneScape macros and all that fun stuff ;)
- Create different command arguments 
     - "help": Display a help menu that explain how the script works and what it expects in arguments
     - "debug": Enable debugging all controllers
     - "debug-keyboard": Enable debugging keyboard
     - "debug-mouse": Enable debugging mouse
     - "disable-keyboard": Disable the keyboard listener if only mouse is desired
     - "disable-mouse": Disable the mouse listener if only keyboard is desired
- Helper functions and better descriptions for the arguments and parameters in the different classes
- Prevent user from starting script if no kill switch has been given
- Update actionHandler to take in only action as a parameter, instead of controller and action
- Update keybindings to be either a string or an array of strings. This will make it so multiple keys can do the same action. And in the long run make it so you can write actions like commands, but anywhere!?
- Update main script to find ActionController and json based on config key
- Refactor main script name to something like mhkos.py = "MyHotKeys-OnSteroids"
- Update ScriptController so it holds a history of keys pressed for easy access. An events array containing objects of the eventtype, timestamp, and key. Only save hold_start & hold_stop events.
- Make the functions in keyboard and mouse controllers into shared functions in a seperate file

## Usage:
# .\AutoHotKey-OS\mhk-os.py [ --config=terraria | default=default ]
# Args:
#   - "--base=": Will make this the base path for both logfiles and config files. Default is path this script is located in.
#   - "--base-log=": Will make this the base path for logfiles only. Default is path this script is located in + "/logs"
#   - "--log=": Filename for log and relative path compared to base path for log files. Default is "main.log".
#   - "--base-config=": Will make this the base path for config files only. Default is path this script is located in + "/config"
#   - "--config=": Name for config file and ActionController to use. So this has to match the name of a json file in the config path AND it has to match the name of a folder for an ActionController