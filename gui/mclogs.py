import flet

from gui.appbar import NoxLauncherGenericAppBar
from fs import get_mc_logs

from typing import List

class NoxLauncherMCLogsGUI:

    def __init__(self, page: flet.Page) -> None:

        self.page: flet.Page = page
        self.index: int = len(get_mc_logs()) - 1
        self.mc_logs: List[flet.Text] = get_mc_logs()
        self.logs_column: flet.Column = flet.Column(
            controls= [self.mc_logs[len(self.mc_logs) - 1]],
            scroll= flet.ScrollMode.AUTO,
            expand= True,
            expand_loose= True
        )

        self.build()

    def build(self) -> flet.View:

        return flet.View(
            appbar= NoxLauncherGenericAppBar(self.page, "Back to home", "/home").build(),
            controls= [
                flet.Container(
                    image= flet.DecorationImage(src= "assets/bgmclogs.png", fit= flet.ImageFit.COVER, filter_quality= flet.FilterQuality.HIGH, repeat= flet.ImageRepeat.NO_REPEAT),
                    expand= True,
                    expand_loose= True,
                    alignment= flet.alignment.center,
                    content= flet.Column(
                        controls= [
                            flet.Text("Minecraft Logs", size= 30, font_family= "NoxLauncher", color= "#FFFFFF"),
                            flet.Container(
                                content= flet.Row(
                                    controls= [
                                        flet.Column(
                                            controls= [flet.IconButton(icon= flet.icons.ARROW_BACK, icon_color= "#717171", icon_size= 30, expand= True, width= 50, on_click= self.back)]
                                        ) if len(self.mc_logs) >= 2 else flet.Container(),
                                        flet.Column(
                                            controls= [
                                                flet.Container(
                                                    expand_loose= True, 
                                                    expand= True, 
                                                    alignment= flet.alignment.center, 
                                                    content= self.logs_column,
                                                    padding= flet.padding.only(left= 10, bottom= 2, right= 10, top= 5)
                                                ),
                                                flet.Container(flet.IconButton(icon= flet.icons.COPY, icon_color= "#717171", icon_size= 30, width= 50, height= 50, on_click= lambda _: self.page.set_clipboard(self.mc_logs[self.index].value)), alignment= flet.alignment.center_right, padding= flet.padding.only(right= 20, bottom= 5))
                                            ],
                                            expand_loose= True,
                                            expand= True,
                                            alignment= flet.MainAxisAlignment.CENTER,
                                            horizontal_alignment= flet.CrossAxisAlignment.CENTER,
                                            spacing= 5,
                                            run_spacing= 5
                                        ) if len(self.mc_logs) >= 1 else flet.Container(alignment= flet.alignment.center, content= flet.Text("No logs found!", size= 20, font_family= "NoxLauncher", color= "#FFFFFF"), expand= True, expand_loose= True)
                                    ],
                                    expand_loose= True,
                                    expand= True
                                ),
                                width= 650,
                                height= 490,
                                alignment= flet.alignment.center,
                                bgcolor= "#272727",
                                border_radius= 20,
                            )  
                        ],
                        expand= True,
                        expand_loose= True,
                        alignment= flet.MainAxisAlignment.CENTER,
                        horizontal_alignment= flet.CrossAxisAlignment.CENTER,
                    )
                )
            ],
            padding= 0,
        )
    
    def back(self, _: flet.ControlEvent) -> None:

        if self.index <= 0:
            self.index = len(self.mc_logs) - 1
        else: 
            self.index -= 1 

        self.logs_column.controls = [self.mc_logs[self.index]]
        self.logs_column.update()