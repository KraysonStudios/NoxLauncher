import os
import json
import jdk
import itertools
import psutil
import flet
import platform

from tkinter.messagebox import showinfo
from typing import Any, Dict, List

class Config:

    def check() -> None:

        if not os.path.exists(Config.get_path() + "/Nox Launcher"):
            os.mkdir(Config.get_path() + "/Nox Launcher/")
            
        if not os.path.exists(Config.get_path() + "/Nox Launcher/java"):
            os.mkdir(Config.get_path() + "/Nox Launcher/java/")

        if not os.path.exists(Config.get_path() + "/Nox Launcher/cache"):
            os.mkdir(Config.get_path() + "/Nox Launcher/cache/")

        if not os.path.exists(Config.get_path() + "/Nox Launcher/skins"):
            os.mkdir(Config.get_path() + "/Nox Launcher/skins/")

        if not os.path.exists(Config.get_path() + "/Nox Launcher/launcher_profiles.json"):
            with open(Config.get_path() + "/Nox Launcher/launcher_profiles.json", "w") as f:
                json.dump({
                    "profiles" : {},                  
                    "settings": {
                        "enableAdvanced": False,
                        "profileSorting": "byName"
                    },
                    "version": 3
                }, f, indent= 4)

        if not os.path.exists(Config.get_path() + "/Nox Launcher/settings"):
            os.mkdir(Config.get_path() + "/Nox Launcher/settings/")
            os.mkdir(Config.get_path() + "/Nox Launcher/settings/profiles/")

            with open(Config.get_path() + "/Nox Launcher/settings/settings.json", "w") as f:
                json.dump({
                    "java": {},
                    "close-on-play": True
                }, f, indent= 4)

        if not os.path.exists(Config.get_path() + "/Nox Launcher/settings/profiles"):
            os.mkdir(Config.get_path() + "/Nox Launcher/settings/profiles/")

        if not os.path.exists(Config.get_path() + "/Nox Launcher/settings/profiles/profiles.json"):
            with open(Config.get_path() + "/Nox Launcher/settings/profiles/profiles.json", "w") as f:
                json.dump({
                    "profiles": {}
                }, f, indent= 4)

        if not os.path.exists(Config.get_path() + "/Nox Launcher/settings/settings.json"):
            with open(Config.get_path() + "/Nox Launcher/settings/settings.json", "w") as f:
                json.dump({
                    "java": {},
                    "close-on-play": True
                }, f, indent= 4)

        if os.path.exists(Config.get_path() + "/Nox Launcher/launcher_profiles.json"):
            with open(Config.get_path() + "/Nox Launcher/launcher_profiles.json", "r") as f:

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
                    with open(Config.get_path() + "/Nox Launcher/launcher_profiles.json", "w") as f:
                        json.dump(META, f, indent= 4)

                for kp, km in itertools.zip_longest(profiles.keys(), META.keys(), fillvalue= None):

                    if kp != km:
                        with open(Config.get_path() + "/Nox Launcher/launcher_profiles.json", "w") as f:
                            json.dump(META, f, indent= 4)
                        break
                    elif "settings" in profiles.keys():

                        for k in profiles["settings"].keys():
                            if k not in META["settings"].keys():
                                with open(Config.get_path() + "/Nox Launcher/launcher_profiles.json", "w") as f:
                                    json.dump(META, f, indent= 4)
                                break
                            
                            for vp, vm in itertools.zip_longest(profiles["settings"].values(), META["settings"].values(), fillvalue= None):
                                if vp != vm:
                                    with open(Config.get_path() + "/Nox Launcher/launcher_profiles.json", "w") as f:
                                        json.dump(META, f, indent= 4)
                                    break

        if os.path.exists(Config.get_path() + "/Nox Launcher/settings/settings.json"):
            with open(Config.get_path() + "/Nox Launcher/settings/settings.json", "r") as f:

                settings = json.load(f)

                META: Dict[str, Any] = {
                    "java": {
                        "path": jdk.shutil.which("java"),
                        "args": ["-Xms1G", f"-Xmx{Config.get_memory_ram()}M"]
                    },
                    "close_on_play": True
                }

                if len(settings.keys()) != len(META.keys()):
                    with open(Config.get_path() + "/Nox Launcher/settings/settings.json", "w") as f:
                        json.dump(META, f, indent= 4)
                elif not "close_on_play" in settings:
                    with open(Config.get_path() + "/Nox Launcher/settings/settings.json", "w") as f:
                        json.dump(META, f, indent= 4)
                elif not "java" in settings:
                    with open(Config.get_path() + "/Nox Launcher/settings/settings.json", "w") as f:
                        json.dump(META, f, indent= 4)
                elif not isinstance(settings["java"], dict):
                    with open(Config.get_path() + "/Nox Launcher/settings/settings.json", "w") as f:
                        json.dump(META, f, indent= 4)
                elif not "path" in settings["java"] or not "args" in settings["java"]:
                    with open(Config.get_path() + "/Nox Launcher/settings/settings.json", "w") as f:
                        json.dump(META, f, indent= 4)
                elif not isinstance(settings["java"]["path"], str) or not isinstance(settings["java"]["args"], list):
                    with open(Config.get_path() + "/Nox Launcher/settings/settings.json", "w") as f:
                        json.dump(META, f, indent= 4)
                elif not isinstance(settings["close_on_play"], bool):
                    with open(Config.get_path() + "/Nox Launcher/settings/settings.json", "w") as f:
                        json.dump(META, f, indent= 4)

        with open(Config.get_path() + "/Nox Launcher/settings/settings.json", "r") as f:

            settings = json.load(f)

            if not isinstance(settings["java"]["path"], str):
                showinfo("Nox Launcher", "Java is not installed. Please be patient while it is being installed. Don`t close app.", type= "ok")
                jdk.install("21", operating_system= jdk.OperatingSystem.LINUX, arch= jdk.Architecture.X64, path= Config.get_path() + "/Nox Launcher/java/")

                with open(Config.get_path() + "/Nox Launcher/settings/settings.json", "r") as f:

                    settings = json.load(f)
                    settings["java"].update({
                        "path": jdk.shutil.which("java"),
                        "args": ["-Xms1G", f"-Xmx{Config.get_memory_ram()}M"]
                    })

                    with open(Config.get_path() + "/Nox Launcher/settings/settings.json", "w") as f:
                        json.dump(settings, f, indent= 4)

    def get_java_info() -> List[str] | bool: 

        if os.path.exists(Config.get_path() + "/Nox Launcher/settings/settings.json"):
            with open(Config.get_path() + "/Nox Launcher/settings/settings.json", "r") as f:

                settings = json.load(f)

                if "java" not in settings: return False
                elif "path" not in settings["java"] or "args" not in settings["java"]: return False
                        
                return [settings["java"]["path"], settings["java"]["args"]]
                        
    def get_memory_ram() -> int: return round(0.40 * psutil.virtual_memory().total / (1024 ** 2))

    def get_java_list() -> List[flet.dropdown.Option]:

        match platform.system():
            case "Windows": 

                if not os.path.exists(Config.get_path() + "/Nox Launcher/java/"): Config.check()

                options: List[flet.dropdown.Option] = [flet.dropdown.Option("System")]

                if len(os.listdir(Config.get_path() + "/Nox Launcher/java/")) > 0:

                    for java in [java for java in os.listdir(Config.get_path() + "/Nox Launcher/java/") if os.path.isdir(Config.get_path() + "/Nox Launcher/java/" + java)]:
                        
                        if os.path.exists(Config.get_path() + "/Nox Launcher/java/" + java + "/bin/java") and os.path.isfile(Config.get_path() + "/Nox Launcher/java/" + java + "/bin/java"):
                            options.append(flet.dropdown.Option(Config.get_path() + "/Nox Launcher/java/" + java + "/bin/java"))
                        
                for java_one, java_two in itertools.zip_longest(
                    [java for java in os.listdir("C:/Program Files (x86)/") if os.path.exists("C:/Program Files (x86)/" + java + "/bin/java.exe")], 
                    [java for java in os.listdir("C:/Program Files/") if os.path.exists("C:/Program Files/" + java + "/bin/java.exe")], 
                    fillvalue= None
                ): 
                    if java_one is not None: options.append(flet.dropdown.Option("C:/Program Files (x86)/" + java_one + "/bin/java.exe"))
                    if java_two is not None: options.append(flet.dropdown.Option("C:/Program Files/" + java_two + "/bin/java.exe"))

                return options
            
            case "Linux":

                if not os.path.exists(Config.get_path() + "/Nox Launcher/java/"): Config.check()

                options: List[flet.dropdown.Option] = [flet.dropdown.Option("System")]

                if len(os.listdir(Config.get_path() + "/Nox Launcher/java/")) > 0: 

                    for java in [java for java in os.listdir(Config.get_path() + "/Nox Launcher/java/") if os.path.isdir(Config.get_path() + "/Nox Launcher/java/" + java)]:

                        if os.path.exists(Config.get_path() + "/Nox Launcher/java/" + java + "/bin/java") and os.path.isfile(Config.get_path() + "/Nox Launcher/java/" + java + "/bin/java"):
                            options.append(flet.dropdown.Option(Config.get_path() + "/Nox Launcher/java/" + java + "/bin/java"))

                for java in [java for java in os.listdir("/usr/lib/jvm/") if os.path.isdir("/usr/lib/jvm/" + java)]:

                    if os.path.exists("/usr/lib/jvm/" + java + "/bin/java") and os.path.isfile("/usr/lib/jvm/" + java + "/bin/java"):
                        options.append(flet.dropdown.Option("/usr/lib/jvm/" + java + "/bin/java"))

                return options
    
    def parse_memory(args: List[str]) -> int: 
        for arg in [arg for arg in args if isinstance(arg, str)]:
            if arg.startswith("-Xmx") and arg.find("M") != -1 and arg.index("M") == len(arg) - 1: return int(arg.replace("-Xmx", "").replace("M", ""))
        else: return 2048

    def determinate_java_path(path: str) -> str: 

        match platform.system():
            case "Windows": 
                
                # HAY QUE ARREGLAR ESTO EN WINDOWS.
                
                parsed_path: List[str] = [path for path in path.split("\\") if path != ""]

                if len(parsed_path) <= 4 and parsed_path[1] == "bin": return "System"
                elif parsed_path[1] == "Program Files" or parsed_path[1] == "Program Files (x86)": return path

            case "Linux":
                parsed_path: List[str] = [path for path in path.split("/") if path != ""]   

                if len(parsed_path) <= 4 and parsed_path[1] == "bin": return "System"
                elif [parsed_path[0], parsed_path[1], parsed_path[2]] == ["usr", "lib", "jvm"]: return path

    def update_java_memory_dedicated(args: List[str], alloc: int) -> List[str]:

        for arg in [arg for arg in args if isinstance(arg, str)]:
            if arg.startswith("-Xmx") and arg.find("M") != -1 and arg.index("M") == len(arg) - 1:
                new_arg = "-Xmx" + str(alloc) + "M"
                args.insert(args.index(arg), new_arg)
                args.remove(arg)

        if not os.path.exists(Config.get_path() + "/Nox Launcher/settings/settings.json"): Config.check()

        with open(Config.get_path() + "/Nox Launcher/settings/settings.json", "r") as f:

            settings = json.load(f)
            settings["java"]["args"] = args

            with open(Config.get_path() + "/Nox Launcher/settings/settings.json", "w") as f:
                json.dump(settings, f, indent= 4)

        return args
    
    def update_java_path(path: str) -> None:
    
        if not os.path.exists(Config.get_path() + "/Nox Launcher/settings/settings.json"): Config.check()

        with open(Config.get_path() + "/Nox Launcher/settings/settings.json", "r") as f:

            settings = json.load(f)
            settings["java"]["path"] = path

            with open(Config.get_path() + "/Nox Launcher/settings/settings.json", "w") as f:
                json.dump(settings, f, indent= 4)

    def get_path() -> str:
        match platform.system():
            case "Windows": return os.environ.get("APPDATA")
            case "Linux": return os.environ.get("HOME")