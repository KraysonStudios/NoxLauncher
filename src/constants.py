try:
    import flet
    import os
    import json
    import datetime
    import minecraft_launcher_lib

    from fs import Config
    from typing import List
    from enum import Enum

except Exception as e: raise Exception(f"Report this error to the developers: \n{e.args[0]}\n")

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

                news = json.load(f)

                if "news" not in news: Config.repair()
                elif "requested" not in news: Config.repair()
                elif not isinstance(news["news"], list): Config.repair()
                elif not isinstance(news["requested"], str): Config.repair()

                if datetime.datetime.strftime(datetime.datetime.now(datetime.UTC), "%Y-%m-%d") != news["requested"]:

                    for article in minecraft_launcher_lib.utils.get_minecraft_news(5).values():

                        if isinstance(article, list): 
                            news["news"].extend(article)
                            break

                    news["requested"] = datetime.datetime.strftime(datetime.datetime.now(datetime.UTC), "%Y-%m-%d")
            
                    with open(Config.get_path() + "/NoxLauncher/cache/minecraft_news.json", "w") as f: json.dump(news, f, indent= 4)

        with open(Config.get_path() + "/NoxLauncher/cache/minecraft_news.json", "r", encoding= "utf-8") as f: 

            news = json.load(f)

            if "news" not in news: Config.repair()
            elif len(news["news"]) == 0: 

                with open(Config.get_path() + "/NoxLauncher/cache/minecraft_news.json", "r", encoding= "utf-8") as f: 

                    news = json.load(f)

                    if "news" not in news: Config.repair()
                    elif not isinstance(news["news"], list): Config.repair()

                    for article in minecraft_launcher_lib.utils.get_minecraft_news(5).values():

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
                    bgcolor= "#272727",
                    padding= flet.padding.all(20)
                ))

    return containers

class constants(Enum):

    MAX_WIDTH = 1920
    MAX_HEIGHT = 1080
    MIN_WIDTH = 900
    MIN_HEIGHT = 700
    MINECRAFT_NEWS = minecraft_news()
    VANILLA_SNAPSHOTS = [flet.dropdown.Option(version["id"]) for version in minecraft_launcher_lib.utils.get_version_list() if version["type"] == "snapshot"]
    VANILLA_RELEASES = [flet.dropdown.Option(version["id"]) for version in minecraft_launcher_lib.utils.get_version_list() if version["type"] == "release"]
    FABRIC_SNAPSHOTS = [flet.dropdown.Option(version["version"]) for version in minecraft_launcher_lib.fabric.get_all_minecraft_versions() if version["stable"] == False]
    FABRIC_RELEASES = [flet.dropdown.Option(version["version"]) for version in minecraft_launcher_lib.fabric.get_all_minecraft_versions() if version["stable"]]
    FORGE = [flet.dropdown.Option(version) for version in minecraft_launcher_lib.forge.list_forge_versions()]