from pathlib import Path
from shutil import copy2
import threading
import win32api

from window import Window
from configReader import ConfigReader
from helper import tlog


FOLDER = Path(__file__).parent
NAME = "Print Versions"
CONFIG_SECTION_NAME = "printversion"

class PrintVersion:
    _window: Window = None
    _configReader: ConfigReader = None

    def __init__(self, director):
        self._window = director._window
        self._configReader = director._configReader
        self._window.Register(NAME, self.Exec)

    def Exec(self):
        thread = threading.Thread(target=self._Exec, daemon=True)
        thread.start()
        
    def _Exec(self):
        self._window.ShowWindow()
        
        records = self._configReader.GetSection(CONFIG_SECTION_NAME)
        for record in records:
            execPath = self._configReader.Get(CONFIG_SECTION_NAME, record)
            self._window.Log(tlog(NAME, f"{record}: {self._GetFileVersion(execPath)}"))

    def _GetFileVersion(self, path):
        try:
            info = win32api.GetFileVersionInfo(path, '\\')
            ms = info['FileVersionMS']
            ls = info['FileVersionLS']
            return f"{win32api.HIWORD(ms)}.{win32api.LOWORD(ms)}.{win32api.HIWORD(ls)}.{win32api.LOWORD(ls)}"
        except Exception as e:
            return None
