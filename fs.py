import flet
import platform
import subprocess
import os
import json
import itertools
import psutil
import shutil
import datetime
import minecraft_launcher_lib

from typing import List
from functools import cache

from logs import error
from constants import VERSION
from utils import has_internet

@cache
def check_noxlauncher_filesystem() -> None:
    
    if not os.path.exists(get_home()): os.mkdir(get_home())
    if not os.path.exists(get_home() + "/mods"): os.mkdir(get_home() + "/mods")
    if not os.path.exists(get_home() + "/accounts.json"): 

        with open(get_home() + "/accounts.json", "w") as file: 

            json.dump({
                "premium": [],
                "free": [],
                "nopremium": [],
                "version": VERSION
            }, file, indent= 4)

    if not os.path.exists(get_home() + "/config.json"): 

        with open(get_home() + "/config.json", "w") as file: 

            json.dump({
                "java": "",
                "jvm-args": ["-Xms1G", f"-Xmx{get_idiomatic_memory_ram()}M"],
                "autoclose": True,
                "receivenews": True,
                "discordrpc": True,
                "version": VERSION
            }, file, indent= 4)

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

    match platform.system():
        case "Windows": 

            try:
                    
                for path_one, path_two in itertools.zip_longest(
                    [path for path in os.listdir('C:/Program Files/') if os.path.isdir('C:/Program Files/' + path)], 
                    [path for path in os.listdir('C:/Program Files (x86)/') if os.path.isdir('C:/Program Files (x86)/' + path)], 
                    fillvalue= None
                ):
                    for java_one, java_two in itertools.zip_longest(
                        [java for java in os.listdir('C:/Program Files/' + path_one) if os.path.isdir(f'C:/Program Files/{path_one}/{java}/') and java.find('jdk') != -1 and os.path.exists(f'C:/Program Files/{path_one}/{java}/bin/java.exe') and os.path.isfile(f'C:/Program Files/{path_one}/{java}/bin/java.exe')] if path_one is not None else [], 
                        [java for java in os.listdir('C:/Program Files (x86)/' + path_two) if os.path.isdir(f'C:/Program Files (x86)/{path_two}/{java}/') and java.find('jdk') != -1 and os.path.exists(f'C:/Program Files (x86)/{path_two}/{java}/bin/java.exe') and os.path.isfile(f'C:/Program Files (x86)/{path_two}/{java}/bin/java.exe')] if path_two is not None else [], 
                        fillvalue= None
                    ):
                        
                        if java_one is not None and path_one is not None: options.append(flet.dropdown.Option(f'C:/Program Files/{path_one}/{java_one}/bin/java.exe', text_style= flet.TextStyle(font_family= "NoxLauncher", size= 14)))
                        if java_two is not None and path_two is not None: options.append(flet.dropdown.Option(f'C:/Program Files (x86)/{path_two}/{java_two}/bin/java.exe', text_style= flet.TextStyle(font_family= "NoxLauncher", size= 14)))

            except Exception as e: error(f"Failed to get all java instances: {e}")

            return options
        
        case "Linux":

            for java in [java for java in os.listdir("/usr/lib/jvm/") if os.path.isdir("/usr/lib/jvm/" + java)]:

                if os.path.exists("/usr/lib/jvm/" + java + "/bin/java") and os.path.isfile("/usr/lib/jvm/" + java + "/bin/java"):
                    options.append(flet.dropdown.Option("/usr/lib/jvm/" + java + "/bin/java", text_style= flet.TextStyle(font_family= "NoxLauncher", size= 14)))

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

        return data["jvm-args"] if "jvm-args" in data else ["-Xms1G", f"-Xmx{get_idiomatic_memory_ram()}M"]
    
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

    if len(versions) == 0: return [flet.dropdown.Option(key= "empty", text="Install a Minecraft version first!", text_style= flet.TextStyle(font_family= "NoxLauncher", size= 14))]

    return versions

@cache            
def get_available_memory_ram() -> int: return round(0.40 * psutil.virtual_memory().total / (1024 ** 2))

@cache
def get_idiomatic_memory_ram() -> int:
    memory_available: int = get_available_memory_ram()

    if memory_available <= 2048: return memory_available
    else: return round(memory_available / 2) if not round(memory_available / 2) <= 2048 else memory_available

def parse_memory(args: List[str]) -> int: 
    for arg in [arg for arg in args if isinstance(arg, str)]:
        if arg.startswith("-Xmx") and arg.find("M") != -1 and arg.index("M") == len(arg) - 1: return int(arg.replace("-Xmx", "").replace("M", ""))
    else: return 2048