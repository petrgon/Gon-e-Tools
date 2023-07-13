from pathlib import Path
from shutil import copy2
import threading
import os

from window import Window
from configReader import ConfigReader
from helper import tlog


FOLDER = Path(__file__).parent
NAME = "Create User Colors"
CONFIG_SECTION_NAME = "createusercolors"
CONFIG_KEY_LOOKUP = "lookuppath"

class CreateUserColors:
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
        records = self._configReader.GetSection(CONFIG_SECTION_NAME)
        if records is None:
            return
    
        foundAny = False;
        data = "# Highlight users"
        for record in records:
            if record == CONFIG_KEY_LOOKUP:
                continue

            foundAny = True
            color = self._configReader.Get(CONFIG_SECTION_NAME, record)
            if color is not None or color != "":
                data += f"\n{record} {color}"

        if foundAny == False:
            text = f"{NAME} is not configured properly"
            self._window.Notify(text, NAME)
            self._window.Log(tlog(NAME, text))

        execFolder = Path(self._configReader.Get(CONFIG_SECTION_NAME, CONFIG_KEY_LOOKUP))
        self._window.Notify("Launched", NAME)
        self._window.Log(tlog(NAME, f"Using:\n{data}"))
        self._window.Log(tlog(NAME, "Started"))
        path: Path
        for path in execFolder.rglob(".git"):
            if path.is_dir() and path.name == ".git":
                dir = path / "fork"
                try:
                    os.makedirs(dir, exist_ok=True)
                except OSError as error:
                    self._window.Log(tlog(NAME, f"Unable to create {dir.name} because of {error}"))
                file = dir / "user-colors"
                with file.open(mode="w") as fp:
                    fp.write(data)
                    self._window.Log(tlog(NAME, f"Wrote to {path.parent.name}"))
        
        self._window.Log(tlog(NAME, "Done"))
        self._window.Notify("Finished", NAME)
