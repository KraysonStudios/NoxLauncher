import minecraft_launcher_lib
import flet
import time

from modrinthapi import ModrinthAPI
from gui.appbar import NoxLauncherGenericAppBar

from fs import *

class NoxLauncherInstallFabricGUI:

    def __init__(self, page: flet.Page) -> None:

        self.page: flet.Page = page
        self.modrinth: ModrinthAPI = ModrinthAPI(self.page, "fabric")
        self.build()

    def search_mods(self, event: flet.ControlEvent) -> None: self.modrinth.search_projects(event.control.value)

    def build(self) -> flet.View:

        return flet.View(
            appbar= NoxLauncherGenericAppBar(self.page).build(),
            controls= [
                flet.Container(
                    content= flet.Row(
                        controls= [
                            flet.Column(
                                controls= [
                                    flet.Container(
                                        content= flet.Column(
                                            controls= [
                                                flet.Container(
                                                    content= flet.Text("Fabric Releases", size= 25, font_family= "NoxLauncher", color= "#FFFFFF"),
                                                    alignment= flet.alignment.center,
                                                    expand_loose= True,
                                                ),
                                                flet.Container(
                                                    content= flet.Dropdown(hint_text= "A fabric release to install!", options= get_fabric_releases(), border_color= "#717171", border_radius= 10, border_width= 2, hint_style= flet.TextStyle(size= 14, font_family= "NoxLauncher"), on_change= self.install),
                                                    alignment= flet.alignment.center,
                                                    expand_loose= True,
                                                    padding= flet.padding.only(left= 40, right= 40, bottom= 25)
                                                ),
                                                flet.Container(
                                                    content= flet.Text("Fabric Snapshots", size= 25, font_family= "NoxLauncher", color= "#FFFFFF"),
                                                    alignment= flet.alignment.center,
                                                    expand_loose= True,
                                                ),
                                                flet.Container(
                                                    content= flet.Dropdown(hint_text= "A fabric snapshot to install!", options= get_fabric_snapshots(), border_color= "#717171", border_radius= 10, border_width= 2, hint_style= flet.TextStyle(size= 14, font_family= "NoxLauncher"), on_change= self.install),
                                                    alignment= flet.alignment.center,
                                                    expand_loose= True,
                                                    padding= flet.padding.only(left= 10, right= 10, bottom= 20)
                                                )
                                            ],
                                            expand= True,
                                            expand_loose= True,
                                            horizontal_alignment= flet.CrossAxisAlignment.CENTER,
                                        ),
                                        width= 480,
                                        height= 280,
                                        bgcolor= "#272727",
                                        border_radius= 20,
                                        padding= 20
                                    )
                                ],
                                alignment= flet.MainAxisAlignment.CENTER,
                                horizontal_alignment= flet.CrossAxisAlignment.CENTER,
                                expand_loose= True,
                                expand= True
                            ),
                            flet.Column(
                                controls= [
                                    flet.Container( 
                                        content= flet.Column(
                                            controls= [
                                                flet.Container(
                                                    content= flet.Row(
                                                        controls= [
                                                            flet.Image(src= "assets/modrinth.png", width= 100, height= 80, filter_quality= flet.FilterQuality.HIGH),
                                                            flet.Text("Modrinth", size= 30, font_family= "NoxLauncher", color= "#FFFFFF")
                                                        ],
                                                        expand_loose= True,  
                                                        alignment= flet.MainAxisAlignment.CENTER,
                                                        run_spacing= 0,
                                                        spacing= 0
                                                    ),
                                                    alignment= flet.alignment.center,
                                                    expand_loose= True,
                                                    height= 80,
                                                ),
                                                flet.Container(
                                                    content= flet.TextField(multiline= False, expand_loose= True, height= 70, border_radius= 10, border_color= "#717171", label= "Search Mods", label_style= flet.TextStyle(size= 16, font_family= "NoxLauncher", color= "#FFFFFF"), hint_text= "Search mods by name", hint_style= flet.TextStyle(size= 16, font_family= "NoxLauncher"), text_style= flet.TextStyle(size= 14, font_family= "NoxLauncher", color= "#FFFFFF"), on_submit= self.search_mods),
                                                    alignment= flet.alignment.center,
                                                    expand_loose= True
                                                ),
                                                self.modrinth.container
                                            ],
                                            expand_loose= True,
                                            expand= True,
                                            horizontal_alignment= flet.CrossAxisAlignment.CENTER,
                                            spacing= 30
                                        ),
                                        width= 550,
                                        height= 570,
                                        bgcolor= "#272727",
                                        border_radius= 20,
                                        padding= 20
                                    )
                                ],
                                alignment= flet.MainAxisAlignment.CENTER,
                                horizontal_alignment= flet.CrossAxisAlignment.CENTER,
                                expand_loose= True,
                                expand= True
                            )
                        ], 
                        expand= True,
                        expand_loose= True,
                        spacing= 260,
                        run_spacing= 260,
                        alignment= flet.MainAxisAlignment.CENTER,
                        vertical_alignment= flet.CrossAxisAlignment.CENTER
                    ),
                    image= flet.DecorationImage(src= "assets/bgfabric.png", fit= flet.ImageFit.COVER, filter_quality= flet.FilterQuality.HIGH, repeat= flet.ImageRepeat.NO_REPEAT),
                    expand= True,
                    expand_loose= True,
                    alignment= flet.alignment.center
                )
            ],
            padding= 0
        )
    
    def install(self, event: flet.ControlEvent) -> None:

        if not has_internet(): return

        status_text: flet.Text = flet.Text(value= "...", size= 16, font_family= "NoxLauncher", color= "#FFFFFF")

        installer_alert: flet.AlertDialog = flet.AlertDialog(
            modal= True,
            icon= flet.Image(src= "assets/fabric.png", width= 160, height= 130, filter_quality= flet.FilterQuality.HIGH),
            title= flet.Container(
                content= flet.Text(value= event.control.value, size= 18, font_family= "NoxLauncher", color= "#FFFFFF"),
                alignment= flet.alignment.center,
                expand_loose= True
            ),
            bgcolor= "#272727",
            content= flet.Column(
                [
                    flet.Text(value= "Installing and downloading...", size= 18, font_family= "NoxLauncher", color= "#717171"),
                    status_text,
                    flet.ProgressBar(width= 150, color= "#148b47")
                ],
                alignment= flet.MainAxisAlignment.CENTER,
                horizontal_alignment= flet.CrossAxisAlignment.CENTER,
                height= 100,
                expand_loose= True
            ),
            actions= [
                flet.FilledButton(
                    text= "Cancel",
                    style= flet.ButtonStyle(
                        color= "#FFFFFF",
                        bgcolor= "#148b47",
                        text_style= flet.TextStyle(font_family= "NoxLauncher", size= 18),
                        shape= flet.RoundedRectangleBorder(radius= 10)
                    ),
                    height= 50,
                    width= 150,
                    on_click= lambda _: self.page.close(installer_alert)
                )
            ]
        )

        self.page.open(installer_alert)

        def setStatus(status: str) -> None:

            status_text.value = status
            status_text.update()

        try:

            minecraft_launcher_lib.fabric.install_fabric(event.control.value, get_home(), callback= {"setStatus": setStatus})

            installer_alert.content = flet.Container(
                content= flet.Text(value= "Done!", size= 18, font_family= "NoxLauncher", color= "#FFFFFF"),
                width= 50,
                height= 40,
                alignment= flet.alignment.center,
            )

            installer_alert.update()

            time.sleep(3)

            self.page.close(installer_alert)

            return

        except: 
            
            time.sleep(5)
            self.page.close(installer_alert)