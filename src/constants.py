import os
import flet
import minecraft_launcher_lib as mc

from typing import List
from enum import Enum

def minecraft_news() -> List[flet.Container]:

    containers: List[flet.Container] = []

    for articles in mc.utils.get_minecraft_news(5).values():
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

    WINDOWS_HOME = os.environ.get("APPDATA")
    LINUX_HOME = os.environ.get("HOME")
    MAX_WIDTH = 1920
    MAX_HEIGHT = 1080
    MIN_WIDTH = 900
    MIN_HEIGHT = 600
    MINECRAFT_NEWS = minecraft_news()