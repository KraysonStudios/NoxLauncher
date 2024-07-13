import flet
import minecraft_launcher_lib

from typing import List
from enum import Enum

def minecraft_news() -> List[flet.Container]:

    containers: List[flet.Container] = []

    for articles in minecraft_launcher_lib.utils.get_minecraft_news(5).values():
        if not isinstance(articles, int):
            for article in articles:
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