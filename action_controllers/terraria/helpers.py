import pyautogui # pip3 install pyautogui && pip3 install Pillow && pip3 install opencv-python
import os
from os import path
import time


def calibrateUISize(actionCtrl):
    pyautogui.keyDown("1")
    pyautogui.keyUp("1")
    time.sleep(0.15)

    pos = locateActiveSlotOnScreen(actionCtrl)

    screen_width, screen_height = pyautogui.size()
    if (not screen_width == 1920 and not screen_height == 1080):
        actionCtrl.debug(f"Only tested with resolution 1080x1920. Resolution {screen_height}x{screen_width} detected. Trying to calclulate the best I can.")
    
    
    if (pos[0] >= 10 and pos[0] <= 15):
        actionCtrl.CALCULATED_UI_SIZE = 75
    elif (pos[0] >= 16 and pos[0] <= 21):
        actionCtrl.CALCULATED_UI_SIZE = 100
    elif (pos[0] >= 22 and pos[0] <= 27):
        actionCtrl.CALCULATED_UI_SIZE = 125
    elif (pos[0] >= 28 and pos[0] <= 33):
        actionCtrl.CALCULATED_UI_SIZE = 150
    elif (pos[0] >= 34 and pos[0] <= 34):
        actionCtrl.CALCULATED_UI_SIZE = 175
    elif (pos[0] >= 35 and pos[0] <= 40):
        actionCtrl.CALCULATED_UI_SIZE = 200
    
    actionCtrl.debug(f"Calculated UI Size: {actionCtrl.CALCULATED_UI_SIZE}")
    


def calibrateThisSlot(actionCtrl, slot, auto = False):
    if (auto):
        pyautogui.keyDown(slot)
        pyautogui.keyUp(slot)

    time.sleep(0.15)
    screen_width, screen_height = pyautogui.size()

    new_slot_config = {
        "slot": slot,
        "x": "x",
        "y": "y",
        "item": "?"
    }

    pos = locateActiveSlotOnScreen(actionCtrl)
    new_slot_config['x'] = pos[0]
    new_slot_config['y'] = pos[1]
    terraria_hotbar_region = (5,10, screen_width/2, 100)
    if (actionCtrl.DEBUG):
        takeScreenshot(img="debug/test_bar.png", region=terraria_hotbar_region)
        takeScreenshot(img=f"debug/test_slot.png", region=(new_slot_config['x']+5, new_slot_config['y']-10, 50, 50))

    # Determine which item is in this spot (if possible)
    new_slot_config = calibrateThisItem(actionCtrl, new_slot_config)

    return new_slot_config


## Calibrate different items to the corrosponding slot number
def calibrateThisItem(actionCtrl, slot):
    slot_regions = [
        {
            "ui_size": 75,
            "slot_size": (slot['x']+5, slot['y']-5, 35, 35)
        },
        {
            "ui_size": 100,
            "slot_size": (slot['x']+5, slot['y']-10, 50, 50)
        },
        {
            "ui_size": 125,
            "slot_size": (slot['x']+5, slot['y']-15, 60, 60)
        },
        {
            "ui_size": 150,
            "slot_size": (slot['x']+5, slot['y']-20, 70, 70)
        },
        {
            "ui_size": 175,
            "slot_size": (slot['x']+5, slot['y']-25, 70, 70)
        },
        {
            "ui_size": 200,
            "slot_size": (slot['x']+5, slot['y']-25, 85, 85)
        }
    ]
    
    ## Find the size of an inventory slot based on UI size
    slot_region = [x for x in slot_regions if x["ui_size"] == actionCtrl.CALCULATED_UI_SIZE ][0]['slot_size']

    if (actionCtrl.DEBUG):
        takeScreenshot(img=f"debug/slot_{slot['slot']}.png", region=slot_region)

    ## Get a list of pngs from items image dir
    items_path = f"{path.dirname(__file__)}/images/items"
    for item_img in os.listdir(items_path):
        if (not item_img.lower().endswith(('.png'))):
            break
        item_path = path.join(items_path, item_img)
        locate = locateImageOnScreen(item_path, region = slot_region, confidence = 0.95)
        if (locate):
            slot['item'] = item_img.replace('.png', '')

    return slot



def locateActiveSlotOnScreen(actionCtrl):
    screen_width, screen_height = pyautogui.size()
    terraria_hotbar_region = (5,10, screen_width/2, 100)
    terraira_active_slot_color = (255, 219, 8)
    pos = locatePixelByRGB(region = terraria_hotbar_region, rgb = terraira_active_slot_color )
    if (pos == (-1, -1)):
        ## Handle the error
        actionCtrl.debug("Active slot not found in given hotswap region on screen. See region in images/errors/active_slot_not_found_in_this_region.png")
        takeScreenshot("errors/active_slot_not_found_in_this_region.png", region=terraria_hotbar_region, save = True)

    return pos


## Calculate based on space between slots. Its good, but not good that we need to know 2 positions before we can figure it out.
## We can use this when all other has been done and we want to be more sure it has correct UI Size
def calculateUISize(actionCtrl, calibrationSlots):
    actionCtrl.debug("Calculating UI Size from the calibrated slot positions and screen resolution...")
    screen_width, screen_height = pyautogui.size()
    ## Figure out how many pixels there are between this slot and the next if there is one
    if (not screen_width == 1920 and not screen_height == 1080):
        actionCtrl.debug(f"Only tested with resolution 1080x1920. Resolution {screen_height}x{screen_width} detected. Trying to calclulate the best I can.")
    
    slot = calibrationSlots[0]
    nextSlot = calibrationSlots[1]

    pixel_diff = nextSlot['x'] - slot['x'] 
    if (pixel_diff >= 30 and pixel_diff <= 39):
        actionCtrl.CALCULATED_UI_SIZE = 75
    elif (pixel_diff >= 40 and pixel_diff <= 49):
        actionCtrl.CALCULATED_UI_SIZE = 100
    elif (pixel_diff >= 50 and pixel_diff <= 59):
        actionCtrl.CALCULATED_UI_SIZE = 125
    elif (pixel_diff >= 60 and pixel_diff <= 69):
        actionCtrl.CALCULATED_UI_SIZE = 150
    elif (pixel_diff >= 70 and pixel_diff <= 79):
        actionCtrl.CALCULATED_UI_SIZE = 175
    elif (pixel_diff >= 80 and pixel_diff <= 89):
        actionCtrl.CALCULATED_UI_SIZE = 200
    
    actionCtrl.debug(f"UI Size equated to {actionCtrl.CALCULATED_UI_SIZE}")



def locatePixelByRGB(region, rgb):
    pos = (-1, -1)
    s = takeScreenshot("", region=region, save = False)

    for x in range(s.width):
        if (pos == (-1, -1)):
            for y in range(s.height):
                if (pos == (-1, -1)):
                    if s.getpixel((x, y)) == rgb:
                        pos = (x, y)
                else:
                    break
        else:
            break
    
    return pos



def takeScreenshot(img, region = None, save = True):
    # region = (left, top, width, height )
    if img == "":
        img = f"{path.dirname(__file__)}/images/test.png"
    else:
        img = f"{path.dirname(__file__)}/images/{img}"

    if (region is None):
        myScreenshot = pyautogui.screenshot() 
    else:
        myScreenshot = pyautogui.screenshot(region=region)
    
    if (save):
        myScreenshot.save(img)

    return myScreenshot

# locateImageOnScreen(f"{img_path}/steamlogo.png", region=windows_bar_region, confidence=confidence)
def locateImageOnScreen(img, region = None, confidence = 0.5):
    if (region is None):
        start = pyautogui.locateCenterOnScreen(img, confidence = confidence) # .png is a must!
    else:
        start = pyautogui.locateCenterOnScreen(img, region=region, confidence = confidence) # .png is a must!

    return start # coords = middle of 