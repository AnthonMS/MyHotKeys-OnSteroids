## Packages
from os import path
import sys
import json

## Append this ActionController directory to path (If append messed change to: sys.path.insert(0, path.dirname(__file__)))
sys.path.append(path.dirname(__file__))

## Local dependencies
from controllers.ScriptController import ScriptController
from helpers import *


class ActionController(ScriptController):
    def __init__(self, keyboard_ctrl, mouse_ctrl, debug, logger):
        super().__init__(keyboard_ctrl, mouse_ctrl, debug, logger)
        self.CALIBRATED = False
        self.CALIBRATING = False
        self.CALIBRATED_SLOTS = [] # Only used for newly calibrated slots
        self.CALIBRATION_CONFIG_PATH = path.join(path.dirname(__file__), "calibration.json")
        self.CALIBRATION_CONFIG = []
        self.CALCULATED_UI_SIZE = 100

        self.loadCalibration()

        if (not self.CALIBRATED):
            print("Please start the game and run the calibration automation.")
        
    
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
        activeWindow = pyautogui.getActiveWindowTitle()
        if ("terraria" in activeWindow.lower()):
            if (action == "calibrate"):
                self.calibrate()
            elif (action == "staff_of_discord"):
                self.debug(f"Active Window: {activeWindow}")
                self.staffOfDiscord()
            elif (action == "cellphone"):
                self.cellphone()
            else:
                self.debug(f"Handle Custom Action: {action}")
        else:
            self.debug("Terraria is not the active window")
    
    def staffOfDiscord(self):
        self.debug("Handling staff of discord action!")
        ## Figure out which slot is active now
        activeSlotCords = locateActiveSlotOnScreen(self)
        activeSlot = [x for x in self.CALIBRATION_CONFIG if x["x"] == activeSlotCords[0] ][0] ## Get slot from current active slot position
        staffSlot = [x for x in self.CALIBRATION_CONFIG if x["item"] == "staff_of_discord" ][0] ## Get slot holding staff


        ## press the key for the slot with the staff
        ## click the mouse button
        ## press the key for the active slot changing
        pyautogui.keyDown(staffSlot['slot'])
        pyautogui.keyUp(staffSlot['slot'])
        pyautogui.mouseDown()
        pyautogui.mouseUp()
        pyautogui.keyDown(activeSlot['slot'])
        pyautogui.keyUp(activeSlot['slot'])


    def cellphone(self):
        self.debug("Handling cellphone action!")
        ## Figure out which slot is active now
        activeSlotCords = locateActiveSlotOnScreen(self)
        activeSlot = [x for x in self.CALIBRATION_CONFIG if x["x"] == activeSlotCords[0] ][0] ## Get slot from current active slot position
        cellphoneSlot = [x for x in self.CALIBRATION_CONFIG if x["item"] == "cellphone" ][0] ## Get slot holding staff

        ## press the key for the slot with the staff
        ## click the mouse button
        ## press the key for the active slot changing
        pyautogui.keyDown(cellphoneSlot['slot'])
        pyautogui.keyUp(cellphoneSlot['slot'])
        pyautogui.mouseDown()
        pyautogui.mouseUp()
        pyautogui.keyDown(activeSlot['slot'])
        pyautogui.keyUp(activeSlot['slot'])

    def loadCalibration(self):
        if (not path.exists(self.CALIBRATION_CONFIG_PATH)):
            f = open(self.CALIBRATION_CONFIG_PATH, "w")
            f.write("[]")
            f.close()
            return False
        
        try:
            f = open(self.CALIBRATION_CONFIG_PATH, "r")
            self.CALIBRATION_CONFIG = json.load(f)
            f.close()
            self.CALIBRATED = True
        except json.decoder.JSONDecodeError:
            self.debug(f"calibration config file is not in a correct json format. Please open the game and run the calibration again.")
            return False
        # for item in self.CALIBRATION_CONFIG:
        #     print(item)



    def calibrate(self):
        ## Check if the last key was the toggle/start calibration
        calibrateToggleKey = [item for item in self.KEYBOARD_CTRL.KEYBINDS if item['action']=="calibrate"][0]['key']
        if (self.getLastEventKey() == str(calibrateToggleKey)):
                self.CALIBRATING = not self.CALIBRATING
                if (self.CALIBRATING):
                    self.debug("Started calibrating slots...")
                    self.CALIBRATED_SLOTS = [] # Reset calibrated keys when starting a new calibration
                else:
                    self.debug("Stopped calibrating slots. Did NOT save!")
        
        ## Try to figure out UI Scale based on position of first slot
        calibrateUISize(self)

        for i in range(0, 10):
            # Determine where to look for active slot i
            # new_slot_config = self.calibrateSlot(str(i), auto = True)
            new_slot_config = calibrateThisSlot(self, str(i), auto = True) # helper

            # Save in config array to save later
            try:
                old_slot_config = [x for x in self.CALIBRATION_CONFIG if x["slot"] == str(i)][0]
                old_slot_index = self.CALIBRATION_CONFIG.index(old_slot_config)
                self.CALIBRATION_CONFIG[old_slot_index] = new_slot_config
            except IndexError:
                self.CALIBRATION_CONFIG.append(new_slot_config)

            # if (i == 1):
            #     calculateUISize(self, self.CALIBRATION_CONFIG)
                

        # calculateUISize(self, self.CALIBRATION_CONFIG)


        # Finish up
        self.saveCalibration()
        self.CALIBRATING = False
        self.debug("Finished calibrating slots automatically...")
        

    def saveCalibration(self):
        self.debug("Saving Calibration...")
        f = open(self.CALIBRATION_CONFIG_PATH, "w")
        json.dump(self.CALIBRATION_CONFIG, f)
        f.close()
        pass



## TODO:
## - When all slots have been calibrated:
##      determine the ui scale based on the amount of pixels between two slots
##      determine which slot the cellphone and which slot the staff of discord are in
## - Save calibration in a json config
## - Load calibration on startup to see if there is one already
## - Create the actual calibration logic. First time working with Image Processing.

## DONE:
## Create calibration function for the number row actions.
## Update calibration to be only 1 button to start/stop the calibration
## Finish calibration when it has recorded 0 through 9.