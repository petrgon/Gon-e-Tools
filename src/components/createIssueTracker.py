from pathlib import Path
from shutil import copy2
import threading

from window import Window
from configReader import ConfigReader
import helper


FOLDER = Path(__file__).parent
NAME = "Create Issue Tracker"
CONFIG_SECTION_NAME = "createissuetracker"
CONFIG_KEY_LOOKUP = "lookuppath"

class CreateIssueTracker:
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
        dataTemplate = """
# Integration with Issue Tracker
#
# (note that '\' need to be escaped).

[issuetracker "{name}"]
regex = "(\\w+-\\d+)"
url = "{url}$1"
"""

        self._window.Notify("Launched", NAME)
        records = self._configReader.GetSection(CONFIG_SECTION_NAME)
        for record in records:
            if record == CONFIG_KEY_LOOKUP:
                continue

            issueTrackerUrl = self._configReader.Get(CONFIG_SECTION_NAME, record)
            if issueTrackerUrl == "":
                continue

            data = dataTemplate.format(name = record, url = issueTrackerUrl)
            
            self._window.Log(helper.tlog(NAME, f"Using:\n{data}"))
            execFolder = Path(self._configReader.Get(CONFIG_SECTION_NAME, CONFIG_KEY_LOOKUP))
            path: Path
            for path in execFolder.rglob(".git"):
                if path.is_dir() and path.name == ".git":
                    fileUrl = path / "issuetracker"
                    with fileUrl.open(mode="w") as fp:
                        fp.write(data)
                        self._window.Log(helper.tlog(NAME, f"Wrote to {path.parent.name}"))
            
        self._window.Log(helper.tlog(NAME, "Done"))
        self._window.Notify("Finished", NAME)
