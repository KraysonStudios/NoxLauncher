import os

from enum import Enum

class constants(Enum):

    WINDOWS_HOME = os.environ.get("APPDATA")
    LINUX_HOME = os.environ.get("HOME")
    MAX_WIDTH = 1920
    MAX_HEIGHT = 1080
    MIN_WIDTH = 900
    MIN_HEIGHT = 600