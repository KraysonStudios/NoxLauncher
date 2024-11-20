import minecraft_launcher_lib
import time
import flet

from gui.appbar import NoxLauncherGenericAppBar
from fs import *

class NoxLauncherInstallVanillaGUI:

    def __init__(self, page: flet.Page) -> None:

        self.page: flet.Page = page
        self.build()

    def build(self) -> flet.View:

        return flet.View(
            appbar= NoxLauncherGenericAppBar(self.page).build(),
            controls= [
                flet.Container(
                    content= flet.Column(
                        controls= [
                            flet.Container(
                                content= flet.Column(
                                    controls= [
                                        flet.Container(
                                            content= flet.Text("Vanilla Releases", size= 25, font_family= "NoxLauncher", color= "#FFFFFF"),
                                            alignment= flet.alignment.center,
                                            expand_loose= True,
                                        ),
                                        flet.Container(
                                            content= flet.Dropdown(hint_text= "A vanilla release to install!", options= get_vanilla_releases(), border_color= "#717171", border_radius= 10, border_width= 2, hint_style= flet.TextStyle(size= 14, font_family= "NoxLauncher"), on_change= self.install),
                                            alignment= flet.alignment.center,
                                            expand_loose= True,
                                            padding= flet.padding.only(left= 40, right= 40, bottom= 25)
                                        ),
                                        flet.Container(
                                            content= flet.Text("Vanilla Snapshots", size= 25, font_family= "NoxLauncher", color= "#FFFFFF"),
                                            alignment= flet.alignment.center,
                                            expand_loose= True,
                                        ),
                                        flet.Container(
                                            content= flet.Dropdown(hint_text= "A vanilla snapshot to install!", options= get_vanilla_snapshots(), border_color= "#717171", border_radius= 10, border_width= 2, hint_style= flet.TextStyle(size= 14, font_family= "NoxLauncher"), on_change= self.install),
                                            alignment= flet.alignment.center,
                                            expand_loose= True,
                                            padding= flet.padding.only(left= 10, right= 10, bottom= 20)
                                        )
                                    ],
                                    expand= True,
                                    expand_loose= True,
                                    horizontal_alignment= flet.CrossAxisAlignment.CENTER
                                ),
                                width= 480,
                                height= 280,
                                bgcolor= "#272727",
                                border_radius= 20,
                                padding= 20
                            )
                        ],
                        expand= True,
                        expand_loose= True,
                        alignment= flet.MainAxisAlignment.CENTER,
                        horizontal_alignment= flet.CrossAxisAlignment.CENTER
                    ),
                    image= flet.DecorationImage(src= "assets/bgvanilla.png", fit= flet.ImageFit.COVER, filter_quality= flet.FilterQuality.HIGH, repeat= flet.ImageRepeat.NO_REPEAT),
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

        installer_alert: flet.AlertDialog =  flet.AlertDialog(
            modal= True,
            icon= flet.Image(src= "assets/mods.png", width= 160, height= 130, filter_quality= flet.FilterQuality.HIGH),
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
            )
        )

        self.page.open(installer_alert)

        def setStatus(status: str) -> None:

            status_text.value = status
            status_text.update()

        try:

            minecraft_launcher_lib.install.install_minecraft_version(event.control.value, get_home(), {"setStatus": setStatus})

            check_noxlauncher_filesystem()

            minecraft_launcher_lib.vanilla_launcher.add_vanilla_launcher_profile(get_home() + "/", {
                "name": event.control.value,
                "version": event.control.value,
                "versionType": "custom"
            })

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