import json
from datetime import datetime

def load_keybinds(ctrl, caller):
    f = open(ctrl.CONFIG_PATH, "r")
    data = json.load(f)
    f.close()

    for bind in data['binds']:
        if (bind['peripheral'] == caller):
            ctrl.KEYBINDS.append(bind)
            if (bind['event'] == "up"):
                ctrl.EVENTS_UP.append(bind)
            elif (bind['event'] == "down"):
                ctrl.EVENTS_DOWN.append(bind)
            elif (bind['event'] == "hold"):
                ctrl.EVENTS_HOLD.append(bind)

def debug(ctrl, str):
    if (ctrl.DEBUG):
        print(str)
        log(ctrl, str)

def log(ctrl, msg):
    if (ctrl.LOGGER is None):
        print("Logger is None")
    
    ctrl.LOGGER.log(msg)


def doActionIfThereIsOne(ctrl, key, bindings):
    keep_alive = True
    if (len(bindings) > 0):
        bind = key_exist_as_bind(ctrl, key, bindings)
        if (type(bind) is dict):
            if ("toggle" in bind["action"] or "kill" in bind["action"] or not ctrl.PAUSED):
                keep_alive = ctrl.ACTION_CTRL.handleAction(bind['action'])
    
    return keep_alive

    
def addEventToHistory(ctrl, key, event):
    new_event = {
        "key": key,
        "event": event,
        "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S") # dd/mm/YY H:M:S
    }
    if (new_event['event'] == "hold"):
        new_event['event'] = "hold_start"
    
    # print(f"adding event::: {new_event}")
    # print(f"ctrl.ACTION_CTRL.getLastEvent()?::: {ctrl.ACTION_CTRL.getLastEvent()}")
    last_event = ctrl.ACTION_CTRL.getLastEvent()
    # print(f"last_event::: {last_event}")
    if (last_event):
        if (new_event['key'] == last_event['key'] and new_event['event'] == last_event['event']):
            pass ## Do not save duplicate events
        else:
            if (last_event['event'] == "hold_start" and new_event['event'] == "up"):
                new_event['event'] = "hold_stop"
            ctrl.ACTION_CTRL.EVENT_HISTORY.append(new_event)
    else:
        ctrl.ACTION_CTRL.EVENT_HISTORY.append(new_event)

            
## Check if the pressed key exist in the given binds list
def key_exist_as_bind(ctrl, key, binds):
    for bind in binds:
        try: 
            if (str(key.char) == str(bind['key'])):
                return bind
        except KeyError: # Raised if ['key'] does not exist in bind
            if (str(key.char) in bind['keys']):
                    return bind
        except AttributeError: # Raised if key.char does not exist
            try:
                if (str(key) == str(bind['key'])):
                    return bind
            except KeyError: # Raised again if ['key'] does not exist in bind
                    if (str(key) in str(bind['keys'])):
                        return bind

            
    return False