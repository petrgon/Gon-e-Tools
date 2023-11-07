from components.createIssueTracker import CreateIssueTracker
from window import Window
from configReader import ConfigReader

from components.switchToSsh import SwitchToSsh
from components.execLauncher import ExecLauncher
from components.createIssueTracker import CreateIssueTracker
from components.createUserColors import CreateUserColors
from components.printVersion import PrintVersion
from components.healthySpine import HealthySpine

class Director:
    _window: Window = None
    _configReader: ConfigReader = None

    # Here you can hold instances of custom components
    _switchToSsh: SwitchToSsh = None
    _execLauncher: ExecLauncher = None
    _createIssueTracker: CreateIssueTracker = None
    _createUserColors: CreateUserColors = None
    _printVersion: PrintVersion = None
    _healthySpine: HealthySpine = None

    def __init__(self):
        # must be first
        self._window = Window()
        self._configReader = ConfigReader(self)

        # Here you can register custom components
        self._switchToSsh = SwitchToSsh(self)
        self._createIssueTracker = CreateIssueTracker(self)
        self._createUserColors = CreateUserColors(self)
        self._printVbsVersion = PrintVersion(self)
        self._launchVbs = ExecLauncher(self)
        self._healthySpine = HealthySpine(self)
        return

    def run(self):
        self._window.Run()
        return