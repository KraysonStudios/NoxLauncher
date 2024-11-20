import flet

from gui.utils import open_discord, open_github, open_kofi
from gui.buttons import BackToPlayButton

class NoxLauncherInfoGUI:

    def __init__(self, page: flet.Page) -> None:

        self.page: flet.Page = page
        self.build()

    def build(self) -> flet.View:

        return flet.View(
            controls= [
                flet.Container(
                    content = flet.Column(
                        controls= [
                            flet.Row(
                                controls= [
                                    BackToPlayButton(self.page).build(),
                                ],
                                height= 150,
                                expand_loose= True
                            ),
                            flet.Container(
                                content= flet.Container(
                                    content= flet.Column(
                                        controls= [
                                            flet.Image(src= "assets/icon.png", width= 230, height= 140, filter_quality= flet.FilterQuality.HIGH),
                                            flet.Container(
                                                content= flet.Text("\" NoxLauncher is a powerful Open Source launcher created by Krayson Studio and its main developers, to provide secure access to a minecraft launcher. \" This launcher is not affiliated with Mojang Studios and their games.", size= 17, font_family= "NoxLauncher"), 
                                                alignment= flet.alignment.center,
                                                expand_loose= True,
                                                padding= flet.padding.only(left= 20, right= 20, bottom= 15)
                                            ),
                                            flet.Container(
                                                content= flet.Row(
                                                    controls= [
                                                        flet.Icon(name= flet.icons.HANDYMAN, color= "#717171", size= 40),
                                                        flet.Text("Main Developers", size= 20, font_family= "NoxLauncher")
                                                    ],
                                                    expand_loose= True
                                                ),
                                                expand_loose= True,
                                                padding= flet.padding.only(left= 20, bottom= 10)
                                            ),
                                            flet.Container(
                                                content= flet.Column(
                                                    controls= [
                                                        flet.Text("•   DevCheckOG", size= 18, font_family= "NoxLauncher"),
                                                        flet.Text("•   Aaronwayas", size= 18, font_family= "NoxLauncher"),
                                                    ],
                                                    expand_loose= True
                                                ),
                                                expand_loose= True,
                                                padding= flet.padding.only(left= 70, bottom= 15),
                                                alignment= flet.alignment.center_left
                                            ),
                                            flet.Container(
                                                content= flet.Row(
                                                    controls= [
                                                        flet.Container(content= flet.Image(src= "assets/discord.png", width= 52, height= 52, filter_quality= flet.FilterQuality.HIGH), on_click= lambda _: open_discord()),
                                                        flet.Container(content= flet.Image(src= "assets/github.png", width= 52, height= 52, filter_quality= flet.FilterQuality.HIGH), on_click= lambda _: open_github()),
                                                        flet.Container(content= flet.Image(src= "assets/kofi.png", width= 52, height= 52, filter_quality= flet.FilterQuality.HIGH), on_click= lambda _: open_kofi())
                                                    ],
                                                    run_spacing= 50,
                                                    spacing= 50,
                                                    expand_loose= True,
                                                    alignment= flet.MainAxisAlignment.CENTER,
                                                    vertical_alignment= flet.CrossAxisAlignment.CENTER
                                                ),
                                                alignment= flet.alignment.center,
                                                expand_loose= True
                                            )
                                        ],
                                        horizontal_alignment= flet.CrossAxisAlignment.CENTER,
                                        expand= True,
                                        expand_loose= True
                                    ),
                                    bgcolor= "#272727",
                                    alignment= flet.alignment.center,
                                    width= 620,
                                    height= 500,
                                    border_radius= 20
                                ),
                                expand= True,
                                expand_loose= True,
                                alignment= flet.alignment.center
                            )
                        ],
                        expand= True,
                        expand_loose= True,
                        horizontal_alignment= flet.CrossAxisAlignment.CENTER
                    ),
                    expand= True,
                    expand_loose= True,
                    image= flet.DecorationImage(src= "assets/bginfo.png", fit= flet.ImageFit.COVER, filter_quality= flet.FilterQuality.HIGH, repeat= flet.ImageRepeat.NO_REPEAT),
                    alignment= flet.alignment.center,
                )
            ],
            padding= 0,
            horizontal_alignment= flet.CrossAxisAlignment.CENTER,
            vertical_alignment= flet.MainAxisAlignment.CENTER,
        )