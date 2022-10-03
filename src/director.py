from components.mugwungs import Mugwungs
from components.createIssueTracker import CreateIssueTracker
from window import Window
from configReader import ConfigReader

from components.switchToSsh import SwitchToSsh
from components.execLauncher import ExecLauncher
from components.createIssueTracker import CreateIssueTracker
from components.mugwungs import Mugwungs

class Director:
    _window: Window = None
    _configReader: ConfigReader = None

    # Here you can hold instances of custom components
    _switchToSsh: SwitchToSsh = None
    _execLauncher: ExecLauncher = None
    _createIssueTracker: CreateIssueTracker = None
    _mugwungs: Mugwungs = None

    def __init__(self):
        # must be first
        self._window = Window()
        self._configReader = ConfigReader()

        # Here you can register custom components
        self._switchToSsh = SwitchToSsh(self)
        self._createIssueTracker = CreateIssueTracker(self)
        self._launchVbs = ExecLauncher(self)
        self._mugwungs = Mugwungs(self)
        return

    def run(self):
        self._window.Run()
        return