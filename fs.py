import flet
import platform
import subprocess
import os
import json
import psutil
import shutil
import datetime
import gzip
import requests
import minecraft_launcher_lib

from typing import List
from functools import cache, lru_cache

from constants import VERSION

@cache
def check_noxlauncher_filesystem() -> None:
    
    if not os.path.exists(get_home()): os.mkdir(get_home())
    if not os.path.exists(get_home() + "/mods"): os.mkdir(get_home() + "/mods")
    if not os.path.exists(get_home() + "/languages"): os.mkdir(get_home() + "/languages")
    
    if not os.path.exists(get_home() + "/accounts.json"): 

        with open(get_home() + "/accounts.json", "w") as file: 

            json.dump({
                "premium": [],
                "nopremium": [],
                "version": VERSION
            }, file, indent= 4)

    if not os.path.exists(get_home() + "/config.json"): 

        with open(get_home() + "/config.json", "w") as file: 

            json.dump({
                "java": "",
                "jvm-args": ["-Xms1G", "-Xmx2G", "-Djava.net.preferIPv4Stack=true"],
                "autoclose": True,
                "receivenews": True,
                "discordrpc": True,
                "version": VERSION
            }, file, indent= 4)

    ConfigChecker(get_home() + "/config.json").check_and_repair()

    if not os.path.exists(get_home() + "/launcher_profiles.json"):

        with open(get_home() + "/launcher_profiles.json", "w") as file: 
            json.dump({
                "profiles": {},
                "settings": {
                    "enableAdvanced": False,
                    "profileSorting": "byName"
                },
                "version": 3
            }, file, indent= 4)

    if not os.path.exists(get_home() + "/versions"): os.mkdir(get_home() + "/versions")
    if not os.path.exists(get_home() + "/versions/vanilla.json"): 

        with open(get_home() + "/versions/vanilla.json", "w") as file: 

            json.dump({
                "versions": {
                    "releases": [version["id"] for version in minecraft_launcher_lib.utils.get_version_list() if version["type"] == "release"] if has_internet() else [],
                    "snapshots": [version["id"] for version in minecraft_launcher_lib.utils.get_version_list() if version["type"] == "snapshot"] if has_internet() else []
                },
                "updated": datetime.datetime.strftime(datetime.datetime.now(datetime.UTC), "%Y-%m-%d"),
                "version": VERSION
            }, file, indent= 4)
    
    with open(get_home() + "/versions/vanilla.json", "r") as file:

        vanilla = json.load(file)

        if datetime.datetime.strftime(datetime.datetime.now(datetime.UTC), "%Y-%m-%d") != vanilla["updated"] and has_internet():
            
            with open(get_home() + "/versions/vanilla.json", "w") as file:

                json.dump({
                    "versions": {
                        "releases": [version["id"] for version in minecraft_launcher_lib.utils.get_version_list() if version["type"] == "release"],
                        "snapshots": [version["id"] for version in minecraft_launcher_lib.utils.get_version_list() if version["type"] == "snapshot"]
                    },
                    "updated": datetime.datetime.strftime(datetime.datetime.now(datetime.UTC), "%Y-%m-%d"),
                    "version": VERSION
                }, file, indent= 4)

    if not os.path.exists(get_home() + "/versions/fabric.json"): 

        with open(get_home() + "/versions/fabric.json", "w") as file: 

            json.dump({
                "versions": {
                    "releases": [version["version"] for version in minecraft_launcher_lib.fabric.get_all_minecraft_versions() if version["stable"]] if has_internet() else [], 
                    "snapshots": [version["version"] for version in minecraft_launcher_lib.fabric.get_all_minecraft_versions() if version["stable"] == False] if has_internet() else [],
                },
                "updated": datetime.datetime.strftime(datetime.datetime.now(datetime.UTC), "%Y-%m-%d"),
                "version": VERSION
            }, file, indent= 4)

    with open(get_home() + "/versions/fabric.json", "r") as file:

        fabric = json.load(file)

        if datetime.datetime.strftime(datetime.datetime.now(datetime.UTC), "%Y-%m-%d") != fabric["updated"] and has_internet():
            
            with open(get_home() + "/versions/fabric.json", "w") as file:

                json.dump({
                    "versions": {
                        "releases": [version["version"] for version in minecraft_launcher_lib.fabric.get_all_minecraft_versions() if version["stable"]],
                        "snapshots": [version["version"] for version in minecraft_launcher_lib.fabric.get_all_minecraft_versions() if version["stable"] == False],
                    },
                    "updated": datetime.datetime.strftime(datetime.datetime.now(datetime.UTC), "%Y-%m-%d"),
                    "version": VERSION
                }, file, indent= 4)

    if not os.path.exists(get_home() + "/versions/forge.json"): 

        with open(get_home() + "/versions/forge.json", "w") as file: 

            json.dump({
                "versions": minecraft_launcher_lib.forge.list_forge_versions() if has_internet() else [],
                "updated": datetime.datetime.strftime(datetime.datetime.now(datetime.UTC), "%Y-%m-%d"),
                "version": VERSION
            }, file, indent= 4)

    with open(get_home() + "/versions/forge.json", "r") as file:

        forge = json.load(file)

        if datetime.datetime.strftime(datetime.datetime.now(datetime.UTC), "%Y-%m-%d") != forge["updated"] and has_internet():
            
            with open(get_home() + "/versions/forge.json", "w") as file:

                json.dump({
                    "versions": minecraft_launcher_lib.forge.list_forge_versions(),
                    "updated": datetime.datetime.strftime(datetime.datetime.now(datetime.UTC), "%Y-%m-%d"),
                    "version": VERSION
                }, file, indent= 4)

def get_home() -> str:

    match platform.system():

        case "Windows": return os.environ.get("APPDATA") + "/NoxLauncher" 
        case "Linux": return os.environ.get("HOME") + "/NoxLauncher"

def open_home(_: flet.ControlEvent) -> None:

    check_noxlauncher_filesystem()

    match platform.system():

        case "Windows": subprocess.call("start explorer .", shell= True, cwd= f"{get_home()}/", stderr= subprocess.DEVNULL, stdout= subprocess.DEVNULL, stdin= subprocess.DEVNULL)
        case "Linux": subprocess.call("nohup xdg-open .", shell= True, cwd= f"{get_home()}/", stderr= subprocess.DEVNULL, stdout= subprocess.DEVNULL, stdin= subprocess.DEVNULL)

def get_all_java_instances() -> List[flet.dropdown.Option]:

    check_noxlauncher_filesystem()

    options: List[flet.dropdown.Option] = [flet.dropdown.Option("System", text_style= flet.TextStyle(font_family= "NoxLauncher", size= 14))]

    options.extend([flet.dropdown.Option(instance, text_style= flet.TextStyle(font_family= "NoxLauncher", size= 14)) for instance in minecraft_launcher_lib.java_utils.find_system_java_versions()])

    return options
        
def get_current_java_instance() -> str | None:

    check_noxlauncher_filesystem()

    with open(get_home() + "/config.json", "r") as file: 

        data = json.load(file)

        if "java" not in data: return get_system_java_instance()
        elif data["java"] == "System" or data["java"] == "" or data["java"].isspace(): return get_system_java_instance()

        return data["java"]
    
def get_system_java_instance() -> str | None:

    which: str | None = shutil.which("java")
    
    return None if which is None else which
    
def get_current_jvm_args() -> List[str]:

    check_noxlauncher_filesystem()

    with open(get_home() + "/config.json", "r") as file: 

        data = json.load(file)

        return data["jvm-args"] if "jvm-args" in data else ["-Xms1G", "-Xmx2G", "-Djava.net.preferIPv4Stack=true"]
    
def update_jvm_args(args: List[str]) -> None:

    check_noxlauncher_filesystem()

    with open(get_home() + "/config.json", "r") as file: 

        data = json.load(file)

        data["jvm-args"] = args

    with open(get_home() + "/config.json", "w") as file: json.dump(data, file, indent= 4)

def update_java(java: str) -> None:

    check_noxlauncher_filesystem()

    with open(get_home() + "/config.json", "r") as file: 

        data = json.load(file)

        data["java"] = java

    with open(get_home() + "/config.json", "w") as file: json.dump(data, file, indent= 4)

def update_autoclose(close: bool) -> None:

    check_noxlauncher_filesystem()

    with open(get_home() + "/config.json", "r") as file: 

        data = json.load(file)

        data["autoclose"] = close

    with open(get_home() + "/config.json", "w") as file: json.dump(data, file, indent= 4)

def get_autoclose() -> bool:

    check_noxlauncher_filesystem()

    with open(get_home() + "/config.json", "r") as file: 

        data = json.load(file)

        if "autoclose" not in data: data["autoclose"] = True

        return data["autoclose"]
    
def get_receivenews() -> bool:

    check_noxlauncher_filesystem()

    with open(get_home() + "/config.json", "r") as file: 

        data = json.load(file)

        if "receivenews" not in data: data["receivenews"] = True

        return data["receivenews"]
    
def update_receivenews(receive: bool) -> None:

    check_noxlauncher_filesystem()

    with open(get_home() + "/config.json", "r") as file: 

        data = json.load(file)

        data["receivenews"] = receive

    with open(get_home() + "/config.json", "w") as file: json.dump(data, file, indent= 4)

def get_discordrpc() -> bool:

    check_noxlauncher_filesystem()

    with open(get_home() + "/config.json", "r") as file: 

        data = json.load(file)

        if "discordrpc" not in data: data["discordrpc"] = True

        return data["discordrpc"]
    
def update_discordrpc(rpc: bool) -> None:

    check_noxlauncher_filesystem()

    with open(get_home() + "/config.json", "r") as file: 

        data = json.load(file)

        data["discordrpc"] = rpc

    with open(get_home() + "/config.json", "w") as file: json.dump(data, file, indent= 4)

def get_fabric_releases() -> List[flet.dropdown.Option]: 

    check_noxlauncher_filesystem()

    with open(get_home() + "/versions/fabric.json", "r") as file: 

        data = json.load(file)

        if "versions" not in data: return [flet.dropdown.Option("No Fabric Releases Found")]
        elif "releases" not in data["versions"]: return [flet.dropdown.Option("No Fabric Releases Found")]

        return [flet.dropdown.Option(release, text_style= flet.TextStyle(font_family= "NoxLauncher", size= 14)) for release in data["versions"]["releases"]]
    
def get_forge_versions() -> List[flet.dropdown.Option]:

    check_noxlauncher_filesystem()

    with open(get_home() + "/versions/forge.json", "r") as file: 

        data = json.load(file)

        if "versions" not in data: return [flet.dropdown.Option("No Forge Versions Found")]

        return [flet.dropdown.Option(version, text_style= flet.TextStyle(font_family= "NoxLauncher", size= 14)) for version in data["versions"]]

def get_fabric_snapshots() -> List[flet.dropdown.Option]:

    check_noxlauncher_filesystem()

    with open(get_home() + "/versions/fabric.json", "r") as file: 

        data = json.load(file)

        if "versions" not in data: return [flet.dropdown.Option("No Fabric Snapshots Found")]
        elif "snapshots" not in data["versions"]: return [flet.dropdown.Option("No Fabric Snapshots Found")]

        return [flet.dropdown.Option(snapshot, text_style= flet.TextStyle(font_family= "NoxLauncher", size= 14)) for snapshot in data["versions"]["snapshots"]]
    
def get_vanilla_releases() -> List[flet.dropdown.Option]: 

    check_noxlauncher_filesystem()

    with open(get_home() + "/versions/vanilla.json", "r") as file: 

        data = json.load(file)

        if "versions" not in data: return [flet.dropdown.Option("No Vanilla Releases Found")]
        elif "releases" not in data["versions"]: return [flet.dropdown.Option("No Vanilla Releases Found")]

        return [flet.dropdown.Option(release, text_style= flet.TextStyle(font_family= "NoxLauncher", size= 14)) for release in data["versions"]["releases"]]
    
def get_vanilla_snapshots() -> List[flet.dropdown.Option]:

    check_noxlauncher_filesystem()

    with open(get_home() + "/versions/vanilla.json", "r") as file: 

        data = json.load(file)

        if "versions" not in data: return [flet.dropdown.Option("No Vanilla Snapshots Found")]
        elif "snapshots" not in data["versions"]: return [flet.dropdown.Option("No Vanilla Snapshots Found")]

        return [flet.dropdown.Option(snapshot, text_style= flet.TextStyle(font_family= "NoxLauncher", size= 14)) for snapshot in data["versions"]["snapshots"]]

def get_minecraft_versions() -> List[flet.dropdown.Option]:

    check_noxlauncher_filesystem()

    versions: List[flet.dropdown.Option] = []

    for version in os.listdir(get_home() + "/versions"):

        if os.path.exists(get_home() + "/versions/" + f"{version}/{version}.jar") and os.path.isfile(get_home() + "/versions/" + f"{version}/{version}.jar"):
            versions.append(flet.dropdown.Option(version, text_style= flet.TextStyle(font_family= "NoxLauncher", size= 14)))

    return versions

def get_mc_logs() -> List[flet.Text]: 

    check_noxlauncher_filesystem()

    logs: List[flet.Text] = []

    if not os.path.exists("logs"): return []

    for log in os.listdir("logs"):

        if os.path.exists(f"logs/{log}") and os.path.isfile(f"logs/{log}") and log.endswith(".log.gz"):

            with gzip.open(f"logs/{log}", "rb") as file: logs.append(flet.Text(file.read().decode("utf-8"), style= flet.TextStyle(font_family= "NoxLauncher", size= 14)))

    if os.path.exists("logs/latest.log"): 
        
        with open("logs/latest.log", "r") as file: logs.insert(len(logs), flet.Text(file.read(), style= flet.TextStyle(font_family= "NoxLauncher", size= 14)))

    return logs

def get_theme() -> str:

    check_noxlauncher_filesystem()

    with open(get_home() + "/config.json", "r") as file:

        data = json.load(file)

        if "customization" not in data: 
            ConfigChecker(get_home() + "/config.json").check_and_repair()
            return "Dark"
        
        if "theme" not in data["customization"]: 
            ConfigChecker(get_home() + "/config.json").check_and_repair()
            return "Dark"

        return data["customization"]["theme"]
    
def get_titlescolor() -> str: 

    check_noxlauncher_filesystem()

    with open(get_home() + "/config.json", "r") as file:

        data = json.load(file)

        if "customization" not in data: 
            ConfigChecker(get_home() + "/config.json").check_and_repair()
            return "#FFFFFF"

        if "titles-color" not in data["customization"]: 
            ConfigChecker(get_home() + "/config.json").check_and_repair()
            return "#FFFFFF"

        return data["customization"]["titles-color"]
    
def update_titlescolor(color: str) -> None:

    check_noxlauncher_filesystem()

    with open(get_home() + "/config.json", "r") as file: 

        data = json.load(file)

        if "customization" not in data: 
            ConfigChecker(get_home() + "/config.json").check_and_repair()
            return

        data["customization"]["titles-color"] = color

    with open(get_home() + "/config.json", "w") as file: json.dump(data, file, indent= 4)
    
def get_subtitlescolor() -> str: 

    check_noxlauncher_filesystem()

    with open(get_home() + "/config.json", "r") as file:

        data = json.load(file)

        if "customization" not in data: 
            ConfigChecker(get_home() + "/config.json").check_and_repair()
            return "#717171"

        if "titles-color" not in data["customization"]: 
            ConfigChecker(get_home() + "/config.json").check_and_repair()
            return "#717171"

        return data["customization"]["subtitles-color"]
        
    
def update_subtitlescolor(color: str) -> None:

    check_noxlauncher_filesystem()

    with open(get_home() + "/config.json", "r") as file: 

        data = json.load(file)

        if "customization" not in data: 
            ConfigChecker(get_home() + "/config.json").check_and_repair()
            return

        data["customization"]["subtitles-color"] = color

    with open(get_home() + "/config.json", "w") as file: json.dump(data, file, indent= 4)

def get_bgcolor() -> str: 

    check_noxlauncher_filesystem()

    with open(get_home() + "/config.json", "r") as file:

        data = json.load(file)

        if "customization" not in data: 
            ConfigChecker(get_home() + "/config.json").check_and_repair()
            return "#272727"

        if "bg-color" not in data["customization"]: 
            ConfigChecker(get_home() + "/config.json").check_and_repair()
            return "#272727"

        return data["customization"]["bg-color"]
    
def update_bgcolor(color: str) -> None:

    check_noxlauncher_filesystem()

    with open(get_home() + "/config.json", "r") as file: 

        data = json.load(file)

        if "customization" not in data: 
            ConfigChecker(get_home() + "/config.json").check_and_repair()
            return

        data["customization"]["bg-color"] = color

    with open(get_home() + "/config.json", "w") as file: json.dump(data, file, indent= 4)
    
def get_filledcolor() -> str: 

    check_noxlauncher_filesystem()

    with open(get_home() + "/config.json", "r") as file:

        data = json.load(file)

        if "customization" not in data: 
            ConfigChecker(get_home() + "/config.json").check_and_repair()
            return "#148b47"

        if "filled-color" not in data["customization"]: 
            ConfigChecker(get_home() + "/config.json").check_and_repair()
            return "#148b47"

        return data["customization"]["filled-color"]
    
def update_filledcolor(color: str) -> None:

    check_noxlauncher_filesystem()

    with open(get_home() + "/config.json", "r") as file: 

        data = json.load(file)

        if "customization" not in data: 
            ConfigChecker(get_home() + "/config.json").check_and_repair()
            return

        data["customization"]["filled-color"] = color

    with open(get_home() + "/config.json", "w") as file: json.dump(data, file, indent= 4)

def update_theme(theme: str) -> None:

    check_noxlauncher_filesystem()

    with open(get_home() + "/config.json", "r") as file: 

        data = json.load(file)

        if "customization" not in data: 
            ConfigChecker(get_home() + "/config.json").check_and_repair()
            return

        data["customization"]["theme"] = theme

    with open(get_home() + "/config.json", "w") as file: json.dump(data, file, indent= 4)

@lru_cache          
def get_available_memory_ram() -> int: return round(0.60 * psutil.virtual_memory().total / (1024 ** 2))

def parse_memory(args: List[str]) -> int: 
    for arg in [arg for arg in args if isinstance(arg, str)]:
        if arg.startswith("-Xmx") and arg.find("M") != -1 and arg.index("M") == len(arg) - 1: return int(arg.replace("-Xmx", "").replace("M", ""))
    else: return 2048

@cache
def has_internet() -> bool:

    try:
        return requests.get("https://google.com", timeout= 20).ok
    except:
        return False
    
class ConfigChecker:

    def __init__(self, path: str) -> None:

        self.path: str = path
        self.keys: List[str] = [
            "java",
            "jvm-args",
            "autoclose",
            "receivenews",
            "discordrpc",
            "customization",
            "version"
        ]

        self.customization_keys: List[str] = [
            "titles-color",
            "subtitles-color",
            "bg-color",
            "filled-color",
            "theme"
        ]

    def check_and_repair(self):

        if not os.path.exists(self.path): check_noxlauncher_filesystem()

        with open(self.path, "r") as file: data = json.load(file)
            
        for key in self.keys: 
            if key not in data.keys(): 
                match key:
                    case "customization": data[key] = {
                        "titles-color": "#FFFFFF",
                        "subtitles-color": "#717171",
                        "bg-color": "#272727",
                        "filled-color": "#148b47",
                        "theme": "Dark"
                    }
                    case "version": data[key] = VERSION
                    case "java": data[key] = get_system_java_instance()
                    case "jvm-args": data[key] = ["-Xms1G", "-Xmx2G", "-Djava.net.preferIPv4Stack=true"]
                    case "autoclose": data[key] = True
                    case "receivenews": data[key] = True
                    case "discordrpc": data[key] = True

            match key:

                case "customization":
    
                    if not isinstance(data[key], dict):

                        data[key] = {
                            "titles-color": "#FFFFFF",
                            "subtitles-color": "#717171",
                            "bg-color": "#272727",
                            "filled-color": "#148b47",
                            "theme": "Dark"
                        }

                    for valid_key in self.customization_keys:
                        if valid_key not in data[key].keys():
                            match valid_key:
                                case "titles-color": data["customization"][valid_key] = "#FFFFFF"
                                case "subtitles-color": data["customization"][valid_key] = "#717171"
                                case "bg-color": data["customization"][valid_key] = "#272727"
                                case "filled-color": data["customization"][valid_key] = "#148b47"
                                case "theme": data["customization"][valid_key] = "Dark"

        with open(self.path, "w") as file: json.dump(data, file, indent= 4)

