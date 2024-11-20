import flet

from gui.appbar import NoxLauncherGenericAppBar

class NoxLauncherAccountsGUI:

    def __init__(self, page: flet.Page) -> None:

        self.page: flet.Page = page
        self.build()

    def build(self) -> flet.View:

        return flet.View(
            appbar= NoxLauncherGenericAppBar(self.page, "Back to home", "/home").build(),
            controls= [
                flet.Container(
                    image= flet.DecorationImage(src= "assets/bgaccounts.png", fit= flet.ImageFit.COVER, filter_quality= flet.FilterQuality.HIGH, repeat= flet.ImageRepeat.NO_REPEAT),
                    content= flet.Row(
                        controls= [
                            flet.Container(
                                content= flet.Column(
                                    controls= [
                                        flet.Image(src= "assets/nopremiumacc.png", width= 240, height= 200, filter_quality= flet.FilterQuality.HIGH, repeat= flet.ImageRepeat.NO_REPEAT), 
                                        flet.Text("Free Accounts", size= 25, font_family= "NoxLauncher", color= "#FFFFFF"), 
                                    ],
                                    expand= True,
                                    expand_loose= True,
                                    horizontal_alignment= flet.CrossAxisAlignment.CENTER
                                ),
                                bgcolor= "#272727",
                                border_radius= 20,
                                width= 360,
                                height= 280,
                                on_click= lambda _: self.page.go("/accounts/nopremium")
                            ),
                            flet.Container(
                                content= flet.Text("Coming Soon...", size= 25, font_family= "NoxLauncher", color= "#FFFFFF"),
                                bgcolor= "#272727",
                                border_radius= 20,
                                width= 360,
                                height= 280,
                                alignment= flet.alignment.center
                            )
                        ],
                        expand= True,
                        expand_loose= True,
                        run_spacing= 180,
                        spacing= 180,
                        alignment= flet.MainAxisAlignment.CENTER
                    ),
                    expand= True,
                    expand_loose= True,
                    alignment= flet.alignment.center
                )
            ],
            padding= 0
        )