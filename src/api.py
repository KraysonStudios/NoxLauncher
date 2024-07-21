import flet
import requests
import json

from abs import NoxLauncherContainer, NoxLauncherRow, NoxLauncherColumn
from constants import constants
from utils import check_internet

from functools import cache 
from typing import Any, Dict, List

class NoxLauncherAPI:

    @cache
    def retrieve_all_news() -> List[NoxLauncherContainer]:

        if not check_internet():
            return NoxLauncherAPI.build_error("No internet connection!")
        
        response: requests.Response = requests.get(
           f"{constants.NOX_LAUNCHER_API.value}/get/news",
           timeout= 60
        )

        match response.status_code:

            case 200: ...
            case 501: NoxLauncherAPI.build_error("Service unavailable, pls notify to Krayson Studio!")

    @cache
    def build_error(msg: str) -> List[NoxLauncherContainer]:

        return [NoxLauncherContainer(
            content= NoxLauncherRow(
                controls= [
                    NoxLauncherContainer(
                        width= 10,
                        height= 200,
                        padding= flet.padding.all(10),
                        bgcolor= flet.colors.RED_500,
                        border_radius= 10
                    ),
                    NoxLauncherContainer(   
                        content= NoxLauncherColumn(
                            controls= [
                                flet.Text(msg, size= 20, font_family= "Minecraft"),
                            ],
                            alignment= flet.MainAxisAlignment.CENTER,
                            horizontal_alignment= flet.CrossAxisAlignment.CENTER,
                            spacing= 10
                        ),
                        alignment= flet.alignment.center,
                        expand= True,
                        expand_loose= True,
                        padding= flet.padding.all(10)
                    )
                ],
                expand_loose= True,
                expand= True
            ),
            alignment= flet.alignment.center,
            width= 170,
            height= 120,
            bgcolor= "#272727",
            border_radius= 20
        )]