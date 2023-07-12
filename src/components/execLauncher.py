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
        if records is None:
            return

        self._window.Register()
        submenuItems = ()
        for record in records:
            execCmd = self._configReader.Get(CONFIG_SECTION_NAME, record)
            if execCmd is None or execCmd == '':
                submenuItems += (self._window.SEPARATOR,)
            else:
                submenuItems += ((record, partial(self.exec, record)),)
            
        self._window.Register(NAME, submenu = submenuItems)
        self._window.Register()

    def exec(self, recordName, icon, menuItem):
        execCmd = self._configReader.Get(CONFIG_SECTION_NAME, recordName)
        # detaches the process from python
        splitted = execCmd.split()
        cwd = Path(splitted[0]).parent.absolute()
        process = subprocess.Popen(execCmd.split(), cwd=cwd, close_fds=True)
        text = f"Launched: '{execCmd}'"
        self.tprint(text)
        self._window.Notify(text, NAME)
        thread = threading.Thread(target=partial(self._wait, process, execCmd), daemon=True)
        thread.start()

    def tprint(self, text):
        self._window.Log(tlog(NAME, text))

    def _wait(self, p, exec):
        p.communicate()
        text = f"Finished: '{exec}' with return code: {p.returncode}"
        self.tprint(text)
        self._window.Notify(text, NAME)
    
