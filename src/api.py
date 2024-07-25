import flet
import requests

from abs import NoxLauncherContainer, NoxLauncherRow, NoxLauncherColumn
from fs import Config
from constants import constants
from utils import check_internet

from functools import cache 
from typing import Any, Dict, List

class NoxLauncherAPI:

    @cache
    def retrieve_all_news() -> List[NoxLauncherContainer]:

        if not check_internet():
            return NoxLauncherAPI.build_error("No internet connection!")

        if not Config.check_launcher_news():
            
            try:

                response: requests.Response = requests.get(
                    f"{constants.NOX_LAUNCHER_API.value}/get/news",
                    timeout= 60*3
                )

            except requests.exceptions.Timeout:

                return NoxLauncherAPI.build_error("Request timed out!, notify to the developers!")

            match response.status_code:

                case 200: 

                    json_news: List[Dict[str, Any]] = response.json()

                    Config.update_launcher_news(json_news)

                    return [
                        NoxLauncherContainer(
                            content= NoxLauncherRow(
                                controls= [
                                    NoxLauncherContainer(
                                        width= 10,
                                        height= 370,
                                        padding= flet.padding.all(10),
                                        bgcolor= "#148b47",
                                        border_radius= 10
                                    ),
                                    NoxLauncherContainer(   
                                        content= NoxLauncherColumn(
                                            controls= [
                                                flet.Image(src_base64= new["media"], expand_loose= True, height= 120, fit= flet.ImageFit.CONTAIN, border_radius= 20) if new["media"] != "" else NoxLauncherContainer(),
                                                flet.Text(value= new["title"], size= 22, font_family= "Minecraft"),
                                                NoxLauncherContainer(
                                                    expand= True,
                                                    expand_loose= True,
                                                ),
                                                flet.Text(value= new["content"], size= 16, font_family= "Minecraft"),
                                                NoxLauncherContainer(
                                                    expand= True,
                                                    expand_loose= True,
                                                ),
                                                NoxLauncherRow(   
                                                    controls= [
                                                        flet.Text(value= new["time"], size= 12, font_family= "Minecraft"),
                                                        flet.Text(value= new["author"], size= 12, font_family= "Minecraft"),
                                                    ],
                                                    expand_loose= True,
                                                    expand= True,
                                                    alignment= flet.MainAxisAlignment.END,
                                                    spacing= 10
                                                )
                                            ],
                                            alignment= flet.MainAxisAlignment.CENTER,
                                            horizontal_alignment= flet.CrossAxisAlignment.CENTER
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
                            expand_loose= True,
                            height= 370,
                            bgcolor= "#272727",
                            border_radius= 20
                        )
                    
                        for new in json_news
                    ]

                case 429: return NoxLauncherAPI.build_error("You have been rate limited, pls try again later!")
                case 500: return NoxLauncherAPI.build_error("Internal server error, pls notify to Krayson Studio!")
                case 503: return NoxLauncherAPI.build_error("Service unavailable, pls notify to Krayson Studio!")

        return [
            NoxLauncherContainer(
                content= NoxLauncherRow(
                    controls= [
                        NoxLauncherContainer(
                            width= 10,
                            height= 370,
                            padding= flet.padding.all(10),
                            bgcolor= "#148b47",
                            border_radius= 10
                        ),
                        NoxLauncherContainer(   
                            content= NoxLauncherColumn(
                                controls= [
                                    flet.Image(src_base64= new["media"], expand_loose= True, height= 120, fit= flet.ImageFit.CONTAIN, border_radius= 20) if new["media"] != "" else NoxLauncherContainer(),
                                    flet.Text(value= new["title"], size= 22, font_family= "Minecraft"),
                                    NoxLauncherContainer(
                                        expand= True,
                                        expand_loose= True,
                                    ),
                                    flet.Text(value= new["content"], size= 16, font_family= "Minecraft"),
                                    NoxLauncherContainer(
                                        expand= True,
                                        expand_loose= True,
                                    ),
                                    NoxLauncherRow(   
                                        controls= [
                                            flet.Text(value= new["time"], size= 12, font_family= "Minecraft"),
                                            flet.Text(value= "|", size= 12, font_family= "Minecraft"),
                                            flet.Text(value= new["author"], size= 12, font_family= "Minecraft")
                                        ],
                                        expand_loose= True,
                                        expand= True,
                                        alignment= flet.MainAxisAlignment.END
                                    )
                                ],
                                alignment= flet.MainAxisAlignment.CENTER,
                                horizontal_alignment= flet.CrossAxisAlignment.CENTER
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
                expand_loose= True,
                height= 370,
                bgcolor= "#272727",
                border_radius= 20
            )

            for new in Config.get_launcher_news()
        ]

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