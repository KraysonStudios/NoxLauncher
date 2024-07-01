import os
import json
import jdk
import itertools
import psutil

from constants import constants
from tkinter.messagebox import showinfo
from typing import Any, Dict, List

class Linux:

    def config() -> None:

        if not os.path.exists(constants.LINUX_HOME.value + "/Nox Launcher"):
            os.mkdir(constants.LINUX_HOME.value + "/Nox Launcher/")
            
        if not os.path.exists(constants.LINUX_HOME.value + "/Nox Launcher/java"):
            os.mkdir(constants.LINUX_HOME.value + "/Nox Launcher/java/")

        if not os.path.exists(constants.LINUX_HOME.value + "/Nox Launcher/cache"):
            os.mkdir(constants.LINUX_HOME.value + "/Nox Launcher/cache/")

        if not os.path.exists(constants.LINUX_HOME.value + "/Nox Launcher/skins"):
            os.mkdir(constants.LINUX_HOME.value + "/Nox Launcher/skins/")

        if not os.path.exists(constants.LINUX_HOME.value + "/Nox Launcher/launcher_profiles.json"):
            with open(constants.LINUX_HOME.value + "/Nox Launcher/launcher_profiles.json", "w") as f:
                json.dump({
                    "profiles" : {},                  
                    "settings": {
                        "enableAdvanced": False,
                        "profileSorting": "byName"
                    },
                    "version": 3
                }, f, indent= 4)

        if not os.path.exists(constants.LINUX_HOME.value + "/Nox Launcher/settings"):
            os.mkdir(constants.LINUX_HOME.value + "/Nox Launcher/settings/")
            os.mkdir(constants.LINUX_HOME.value + "/Nox Launcher/settings/profiles/")

            with open(constants.LINUX_HOME.value + "/Nox Launcher/settings/settings.json", "w") as f:
                json.dump({
                    "java": {},
                    "close-on-play": True
                }, f, indent= 4)

        if not os.path.exists(constants.LINUX_HOME.value + "/Nox Launcher/settings/profiles"):
            os.mkdir(constants.LINUX_HOME.value + "/Nox Launcher/settings/profiles/")

        if not os.path.exists(constants.LINUX_HOME.value + "/Nox Launcher/settings/profiles/profiles.json"):
            with open(constants.LINUX_HOME.value + "/Nox Launcher/settings/profiles/profiles.json", "w") as f:
                json.dump({
                    "profiles": {}
                }, f, indent= 4)

        if not os.path.exists(constants.LINUX_HOME.value + "/Nox Launcher/settings/settings.json"):
            with open(constants.LINUX_HOME.value + "/Nox Launcher/settings/settings.json", "w") as f:
                json.dump({
                    "java": {},
                    "close-on-play": True
                }, f, indent= 4)

        if os.path.exists(constants.LINUX_HOME.value + "/Nox Launcher/launcher_profiles.json"):
            with open(constants.LINUX_HOME.value + "/Nox Launcher/launcher_profiles.json", "r") as f:

                META: Dict[str, Any] = {
                    "profiles" : {},                  
                    "settings": {
                        "enableAdvanced": False,
                        "profileSorting": "byName"
                    },
                    "version": 3
                }

                profiles = json.load(f)

                if len(profiles.keys()) + len(profiles.values()) != len(META.keys()) + len(META.values()):
                    with open(constants.LINUX_HOME.value + "/Nox Launcher/launcher_profiles.json", "w") as f:
                        json.dump(META, f, indent= 4)

                for kp, km in itertools.zip_longest(profiles.keys(), META.keys(), fillvalue= None):

                    if kp != km:
                        with open(constants.LINUX_HOME.value + "/Nox Launcher/launcher_profiles.json", "w") as f:
                            json.dump(META, f, indent= 4)
                        break
                    elif "settings" in profiles.keys():

                        for k in profiles["settings"].keys():
                            if k not in META["settings"].keys():
                                with open(constants.LINUX_HOME.value + "/Nox Launcher/launcher_profiles.json", "w") as f:
                                    json.dump(META, f, indent= 4)
                                break
                            
                            for vp, vm in itertools.zip_longest(profiles["settings"].values(), META["settings"].values(), fillvalue= None):
                                if vp != vm:
                                    with open(constants.LINUX_HOME.value + "/Nox Launcher/launcher_profiles.json", "w") as f:
                                        json.dump(META, f, indent= 4)
                                    break

        if os.path.exists(constants.LINUX_HOME.value + "/Nox Launcher/settings/settings.json"):
            with open(constants.LINUX_HOME.value + "/Nox Launcher/settings/settings.json", "r") as f:

                settings = json.load(f)

                META: Dict[str, Any] = {
                    "java": {},
                    "close_on_play": True
                }

                if len(settings.keys()) != len(META.keys()):
                    with open(constants.LINUX_HOME.value + "/Nox Launcher/settings/settings.json", "w") as f:
                        json.dump(META, f, indent= 4)
                elif not "close_on_play" in settings:
                    with open(constants.LINUX_HOME.value + "/Nox Launcher/settings/settings.json", "w") as f:
                        json.dump(META, f, indent= 4)
                elif not "java" in settings:
                    with open(constants.LINUX_HOME.value + "/Nox Launcher/settings/settings.json", "w") as f:
                        json.dump(META, f, indent= 4)
                elif not isinstance(settings["close_on_play"], bool):
                    with open(constants.LINUX_HOME.value + "/Nox Launcher/settings/settings.json", "w") as f:
                        json.dump(META, f, indent= 4)

        with open(constants.LINUX_HOME.value + "/Nox Launcher/settings/settings.json", "r") as f:

            settings = json.load(f)

            if "path" not in settings["java"] or "args" not in settings["java"]:

                if jdk.shutil.which("java") is None:
                    showinfo("Nox Launcher", "Java is not installed. Please be patient while it is being installed. Don`t close app.", type= "ok")
                    jdk.install("21", operating_system= jdk.OperatingSystem.LINUX, arch= jdk.Architecture.X64, path= constants.LINUX_HOME + "/Nox Launcher/java/")

                    with open(constants.LINUX_HOME.value + "/Nox Launcher/settings/settings.json", "r") as f:

                        settings = json.load(f)
                        settings["java"].update({
                            "path": jdk.shutil.which("java"),
                            "args": ["-Xms1G", f"-Xmx{Linux.get_memory_ram()}M"]
                        })

                        with open(constants.LINUX_HOME.value + "/Nox Launcher/settings/settings.json", "w") as f:
                            json.dump(settings, f, indent= 4)

                else:
                    with open(constants.LINUX_HOME.value + "/Nox Launcher/settings/settings.json", "r") as f:

                        settings = json.load(f)
                        
                        settings["java"].update({
                            "path": jdk.shutil.which("java"),
                            "args": ["-Xms1G", f"-Xmx{Linux.get_memory_ram()}M"]
                        })

                        with open(constants.LINUX_HOME.value + "/Nox Launcher/settings/settings.json", "w") as f:
                            json.dump(settings, f, indent= 4)

    def get_java_info() -> List[str] | bool: 

        if os.path.exists(constants.LINUX_HOME.value + "/Nox Launcher/settings/settings.json"):
            with open(constants.LINUX_HOME.value + "/Nox Launcher/settings/settings.json", "r") as f:

                settings = json.load(f)

                if "java" not in settings: return False
                elif "path" not in settings["java"] or "args" not in settings["java"]: return False
                        
                return [settings["java"]["path"], settings["java"]["args"]]
                        
    def get_memory_ram() -> int: return round(0.40 * psutil.virtual_memory().total / (1024 ** 2))