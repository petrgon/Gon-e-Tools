from pathlib import Path
from shutil import copy2
import threading
import time

from window import Window
from configReader import ConfigReader
from helper import tlog


FOLDER = Path(__file__).parent
NAME = "Healthy Spine"
CONFIG_SECTION_NAME = "healthyspine"
CONFIG_KEY_LOOKUP = "interval"

class HealthySpine:
    _window: Window = None
    _configReader: ConfigReader = None

    def __init__(self, director):
        self._window = director._window
        self._configReader = director._configReader
        self.Exec()

    def Exec(self):
        thread = threading.Thread(target=self._Exec, daemon=True)
        thread.start()

    def GetWaitTime(self):
        return self._configReader.Get(CONFIG_SECTION_NAME, CONFIG_KEY_LOOKUP)
        
    def _Exec(self):
        try:
            while True:
                waitTime = int(self.GetWaitTime())
                self._window.Log(tlog(NAME, "Waiting for " + str(waitTime) + " seconds"))
                time.sleep(waitTime)
                self._window.Notify("Sit straight!", NAME)
        except Exception as e:
            self._window.Log(tlog(NAME, e))

            
