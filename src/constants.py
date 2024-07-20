try:
    import flet
    import os
    import json
    import datetime
    import minecraft_launcher_lib

    from abs import NoxLauncherDropdown
    from fs import Config
    from typing import List, Dict, Any
    from enum import Enum

except Exception as e: 
    
    print(f"Report this error to the developers: \n{e.args[0]}")
    exit(1)

def update_minecraft_news(news: Dict[str, Any]) -> None:

    for article in minecraft_launcher_lib.utils.get_minecraft_news(5).values():

        if isinstance(article, list): 
            news["news"].extend(article)
            break

    news["requested"] = datetime.datetime.strftime(datetime.datetime.now(datetime.UTC), "%Y-%m-%d")

    with open(Config.get_path() + "/NoxLauncher/cache/minecraft_news.json", "w") as f: json.dump(news, f, indent= 4)

def minecraft_news() -> List[flet.Container]:

    if not os.path.exists(Config.get_path() + "/NoxLauncher/cache/minecraft_news.json"):
        with open(Config.get_path() + "/NoxLauncher/cache/minecraft_news.json", "w", encoding= "utf-8") as f:
            json.dump({
                "news": [],
                "requested": ""
            }, f, indent= 4)

    containers: List[flet.Container] = []

    if os.path.exists(Config.get_path() + "/NoxLauncher/cache/minecraft_news.json"): 

        if datetime.datetime.now(datetime.UTC).day % 2 == 0 :

            with open(Config.get_path() + "/NoxLauncher/cache/minecraft_news.json", "r", encoding= "utf-8") as f: 

                news: Dict[str, Any] = json.load(f)

                if "news" not in news: Config.repair()
                elif "requested" not in news: Config.repair()
                elif not isinstance(news["news"], list): Config.repair()
                elif not isinstance(news["requested"], str): Config.repair()

                if news["requested"] != "" and not news["requested"].isspace():
                    if (
                        datetime.datetime.strftime(datetime.datetime.now(datetime.UTC), "%Y-%m-%d") != news["requested"] and 
                        datetime.datetime.strptime(news["requested"], "%Y-%m-%d").day != datetime.datetime.now(datetime.UTC).day
                    ): update_minecraft_news(news)

                else: update_minecraft_news(news)

        with open(Config.get_path() + "/NoxLauncher/cache/minecraft_news.json", "r", encoding= "utf-8") as f: 

            news = json.load(f)

            if "news" not in news: Config.repair()
            elif len(news["news"]) == 0: 

                with open(Config.get_path() + "/NoxLauncher/cache/minecraft_news.json", "r", encoding= "utf-8") as f: 

                    news = json.load(f)

                    if "news" not in news: Config.repair()
                    elif not isinstance(news["news"], list): Config.repair()

                    for article in minecraft_launcher_lib.utils.get_minecraft_news(1).values():

                        if isinstance(article, list): 
                            news["news"].extend(article)
                            break
                
                with open(Config.get_path() + "/NoxLauncher/cache/minecraft_news.json", "w", encoding= "utf-8") as f: json.dump(news, f, indent= 4)
            
            for article in news["news"]:
                containers.append(flet.Container(
                    content= flet.Column(controls= [
                        flet.Text(article["default_tile"]["title"], size= 15, color= "#ffffff", font_family= "Minecraft"),
                        flet.FilledButton(text= "Read", icon= flet.icons.OPEN_IN_NEW, icon_color= "#ffffff", url_target= "article", url= "https://minecraft.net" + article["article_url"], style= flet.ButtonStyle(bgcolor= "#148b47", color= "#ffffff", shape= flet.RoundedRectangleBorder(radius= 5)), width= 120, height= 40),
                    ], spacing= 8),
                    height= 180,
                    width= 180,
                    border_radius= 20,
                    opacity= 0.9,
                    blur= flet.Blur(
                        30,
                        20
                    ),
                    shadow= flet.BoxShadow(
                        1,
                        145,
                        color= "#ffffff",
                        offset= flet.Offset(0, 0)
                    ),
                    padding= flet.padding.all(20)
                ))

    return containers

class constants(Enum):

    MAX_WIDTH = 1920
    MAX_HEIGHT = 1080
    MIN_WIDTH = 900
    MIN_HEIGHT = 700
    MINECRAFT_NEWS = minecraft_news()
    VANILLA_SNAPSHOTS = NoxLauncherDropdown(label= "Vanilla Snapshots", hint_text= "Select a snapshot and install it!", options= [flet.dropdown.Option(version["id"]) for version in minecraft_launcher_lib.utils.get_version_list() if version["type"] == "snapshot"], border_color= "#717171", border_radius= 10, border_width= 2, label_style= flet.TextStyle(color= "#ffffff"))
    VANILLA_RELEASES = NoxLauncherDropdown(label= "Vanilla Releases", hint_text= "Select a release and install it!", options= [flet.dropdown.Option(version["id"]) for version in minecraft_launcher_lib.utils.get_version_list() if version["type"] == "release"], border_color= "#717171", border_radius= 10, border_width= 2, label_style= flet.TextStyle(color= "#ffffff"))
    FABRIC_SNAPSHOTS = NoxLauncherDropdown(label= "Fabric Snapshots", hint_text= "Select a snapshot and install it!", options= [flet.dropdown.Option(version["version"]) for version in minecraft_launcher_lib.fabric.get_all_minecraft_versions() if version["stable"] == False], border_color= "#717171", border_radius= 10, border_width= 2, label_style= flet.TextStyle(color= "#ffffff"))
    FABRIC_RELEASES = NoxLauncherDropdown(label= "Fabric Releases", hint_text= "Select a release and install it!", options= [flet.dropdown.Option(version["version"]) for version in minecraft_launcher_lib.fabric.get_all_minecraft_versions() if version["stable"]], border_color= "#717171", border_radius= 10, border_width= 2, label_style= flet.TextStyle(color= "#ffffff"))
    FORGE = NoxLauncherDropdown(label= "Forge versions", hint_text= "Select a version and install it!", options= [flet.dropdown.Option(version) for version in minecraft_launcher_lib.forge.list_forge_versions()], border_color= "#717171", border_radius= 10, border_width= 2, label_style= flet.TextStyle(color= "#ffffff"))