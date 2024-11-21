import flet

from gui.buttons import BackToPlayButton
from gui.appbar import NoxLauncherGenericAppBar

class NoxLauncherInstallGUI:

    def __init__(self, page: flet.Page) -> None:

        self.page: flet.Page = page
        self.build()

    def build(self) -> flet.View:

        return flet.View(
            appbar= NoxLauncherGenericAppBar(self.page, "Back to home", "/home").build(),
            controls= [
                flet.Container(
                    image= flet.DecorationImage(src= "assets/bginstall.png", fit= flet.ImageFit.COVER, filter_quality= flet.FilterQuality.HIGH, repeat= flet.ImageRepeat.NO_REPEAT),
                    expand= True,
                    expand_loose= True,
                    content= flet.Row(
                        controls= [
                            flet.Container(
                                content= flet.Column(
                                    controls= [
                                        flet.Image(src= "assets/fabric.png", width= 200, height= 150, filter_quality= flet.FilterQuality.HIGH, repeat= flet.ImageRepeat.NO_REPEAT), 
                                        flet.Text("Fabric", size= 25, font_family= "NoxLauncher", color= "#FFFFFF"), 
                                    ],
                                    expand= True,
                                    expand_loose= True,
                                    horizontal_alignment= flet.CrossAxisAlignment.CENTER,
                                    alignment= flet.MainAxisAlignment.CENTER,
                                    spacing= 40,
                                    run_spacing= 40
                                ),
                                bgcolor= "#272727",
                                border_radius= 20,
                                width= 300,
                                height= 280,
                                on_click= lambda _: self.page.go("/install/fabric")
                            ),
                            flet.Container(
                                content= flet.Column(
                                    controls= [
                                        flet.Image(src= "assets/vanilla.png", width= 200, height= 150, filter_quality= flet.FilterQuality.HIGH, repeat= flet.ImageRepeat.NO_REPEAT), 
                                        flet.Text("Vanilla", size= 25, font_family= "NoxLauncher", color= "#FFFFFF"), 
                                    ],
                                    expand= True,
                                    expand_loose= True,
                                    horizontal_alignment= flet.CrossAxisAlignment.CENTER,
                                    alignment= flet.MainAxisAlignment.CENTER,
                                    spacing= 40,
                                    run_spacing= 40
                                ),
                                bgcolor= "#272727",
                                border_radius= 20,
                                width= 300,
                                height= 280,
                                on_click= lambda _: self.page.go("/install/vanilla")
                            ), 
                            flet.Container(
                                content= flet.Column(
                                    controls= [
                                        flet.Image(src= "assets/forge.png", width= 200, height= 150, filter_quality= flet.FilterQuality.HIGH, repeat= flet.ImageRepeat.NO_REPEAT), 
                                        flet.Text("Forge", size= 25, font_family= "NoxLauncher", color= "#FFFFFF"), 
                                    ],
                                    expand= True,
                                    expand_loose= True,
                                    horizontal_alignment= flet.CrossAxisAlignment.CENTER,
                                    alignment= flet.MainAxisAlignment.CENTER,
                                    spacing= 40,
                                    run_spacing= 40
                                ),
                                bgcolor= "#272727",
                                border_radius= 20,
                                width= 300,
                                height= 280,
                                on_click= lambda _: self.page.go("/install/forge")
                            )
                        ],
                        vertical_alignment= flet.CrossAxisAlignment.CENTER,  
                        alignment= flet.MainAxisAlignment.CENTER,
                        expand= True,
                        expand_loose= True,
                        spacing= 60,
                        run_spacing= 60
                    ),
                    alignment= flet.alignment.center
                )
                        
            ],
            padding= 0
        )
    
class NoxLauncherInstallAppBar: 

    def __init__(self, page: flet.Page) -> None:

        self.page: flet.Page = page
        self.build()

    def build(self) -> flet.AppBar:

        return flet.AppBar(
            leading= BackToPlayButton(self.page).build(),
            leading_width= 240,
            title= flet.Image(src= "assets/icon.png", width= 200, height= 170, filter_quality= flet.FilterQuality.HIGH),
            center_title= True,
            actions= [
                flet.Container(
                    width= 250,
                    height= 44, 
                    alignment= flet.alignment.center,
                    content= flet.Row(
                        expand= True,
                        expand_loose= True,
                        spacing= 5,
                        run_spacing= 5,
                        controls= [
                            flet.Container(
                                content= flet.Image(
                                    src= "assets/fabric.png", 
                                    width= 80, 
                                    height= 80, 
                                    filter_quality= flet.FilterQuality.HIGH, 
                                    tooltip= flet.Tooltip(
                                        message= "Install the mod fabric loader in addition to installing mods via modrinth.",
                                        bgcolor= "#272727",
                                        text_style= flet.TextStyle(
                                            size= 14,
                                            color= "#FFFFFF",
                                            font_family= "NoxLauncher"
                                        )
                                    )
                                ),
                                on_click= lambda _: self.page.go("/install/fabric")
                            ),
                            flet.Container(
                                content= flet.Image(
                                    src= "assets/forge.png", 
                                    width= 80, 
                                    height= 80, 
                                    filter_quality= flet.FilterQuality.HIGH,
                                    tooltip= flet.Tooltip(
                                        message= "Install the mod forge loader in addition to installing mods via modrinth.",
                                        bgcolor= "#272727",
                                        text_style= flet.TextStyle(
                                            size= 14,
                                            color= "#FFFFFF",
                                            font_family= "NoxLauncher"
                                        )
                                    )
                                ),
                                on_click= lambda _: self.page.go("/install/forge")
                            ),
                            flet.Container(
                                content= flet.Image(
                                    src= "assets/vanilla.png", 
                                    width= 80, 
                                    height= 80, 
                                    filter_quality= flet.FilterQuality.HIGH,
                                    tooltip= flet.Tooltip(
                                        message= "Install the a vanilla version.",
                                        bgcolor= "#272727",
                                        text_style= flet.TextStyle(
                                            size= 14,
                                            color= "#FFFFFF",
                                            font_family= "NoxLauncher"
                                        )
                                    )
                                ),
                                on_click= lambda _: self.page.go("/install/vanilla")
                            )
                        ],
                        alignment= flet.MainAxisAlignment.CENTER,
                        vertical_alignment= flet.CrossAxisAlignment.CENTER
                    )
                )
            ],
            bgcolor= "#272727",
            toolbar_height= 120
        )