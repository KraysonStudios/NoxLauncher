import flet

class BackToPlayButton:

    def __init__(self, page: flet.Page, width: int = 240, height: int = 90, text: str = "Back to home", path: str = "/home", bgcolor: str | None = "#272727") -> None:

        self.page: flet.Page = page
        self.height: int = height
        self.width: int = width
        self.text: str = text
        self.path: str = path
        self.bgcolor: str | None = bgcolor
        
        self.build()

    def build(self) -> flet.Container:

        return flet.Container(
            content= flet.Container(
                content= flet.Row(
                    controls= [
                        flet.Icon(name= flet.icons.ARROW_BACK, color= "#717171", size= 40),
                        flet.Container(content= flet.Text(self.text, size= 20, font_family= "NoxLauncher"), expand_loose= True, alignment= flet.alignment.center, padding= flet.padding.only(top= 2))
                    ],
                    height= self.height,
                    width= self.width,
                ),
                height= self.height,
                width= self.width,
                padding= flet.padding.only(left= 20),
                bgcolor= self.bgcolor,
                border_radius= 20,
                alignment= flet.alignment.center
            ),
            expand= True,
            expand_loose= True,
            padding= flet.padding.only(left= 20),
            on_click= lambda _: self.page.go(self.path)
        )
