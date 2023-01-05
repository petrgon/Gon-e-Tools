from pathlib import Path
from shutil import copy2
import threading
import os

from window import Window
from configReader import ConfigReader
import helper


FOLDER = Path(__file__).parent
NAME = "Create User Colors"
CONFIG_SECTION_NAME = "createusercolors"
CONFIG_KEY_NAME = "lookuppath"

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
        data = """
# Highlight users

"""

        execFolder = Path(self._configReader.Get(CONFIG_SECTION_NAME, CONFIG_KEY_NAME))
        self._window.Notify(f"Launched", NAME)
        path: Path
        for path in execFolder.rglob(".git"):
            if path.is_dir() and path.name == ".git":
                dir = path / "fork"
                try:
                    os.makedirs(dir, exist_ok=True)
                except OSError as error:
                    self._window.Log(helper.tlog(NAME, f"Unable to create {dir.name} because of {error}"))
                file = dir / "user-colors"
                with file.open(mode="w") as fp:
                    fp.write(data)
                    self._window.Log(helper.tlog(NAME, f"Wrote to {path.parent.name}"))
        
        self._window.Notify(f"Finished", NAME)
