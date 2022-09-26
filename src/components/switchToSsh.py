from pathlib import Path
from os import system
import os
import subprocess
import threading

from helper import tlog
from window import Window
from configReader import ConfigReader

PIPE = subprocess.PIPE
NAME = "Switch to SSH"
CONFIG_SECTION_NAME = "switchtossh"
CONFIG_KEY_NAME = "lookuppath"
CONFIG_GITLAB_URL_KEY_NAME = "gitlab_url"

# @Author Alwin Postmus

# Switch to SSH functionality
class SwitchToSsh:
    _window: Window = None
    _configReader: ConfigReader = None
    _gitlabUrl: str = None
    def __init__(self, director):
        self._window = director._window
        self._configReader = director._configReader
        self._gitlabUrl = self._configReader.Get(CONFIG_SECTION_NAME, CONFIG_GITLAB_URL_KEY_NAME)
        self._window.Register("Switch to SSH", self.exec)

    def exec(self):
        thread = threading.Thread(target=self._exec, daemon=True)
        thread.start()

    def _exec(self):
        # system('title ' + constants.APP_NAME)
        folder = self._configReader.Get(CONFIG_SECTION_NAME, CONFIG_KEY_NAME)

        if(folder == None):
            self._window.Notify("Configuration not set.", NAME)
            return
            
        path: Path = Path(folder)  
        if not path.exists():
            self._window.Notify(f"Given path {folder} does not exist.", NAME)
            return

        if not path.is_dir():
            self._window.Notify(f"Given path {folder} is not folder.", NAME)
            return
            
        self._window.Notify("Started.", NAME)
        for path in os.scandir(folder):
            if not path.is_dir():
                continue
            self.tprint(f"Processing {path.name}")
            process = subprocess.Popen(
                ['git', 'config', '--get', 'remote.origin.url'], universal_newlines=True, cwd=path.path, stdout=PIPE, stderr=PIPE, shell=True)
            stdoutput = process.communicate()[0]

            if 'fatal' in stdoutput:
                self.tprint(f"Failed to get remote for {path.name}")
                continue

            if 'https://' in stdoutput:
                url: str = 'git@' + self._gitlabUrl + ':' + \
                    stdoutput.split(self._gitlabUrl + '/', 1)[1].rstrip('\n')
                process = subprocess.Popen(
                    ['git', 'remote', 'set-url', 'origin', url], universal_newlines=True, cwd=path.path, stdout=PIPE, stderr=PIPE)
                stdoutput = process.communicate()[0]
                if 'fatal' in stdoutput:
                    self.tprint(f"Failed to change remote for {path.name}")
                    continue

                self.tprint(f"Origin updated for {path.name}")
                
        self._window.Notify("Finished.", NAME)

    def tprint(self, text):
        self._window.Log(tlog(NAME, text))
