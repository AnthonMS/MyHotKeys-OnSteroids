## Packages
from os import path
from os import mkdir
from datetime import datetime

## Local dependencies

class Logger:
    def __init__(self, base_path = "", log = "main.log", clear_log = False):
        self.PAUSED = True
        self.WORKING = False
        self.BASE_PATH = base_path
        self.LOG_NAME = path.basename(log)
        self.LOG_PATH = path.dirname(log)
        self.DIR_PATH = path.dirname(path.join(base_path, log))
        self.FILE_PATH = path.join(self.DIR_PATH, self.LOG_NAME)
        self.checkIfPathExist()

        if (clear_log):
            self.clear()

        self.log("Logger Initiated...")
    
    def __str__(self):
        return f"""
        Logger:
            Paused: {self.PAUSED}
            Working: {self.WORKING}
            Base Path: {self.BASE_PATH}
            Log Name: {self.LOG_NAME}
            Log Path: {self.LOG_PATH}
            Dir Path: {self.DIR_PATH}
            File Path: {self.FILE_PATH}
        """
    
    def checkIfPathExist(self):
        if (not path.exists(self.DIR_PATH) or not path.exists(self.FILE_PATH)):
            self.createFileAndFolders()
        else:
            self.PAUSED = False
    
    def createFileAndFolders(self):
        self.WORKING = True
        if (not path.exists(self.DIR_PATH)):
            mkdir(self.DIR_PATH)

        if (not path.exists(self.FILE_PATH)):
            f = open(self.FILE_PATH, "w")
            f.close()

        if (path.exists(self.FILE_PATH)):
            self.PAUSED = False
        
        self.WORKING = False
    

    def clear(self):
        if (self.PAUSED):
            return "Logger Paused"

        open(self.FILE_PATH, 'w').close()
        self.log("LOG CLEARED")
    
    def log(self, msg):
        if (self.PAUSED):
            print("Logger Paused")
            return "Logger Paused"
        
        self.WORKING = True
        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S") # dd/mm/YY H:M:S

        f = open(self.FILE_PATH, "a")
        f.write(dt_string + ": ")
        f.write(msg)
        f.write("\n")
        f.close()
        
        self.WORKING = False
    
## Usage:
# logger = Logger(base_path = "D:\Folders\Logs", log_path = "default.log")
# logger.log("Log this")