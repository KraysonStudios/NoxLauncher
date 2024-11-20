import flet

from gui.appbar import NoxLauncherGenericAppBar

class NoxLauncherHelpGUI:

    def __init__(self, page: flet.Page) -> None:

        self.page: flet.Page = page
        self.build()

    def build(self) -> flet.View:

        return flet.View(
            appbar= NoxLauncherGenericAppBar(self.page, "Back to home", "/home").build(),
            controls= [
                flet.Container(
                    content= flet.Row(
                        controls= [
                            flet.Container(
                                content= flet.Column(
                                    controls= [
                                        flet.Image(src= "assets/java.png", width= 240, height= 200, filter_quality= flet.FilterQuality.HIGH, repeat= flet.ImageRepeat.NO_REPEAT), 
                                        flet.Text("Java Help", size= 25, font_family= "NoxLauncher", color= "#FFFFFF"), 
                                    ],
                                    expand= True,
                                    expand_loose= True,
                                    horizontal_alignment= flet.CrossAxisAlignment.CENTER
                                ),
                                bgcolor= "#272727",
                                border_radius= 20,
                                width= 360,
                                height= 280
                            ),
                            flet.Container(
                                content= flet.Column(
                                    controls= [
                                        flet.Image(src= "assets/mods.png", width= 240, height= 200, filter_quality= flet.FilterQuality.HIGH, repeat= flet.ImageRepeat.NO_REPEAT), 
                                        flet.Text("Mods Help", size= 25, font_family= "NoxLauncher", color= "#FFFFFF"), 
                                    ],
                                    expand= True,
                                    expand_loose= True,
                                    horizontal_alignment= flet.CrossAxisAlignment.CENTER
                                ),
                                bgcolor= "#272727",
                                border_radius= 20,
                                width= 360,
                                height= 280
                            ),
                            flet.Container(
                                content= flet.Column(
                                    controls= [
                                        flet.Image(src= "assets/play.png", width= 240, height= 200, filter_quality= flet.FilterQuality.HIGH, repeat= flet.ImageRepeat.NO_REPEAT), 
                                        flet.Text("Launcher Help", size= 25, font_family= "NoxLauncher", color= "#FFFFFF"), 
                                    ],
                                    expand= True,
                                    expand_loose= True,
                                    horizontal_alignment= flet.CrossAxisAlignment.CENTER
                                ),
                                bgcolor= "#272727",
                                border_radius= 20,
                                width= 360,
                                height= 280
                            )
                        ],
                        expand= True,
                        expand_loose= True,
                        alignment= flet.MainAxisAlignment.CENTER,
                        vertical_alignment= flet.CrossAxisAlignment.CENTER,  
                        run_spacing= 40,
                        spacing= 40
                    ),
                    image= flet.DecorationImage(src= "assets/bghelp.png", fit= flet.ImageFit.COVER, filter_quality= flet.FilterQuality.HIGH, repeat= flet.ImageRepeat.NO_REPEAT),
                    expand= True,
                    expand_loose= True,
                    alignment= flet.alignment.center
                )
            ],
            padding= 0
        )