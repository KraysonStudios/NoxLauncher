import flet

from fs import *

class NoxLauncherHomeGUI: 

    def __init__(self, page: flet.Page) -> None:

        self.page: flet.Page = page
        self.build()

    def build(self) -> flet.View:

        return flet.View(
            appbar= NoxLauncherHomeAppBar(self.page).build(),
            controls= [
                flet.Container(
                    alignment= flet.alignment.center,
                    expand= True,
                    expand_loose= True,
                    image= flet.DecorationImage(src= "assets/bghome.png", fit= flet.ImageFit.COVER, filter_quality= flet.FilterQuality.HIGH, repeat= flet.ImageRepeat.NO_REPEAT),
                    content= flet.Row(
                        controls= [
                            flet.Column(
                                controls= [
                                    flet.Container(
                                        width= 300,
                                        height= 280,
                                        border_radius= 20,
                                        content= flet.Image(
                                            src= "assets/play.png", 
                                            repeat= flet.ImageRepeat.NO_REPEAT, 
                                            filter_quality= flet.FilterQuality.HIGH,
                                            tooltip= flet.Tooltip(
                                                message= "Select and play the version you want!",
                                                bgcolor= "#272727",
                                                text_style= flet.TextStyle(
                                                    size= 14,
                                                    color= "#FFFFFF",
                                                    font_family= "NoxLauncher"
                                                )
                                            )
                                        ),
                                        on_click= lambda _: self.page.go("/play")
                                    )
                                ],
                                alignment= flet.MainAxisAlignment.CENTER,
                                horizontal_alignment= flet.CrossAxisAlignment.CENTER,
                                expand= True,
                                expand_loose= True
                            ),
                            flet.Column(
                                controls= [
                                    flet.Container(
                                        width= 300,
                                        height= 280,
                                        border_radius= 20,
                                        content= flet.Image(src= "assets/mods.png", repeat= flet.ImageRepeat.NO_REPEAT, filter_quality= flet.FilterQuality.HIGH, width= 80, height= 80),
                                        tooltip= flet.Tooltip(
                                            message= "Download and install mod loaders like Fabric, Forge or simple Vanilla.",
                                            bgcolor= "#272727",
                                            text_style= flet.TextStyle(
                                                size= 14,
                                                color= "#FFFFFF",
                                                font_family= "NoxLauncher"
                                            )
                                        ),
                                        on_click= lambda _: self.page.go("/install")
                                    ),
                                ],
                                alignment= flet.MainAxisAlignment.CENTER,
                                horizontal_alignment= flet.CrossAxisAlignment.CENTER,
                                expand= True,
                                expand_loose= True
                            ),
                            flet.Column(
                                controls= [
                                    flet.Container(
                                        width= 300,
                                        height= 280,
                                        border_radius= 20,
                                        content= flet.Image(src= "assets/accounts.png", repeat= flet.ImageRepeat.NO_REPEAT, filter_quality= flet.FilterQuality.HIGH),
                                        tooltip= flet.Tooltip(
                                            message= "Change the account or skin.",
                                            bgcolor= "#272727",
                                            text_style= flet.TextStyle(
                                                size= 14,
                                                color= "#FFFFFF",
                                                font_family= "NoxLauncher"
                                            )
                                        ),
                                        on_click= lambda _: self.page.go("/accounts")
                                    )
                                ],
                                alignment= flet.MainAxisAlignment.CENTER,
                                horizontal_alignment= flet.CrossAxisAlignment.CENTER,
                                expand= True,
                                expand_loose= True
                            )
                        ],
                        expand= True,
                        expand_loose= True,
                        spacing= 80,
                        alignment= flet.MainAxisAlignment.CENTER,
                        vertical_alignment= flet.CrossAxisAlignment.CENTER
                    )
                )
            ],
            padding= 0
        )
    
class NoxLauncherHomeAppBar: 

    def __init__(self, page: flet.Page) -> None:

        self.page: flet.Page = page
        self.build()

    def build(self) -> flet.AppBar:

        return flet.AppBar(
            title= flet.Image(src= "assets/icon.png", width= 200, height= 170, filter_quality= flet.FilterQuality.HIGH),
            center_title= True,
            actions= [
                flet.Container(
                    width= 400,
                    height= 44, 
                    alignment= flet.alignment.center,
                    content= flet.Row(
                        expand= True,
                        expand_loose= True,
                        spacing= 12,
                        controls= [
                            flet.IconButton(
                                icon= flet.icons.INFO,
                                icon_size= 26,
                                icon_color= "#717171",
                                height= 42,
                                width= 42,
                                on_click= lambda _: self.page.go("/info")
                            ),
                            flet.VerticalDivider(color= "#717171", width= 1),
                            flet.IconButton(icon= flet.icons.SETTINGS_ROUNDED, icon_color= "#717171", icon_size= 30, on_click= lambda _: self.page.go("/settings")),
                            flet.IconButton(icon= flet.icons.FOLDER_OPEN, icon_color= "#717171", icon_size= 30, on_click= open_home),
                            flet.VerticalDivider(color= "#717171", width= 1),
                            flet.FilledButton(icon= flet.icons.HELP_CENTER, icon_color= "#717171", text= "You need help?", style= flet.ButtonStyle(text_style= flet.TextStyle(font_family= "NoxLauncher", size= 16), bgcolor= "#272727", color= "#FFFFFF"), height= 60)
                        ],
                        alignment= flet.MainAxisAlignment.CENTER,
                        vertical_alignment= flet.CrossAxisAlignment.CENTER
                    )
                )
            ],
            bgcolor= "#272727",
            toolbar_height= 120,
        )