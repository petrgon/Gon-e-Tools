from tokenize import String
import subprocess
from functools import partial
import threading
from pathlib import Path

from helper import tlog
from window import Window
from configReader import ConfigReader

CONFIG_SECTION_NAME = "execlauncher"
NAME = "Exec Launcher"


class ExecLauncher:
    _window: Window = None
    _configReader: ConfigReader = None

    def __init__(self, director):
        self._window = director._window
        self._configReader = director._configReader

        
        records = self._configReader.GetSection(CONFIG_SECTION_NAME)
        
        self._window.Register()
        submenuItems = ()
        for record in records:
            submenuItems += ((record, partial(self.exec, record)),)
            
        self._window.Register(NAME, submenu = submenuItems)
        self._window.Register()

    def exec(self, recordName, icon, menuItem):
        exec = self._configReader.Get(CONFIG_SECTION_NAME, recordName)
        # detaches the process from python
        splitted = exec.split()
        cwd = Path(splitted[0]).parent.absolute()
        process = subprocess.Popen(exec.split(), cwd=cwd, close_fds=True)
        text = f"Launched: '{exec}'"
        self.tprint(text)
        self._window.Notify(text, NAME)
        thread = threading.Thread(target=partial(self._wait, process, exec), daemon=True)
        thread.start()

    def tprint(self, text):
        self._window.Log(tlog(NAME, text))

    def _wait(self, p, exec):
        p.communicate()
        text = f"Finished: '{exec}' with return code: {p.returncode}"
        self.tprint(text)
        self._window.Notify(text, NAME)
    
