import flet

from gui.buttons import BackToPlayButton

class NoxLauncherGenericAppBar:

    def __init__(self, page: flet.Page, text: str = "Back to forge", path: str = "/install") -> None:

        self.page: flet.Page = page
        self.text: str = text
        self.path: str = path
        self.build()

    def build(self) -> flet.AppBar:

        return flet.AppBar(
            leading= BackToPlayButton(self.page, text= self.text, path= self.path, bgcolor= None).build(),
            leading_width= 240,
            title= flet.Image(src= "assets/icon.png", width= 200, height= 170, filter_quality= flet.FilterQuality.HIGH),
            center_title= True,
            bgcolor= "#272727",
            toolbar_height= 120
        )