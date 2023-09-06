from datetime import datetime
import os
import sys
from constants import APP_DIR

def tlog(componentName, text):
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    return (f'[{timestamp}] [{componentName}]: {text}\n')

def GetAbsoluteResourcePath(relativePath):
    try:
        # PyInstaller stores data files in a tmp folder refered to as _MEIPASS
        basePath = sys._MEIPASS
    except Exception:
        # If not running as a PyInstaller created binary, try to find the data file as
        # an installed Python egg
        try:
            basePath = os.path.dirname(sys.modules[APP_DIR].__file__)
        except Exception:
            basePath = ''

        # If the egg path does not exist, assume we're running as non-packaged
        if not os.path.exists(os.path.join(basePath, relativePath)):
            basePath = APP_DIR

    path = os.path.join(basePath, relativePath)

    if not os.path.exists(path):
        return None

    return path