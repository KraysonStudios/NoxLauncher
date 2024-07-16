try:

    import os
    import json
    import jdk
    import itertools
    import psutil
    import flet
    import platform

    from functools import cache
    from tkinter.messagebox import showinfo
    from typing import Any, Dict, List

except Exception as e: raise Exception(f"Report this error to the developers: \n{e.args[0]}\n")

class Config:

    def repair() -> None:

        if not os.path.exists(Config.get_path() + "/NoxLauncher"): os.mkdir(Config.get_path() + "/NoxLauncher/")
        if not os.path.exists(Config.get_path() + "/NoxLauncher/java"): os.mkdir(Config.get_path() + "/NoxLauncher/java/")
        if not os.path.exists(Config.get_path() + "/NoxLauncher/cache"): os.mkdir(Config.get_path() + "/NoxLauncher/cache/")

        if not os.path.exists(Config.get_path() + "/NoxLauncher/cache/minecraft_news.json"):
            with open(Config.get_path() + "/NoxLauncher/cache/minecraft_news.json", "w", encoding= "utf-8") as f:
                json.dump({
                    "news": [],
                    "requested": ""
                }, f, indent= 4)

        if not os.path.exists(Config.get_path() + "/NoxLauncher/launcher_profiles.json"):
            with open(Config.get_path() + "/NoxLauncher/launcher_profiles.json", "w", encoding= "utf-8") as f:
                json.dump({
                    "profiles" : {},                  
                    "settings": {
                        "enableAdvanced": False,
                        "profileSorting": "byName"
                    },
                    "version": 3
                }, f, indent= 4)

        if not os.path.exists(Config.get_path() + "/NoxLauncher/settings"):
            os.mkdir(Config.get_path() + "/NoxLauncher/settings/")
            os.mkdir(Config.get_path() + "/NoxLauncher/settings/profiles/")

            with open(Config.get_path() + "/NoxLauncher/settings/settings.json", "w", encoding= "utf-8") as f:
                json.dump({
                    "java": {},
                    "close-when-playing": True
                }, f, indent= 4)

        if not os.path.exists(Config.get_path() + "/NoxLauncher/settings/profiles"):
            os.mkdir(Config.get_path() + "/NoxLauncher/settings/profiles/")

        if not os.path.exists(Config.get_path() + "/NoxLauncher/settings/profiles/profiles.json"):
            with open(Config.get_path() + "/NoxLauncher/settings/profiles/profiles.json", "w", encoding= "utf-8") as f:
                json.dump({
                    "profiles": {}
                }, f, indent= 4)

        if not os.path.exists(Config.get_path() + "/NoxLauncher/settings/settings.json"):
            with open(Config.get_path() + "/NoxLauncher/settings/settings.json", "w", encoding= "utf-8") as f:
                json.dump({
                    "java": {},
                    "close-when-playing": True
                }, f, indent= 4)

        if os.path.exists(Config.get_path() + "/NoxLauncher/launcher_profiles.json"):
            with open(Config.get_path() + "/NoxLauncher/launcher_profiles.json", "r", encoding= "utf-8") as f:

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
                    with open(Config.get_path() + "/NoxLauncher/launcher_profiles.json", "w") as f:
                        json.dump(META, f, indent= 4)

                for kp, km in itertools.zip_longest(profiles.keys(), META.keys(), fillvalue= None):

                    if kp != km:
                        with open(Config.get_path() + "/NoxLauncher/launcher_profiles.json", "w") as f:
                            json.dump(META, f, indent= 4)
                        break
                    elif "settings" in profiles.keys():

                        for k in profiles["settings"].keys():
                            if k not in META["settings"].keys():
                                with open(Config.get_path() + "/NoxLauncher/launcher_profiles.json", "w") as f:
                                    json.dump(META, f, indent= 4)
                                break
                            
                            for vp, vm in itertools.zip_longest(profiles["settings"].values(), META["settings"].values(), fillvalue= None):
                                if vp != vm:
                                    with open(Config.get_path() + "/NoxLauncher/launcher_profiles.json", "w") as f:
                                        json.dump(META, f, indent= 4)
                                    break

        if os.path.exists(Config.get_path() + "/NoxLauncher/settings/settings.json"):
            with open(Config.get_path() + "/NoxLauncher/settings/settings.json", "r", encoding= "utf-8") as f:

                settings = json.load(f)

                META: Dict[str, Any] = {
                    "java": {
                        "path": jdk.shutil.which("java"),
                        "args": ["-Xms1G", f"-Xmx{Config.get_idiomatic_alloc_ram()}M"]
                    },
                    "close-when-playing": True,
                    "debug": True
                }

                if len(settings.keys()) != len(META.keys()):
                    with open(Config.get_path() + "/NoxLauncher/settings/settings.json", "w", encoding= "utf-8") as f:
                        json.dump(META, f, indent= 4)
                elif not "close-when-playing" in settings:
                    with open(Config.get_path() + "/NoxLauncher/settings/settings.json", "w", encoding= "utf-8") as f:
                        json.dump(META, f, indent= 4)
                elif not "debug" in settings:
                    with open(Config.get_path() + "/NoxLauncher/settings/settings.json", "w", encoding= "utf-8") as f:
                        json.dump(META, f, indent= 4)
                elif not "java" in settings:
                    with open(Config.get_path() + "/NoxLauncher/settings/settings.json", "w", encoding= "utf-8") as f:
                        json.dump(META, f, indent= 4)
                elif not isinstance(settings["java"], dict):
                    with open(Config.get_path() + "/NoxLauncher/settings/settings.json", "w", encoding= "utf-8") as f:
                        json.dump(META, f, indent= 4)
                elif not "path" in settings["java"] or not "args" in settings["java"]:
                    with open(Config.get_path() + "/NoxLauncher/settings/settings.json", "w", encoding= "utf-8") as f:
                        json.dump(META, f, indent= 4)
                elif not isinstance(settings["java"]["path"], str) or not isinstance(settings["java"]["args"], list):
                    with open(Config.get_path() + "/NoxLauncher/settings/settings.json", "w", encoding= "utf-8") as f:
                        json.dump(META, f, indent= 4)
                elif not isinstance(settings["close-when-playing"], bool):
                    with open(Config.get_path() + "/NoxLauncher/settings/settings.json", "w", encoding= "utf-8") as f:
                        json.dump(META, f, indent= 4)
                elif not isinstance(settings["debug"], bool):
                    with open(Config.get_path() + "/NoxLauncher/settings/settings.json", "w", encoding= "utf-8") as f:
                        json.dump(META, f, indent= 4)

        with open(Config.get_path() + "/NoxLauncher/settings/settings.json", "r") as f:

            settings = json.load(f)

            if not isinstance(settings["java"]["path"], str):
                showinfo("NoxLauncher", "Java is not installed. Please be patient while it is being installed. Don`t close app internally.", type= "ok")
                jdk.install("21", operating_system= jdk.OperatingSystem.LINUX if platform.system() == "Linux" else jdk.OperatingSystem.WINDOWS, arch= jdk.Architecture.X64, path= Config.get_path() + "/NoxLauncher/java/")

                with open(Config.get_path() + "/NoxLauncher/settings/settings.json", "r", encoding= "utf-8") as f:

                    settings = json.load(f)
                    settings["java"].update({
                        "path": jdk.shutil.which("java"),
                        "args": ["-Xms1G", f"-Xmx{Config.get_idiomatic_alloc_ram()}M"]
                    })

                    with open(Config.get_path() + "/NoxLauncher/settings/settings.json", "w", encoding= "utf-8") as f:
                        json.dump(settings, f, indent= 4)

    def get_java_info() -> List[str] | bool: 

        if os.path.exists(Config.get_path() + "/NoxLauncher/settings/settings.json"):
            with open(Config.get_path() + "/NoxLauncher/settings/settings.json", "r", encoding= "utf-8") as f:

                settings = json.load(f)

                if "java" not in settings: return False
                elif "path" not in settings["java"] or "args" not in settings["java"]: return False
                        
                return [settings["java"]["path"], settings["java"]["args"]]
                        
    def get_memory_ram() -> int: return round(0.40 * psutil.virtual_memory().total / (1024 ** 2))

    def get_idiomatic_alloc_ram() -> int:
        memory_available: int = Config.get_memory_ram()

        if memory_available <= 2048: return memory_available
        else: return round(memory_available / 2) if not round(memory_available / 2) <= 2048 else memory_available

    def get_java_list() -> List[flet.dropdown.Option]:

        match platform.system():
            case "Windows": 

                if not os.path.exists(Config.get_path() + "/NoxLauncher/java/"): Config.repair()

                options: List[flet.dropdown.Option] = [flet.dropdown.Option("System")]

                if len(os.listdir(Config.get_path() + "/NoxLauncher/java/")) > 0:

                    for java in [java for java in os.listdir(Config.get_path() + "/NoxLauncher/java/") if os.path.isdir(Config.get_path() + "/NoxLauncher/java/" + java)]:
                        
                        if os.path.exists(Config.get_path() + "/NoxLauncher/java/" + java + "/bin/java") and os.path.isfile(Config.get_path() + "/NoxLauncher/java/" + java + "/bin/java"):
                            options.append(flet.dropdown.Option(Config.get_path() + "/NoxLauncher/java/" + java + "/bin/java"))
                        
                for path_one, path_two in itertools.zip_longest(
                    [path for path in os.listdir('C:/Program Files/') if os.path.isdir('C:/Program Files/' + path)], 
                    [path for path in os.listdir('C:/Program Files (x86)/') if os.path.isdir('C:/Program Files (x86)/' + path)], 
                    fillvalue= None
                ):
                    for java_one, java_two in itertools.zip_longest(
                        [java for java in os.listdir('C:/Program Files/' + path_one) if os.path.isdir(f'C:/Program Files/{path_one}/{java}/') and java.find('jdk') != -1 and os.path.exists(f'C:/Program Files/{path_one}/{java}/bin/java.exe') and os.path.isfile(f'C:/Program Files/{path_one}/{java}/bin/java.exe')], 
                        [java for java in os.listdir('C:/Program Files (x86)/' + path_two) if os.path.isdir(f'C:/Program Files (x86)/{path_two}/{java}/') and java.find('jdk') != -1 and os.path.exists(f'C:/Program Files (x86)/{path_two}/{java}/bin/java.exe') and os.path.isfile(f'C:/Program Files (x86)/{path_two}/{java}/bin/java.exe')], 
                        fillvalue= None
                    ):
                        
                        if java_one is not None: options.append(flet.dropdown.Option(f'C:/Program Files/{path_one}/{java_one}/bin/java.exe'))
                        if java_two is not None: options.append(flet.dropdown.Option(f'C:/Program Files (x86)/{path_two}/{java_two}/bin/java.exe'))

                return options
            
            case "Linux":

                if not os.path.exists(Config.get_path() + "/NoxLauncher/java/"): Config.repair()

                options: List[flet.dropdown.Option] = [flet.dropdown.Option("System")]

                if len(os.listdir(Config.get_path() + "/NoxLauncher/java/")) > 0: 

                    for java in [java for java in os.listdir(Config.get_path() + "/NoxLauncher/java/") if os.path.isdir(Config.get_path() + "/NoxLauncher/java/" + java)]:

                        if os.path.exists(Config.get_path() + "/NoxLauncher/java/" + java + "/bin/java") and os.path.isfile(Config.get_path() + "/NoxLauncher/java/" + java + "/bin/java"):
                            options.append(flet.dropdown.Option(Config.get_path() + "/NoxLauncher/java/" + java + "/bin/java"))

                for java in [java for java in os.listdir("/usr/lib/jvm/") if os.path.isdir("/usr/lib/jvm/" + java)]:

                    if os.path.exists("/usr/lib/jvm/" + java + "/bin/java") and os.path.isfile("/usr/lib/jvm/" + java + "/bin/java"):
                        options.append(flet.dropdown.Option("/usr/lib/jvm/" + java + "/bin/java"))

                return options
            
    def get_versions_available() -> List[flet.dropdown.Option]:

        if not os.path.exists(Config.get_path() + "/NoxLauncher/"): Config.repair()
        elif not os.path.exists(Config.get_path() + "/NoxLauncher/versions/"): return [flet.dropdown.Option("Install an minecraft version!")]

        versions: List[flet.dropdown.Option] = []

        for version in [version for version in os.listdir(Config.get_path() + "/NoxLauncher/versions/") if os.path.isdir(Config.get_path() + "/NoxLauncher/versions/" + version)]:

            if os.path.exists(Config.get_path() + "/NoxLauncher/versions/" + f"{version}/{version}.jar") and os.path.isfile(Config.get_path() + "/NoxLauncher/versions/" + f"{version}/{version}.jar"):
                versions.append(flet.dropdown.Option(version))

        if len(versions) == 0: return [flet.dropdown.Option("Install an minecraft version!")]
        else: return versions
            
    def get_close_when_playing() -> bool: 

        if not os.path.exists(Config.get_path() + "/NoxLauncher/settings/settings.json"): Config.repair()

        with open(Config.get_path() + "/NoxLauncher/settings/settings.json", "r", encoding= "utf-8") as f:

            settings = json.load(f)

            if "close-when-playing" not in settings: return False
            elif not isinstance(settings["close-when-playing"], bool): return False
            else: return settings["close-when-playing"]

    def update_close_when_playing(value: bool) -> None:

        if not os.path.exists(Config.get_path() + "/NoxLauncher/settings/settings.json"): Config.repair()

        with open(Config.get_path() + "/NoxLauncher/settings/settings.json", "r", encoding= "utf-8") as f:

            settings = json.load(f)
            settings["close-when-playing"] = value

            with open(Config.get_path() + "/NoxLauncher/settings/settings.json", "w") as f:
                json.dump(settings, f, indent= 4)

    def get_debug_mode() -> bool: 

        if not os.path.exists(Config.get_path() + "/NoxLauncher/settings/settings.json"): Config.repair()

        with open(Config.get_path() + "/NoxLauncher/settings/settings.json", "r", encoding= "utf-8") as f:

            settings = json.load(f)

            if "debug" not in settings: return False
            elif not isinstance(settings["debug"], bool): return False
            else: return settings["debug"]

    def update_debug_mode(value: bool) -> None:

        if not os.path.exists(Config.get_path() + "/NoxLauncher/settings/settings.json"): Config.repair()

        with open(Config.get_path() + "/NoxLauncher/settings/settings.json", "r", encoding= "utf-8") as f:

            settings = json.load(f)
            settings["debug"] = value

            with open(Config.get_path() + "/NoxLauncher/settings/settings.json", "w", encoding= "utf-8") as f:
                json.dump(settings, f, indent= 4)
    
    def parse_memory(args: List[str]) -> int: 
        for arg in [arg for arg in args if isinstance(arg, str)]:
            if arg.startswith("-Xmx") and arg.find("M") != -1 and arg.index("M") == len(arg) - 1: return int(arg.replace("-Xmx", "").replace("M", ""))
        else: return 2048

    def get_java_version(path: str) -> str:
        
        for direct in [path for path in path.split("/") if path != ""]: 
            if direct.find(".") != -1 or direct.find("-") != -1: return direct if len(direct) <= 20 else direct[:19] + "..."
        else: return "Undetermined"

    def determinate_java_path(path: str) -> str: 

        match platform.system():
            case "Windows": 
                
                parsed_path: List[str] = [path for path in path.split("\\") if path != ""]

                if len(parsed_path) <= 4 and parsed_path[1] == "bin": return "System"
                elif parsed_path[1] == "Program Files" or parsed_path[1] == "Program Files (x86)": return path

            case "Linux":
                parsed_path: List[str] = [path for path in path.split("/") if path != ""]   

                if len(parsed_path) <= 4 and parsed_path[1] == "bin": return "System"
                elif [parsed_path[0], parsed_path[1], parsed_path[2]] == ["usr", "lib", "jvm"]: return path

    def update_java_memory_allocated(args: List[str], alloc: int) -> List[str]:

        for arg in [arg for arg in args if isinstance(arg, str)]:
            if arg.startswith("-Xmx") and arg.find("M") != -1 and arg.index("M") == len(arg) - 1:
                new_arg = "-Xmx" + str(alloc) + "M"
                args.insert(args.index(arg), new_arg)
                args.remove(arg)

        if not os.path.exists(Config.get_path() + "/NoxLauncher/settings/settings.json"): Config.repair()

        with open(Config.get_path() + "/NoxLauncher/settings/settings.json", "r", encoding= "utf-8") as f:

            settings = json.load(f)
            settings["java"]["args"] = args

            with open(Config.get_path() + "/NoxLauncher/settings/settings.json", "w", encoding= "utf-8") as f:
                json.dump(settings, f, indent= 4)

        return args
    
    def update_java_path(path: str) -> None:
    
        if not os.path.exists(Config.get_path() + "/NoxLauncher/settings/settings.json"): Config.repair()

        with open(Config.get_path() + "/NoxLauncher/settings/settings.json", "r", encoding= "utf-8") as f:

            settings = json.load(f)
            settings["java"]["path"] = path

            with open(Config.get_path() + "/NoxLauncher/settings/settings.json", "w", encoding= "utf-8") as f:
                json.dump(settings, f, indent= 4)

    @cache
    def get_path() -> str:
        match platform.system():
            case "Windows": return os.environ.get("APPDATA")
            case "Linux": return os.environ.get("HOME")