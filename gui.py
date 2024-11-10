import flet
import os
import time
import uuid
import webbrowser
import threading

from threadpool import NOXLAUNCHER_THREADPOOL
from accounts import FreeACC, Account
from modrinthapi import ModrinthAPI
from constants import *
from fs import *

from typing import Dict, Any

class NoxLauncherStandardWindowConfig: 

    def __init__(self, page: flet.Page) -> None:

        self.page: flet.Page = page

        self.define_standard_config()

    def define_standard_config(self):

        self.page.title = f"NoxLauncher ({DEPLOYMENT_TYPE}) - v{VERSION}"

        self.page.window.icon = os.path.join(os.getcwd().replace("\\", "/"), "assets/icon.ico")

        self.page.fonts = {
            "NoxLauncher": "assets/fonts/minecraft.ttf",
        }
        
        self.page.window.width = 1280
        self.page.window.height = 720

        self.page.theme_mode = flet.ThemeMode.DARK

        self.page.update()

class NoxLauncher:

    def __init__(self, page: flet.Page) -> None:

        self.page: flet.Page = page
        self.routing: NoxLauncherRouting = NoxLauncherRouting(self.page)

        self.build()

    def build(self):

        self.routing.go("/home")

class NoxLauncherRouting:

    def __init__(self, page: flet.Page) -> None:

        self.page: flet.Page = page
        self.build()

    def build(self):

        def routing(_: flet.RouteChangeEvent) -> None:
            self.page.views.clear()

            match self.page.route:
                case "/home": self.append(NoxLauncherHomeGUI(self.page).build())
                case "/settings": self.append(NoxLauncherSettingsGUI(self.page).build())
                case "/play": self.append(NoxLauncherPlayGUI(self.page).build())
                case "/accounts": self.append(NoxLauncherAccountsGUI(self.page).build())
                case "/accounts/free": self.append(NoxLauncherFreeAccountsGUI(self.page).build())
                case "/info": self.append(NoxLauncherInfoGUI(self.page).build())
                case "/install": self.append(NoxLauncherInstallGUI(self.page).build())
                case "/install/fabric": self.append(NoxLauncherInstallFabricGUI(self.page).build())
                case "/install/forge": self.append(NoxLauncherInstallForgeGUI(self.page).build())
                case "/install/vanilla": self.append(NoxLauncherInstallVanillaGUI(self.page).build())

            self.page.update()

        self.page.on_route_change = routing

    def append(self, view: flet.View) -> None: self.page.views.append(view)

    def go(self, route: str) -> None: self.page.go(route)

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
                    width= 250,
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
                            flet.IconButton(
                                icon= flet.icons.NEWSPAPER_ROUNDED,
                                icon_size= 26,
                                icon_color= "#717171",
                                height= 42,
                                width= 42,
                                on_click= lambda _: None
                            ),
                            flet.VerticalDivider(color= "#717171", width= 1),
                            flet.IconButton(icon= flet.icons.SETTINGS_ROUNDED, icon_color= "#717171", icon_size= 30, on_click= lambda _: self.page.go("/settings")),
                            flet.IconButton(icon= flet.icons.FOLDER_OPEN, icon_color= "#717171", icon_size= 30, on_click= open_home)
                        ],
                        alignment= flet.MainAxisAlignment.CENTER,
                        vertical_alignment= flet.CrossAxisAlignment.CENTER
                    )
                )
            ],
            bgcolor= "#272727",
            toolbar_height= 120
        )
    
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
    
class NoxLauncherSettingsGUI:

    def __init__(self, page: flet.Page) -> None:

        self.page: flet.Page = page
        self.jvm_args_input: flet.TextField = flet.TextField(value= " ".join(get_current_jvm_args()), multiline= False, expand_loose= True, height= 70, border_radius= 10, border_color= "#717171", on_submit= self.update_jvm_args)
        self.build()

    def build(self) -> flet.View:

        return flet.View(
            controls= [
                flet.Container(
                    content= flet.Column(
                        controls= [
                            flet.Row(
                                controls= [
                                    BackToPlayButton(self.page).build(),
                                ],
                                height= 140,
                                expand_loose= True
                            ),
                            flet.Row(
                                controls= [
                                    flet.Column(
                                        controls= [
                                            flet.Container(
                                                content= flet.Column(
                                                    controls= [
                                                        flet.Container(
                                                            content= flet.Row(
                                                                controls= [
                                                                    flet.Image(src= "assets/java.png", width= 100, height= 100, filter_quality= flet.FilterQuality.HIGH),
                                                                    flet.Container(content= flet.Text("Java Settings", size= 30, font_family= "NoxLauncher"), expand_loose= True, alignment= flet.alignment.center, padding= flet.padding.only(top= 25))
                                                                ],
                                                                alignment= flet.MainAxisAlignment.CENTER,
                                                                vertical_alignment= flet.CrossAxisAlignment.CENTER,
                                                                expand_loose= True,
                                                                spacing= 30,
                                                                run_spacing= 30
                                                            ),
                                                            expand_loose= True,
                                                            padding= flet.padding.only(top= 20),
                                                            alignment= flet.alignment.center
                                                        ),
                                                        flet.Container(
                                                            content= flet.Text("All Java Instances Available", size= 23, font_family= "NoxLauncher"),
                                                            expand_loose= True,
                                                            alignment= flet.alignment.center_left,
                                                            padding= flet.padding.only(left= 40, top= 30)
                                                        ),
                                                        flet.Container(
                                                            content= flet.Dropdown(hint_text= "Select a Java source!", options= get_all_java_instances(), border_color= "#717171", border_radius= 10, border_width= 2, label_style= flet.TextStyle(color= "#ffffff"), value= get_current_java_instance(), on_change= self.update_java,),
                                                            alignment= flet.alignment.center,
                                                            expand_loose= True,
                                                            padding= flet.padding.only(left= 40, right= 40, bottom= 10)
                                                        ),
                                                        flet.Container(
                                                            content= flet.Text("JVM Arguments", size= 23, font_family= "NoxLauncher"),
                                                            expand_loose= True,
                                                            alignment= flet.alignment.center_left,
                                                            padding= flet.padding.only(left= 40, top= 20)
                                                        ),
                                                        flet.Container(
                                                            content= self.jvm_args_input,
                                                            alignment= flet.alignment.center,
                                                            expand_loose= True,
                                                            padding= flet.padding.only(left= 40, right= 40, bottom= 5)
                                                        ),
                                                        flet.Container(
                                                            content= flet.Slider(value= parse_memory(get_current_jvm_args()), min= 1000, max= get_available_memory_ram(), expand_loose= True, height= 40, active_color= "#148b47", thumb_color= "#ffffff", on_change= self.update_memory_in_jvm_args),
                                                            alignment= flet.alignment.center,
                                                            expand_loose= True,
                                                            padding= flet.padding.only(left= 40, right= 40, bottom= 10)
                                                        )
                                                    ],
                                                    horizontal_alignment= flet.CrossAxisAlignment.CENTER,
                                                    expand= True,
                                                    expand_loose= True
                                                ),
                                                width= 750,
                                                height= 500,
                                                bgcolor= "#272727",
                                                border_radius= 20
                                            )
                                        ]
                                    ),
                                    flet.Container(
                                        expand_loose= True  
                                    ),
                                    flet.Column(
                                        controls= [
                                            flet.Container(
                                                content= flet.Column(
                                                    controls= [
                                                        flet.Image(src= "assets/icon.png", width= 150, height= 130, filter_quality= flet.FilterQuality.HIGH),
                                                        flet.Container(
                                                            content= flet.Text("Close NoxLauncher when Minecraft starts", size= 18, font_family= "NoxLauncher"),
                                                            expand_loose= True,
                                                            alignment= flet.alignment.center_left,
                                                            padding= flet.padding.only(left= 20, right= 20)
                                                        ),
                                                        flet.Container(
                                                            content= flet.Switch(value= get_autoclose(), active_color= "#148b47", on_change= self.update_autoclose),
                                                            expand_loose= True,
                                                            alignment= flet.alignment.center_left,
                                                            padding= flet.padding.only(left= 20, bottom= 10)
                                                        ),
                                                        flet.Container(
                                                            content= flet.Text("Receive yes or no news in the launcher section", size= 18, font_family= "NoxLauncher"),
                                                            expand_loose= True,
                                                            alignment= flet.alignment.center_left,
                                                            padding= flet.padding.only(left= 20, right= 20)
                                                        ),
                                                        flet.Container(
                                                            content= flet.Switch(value= get_receivenews(), active_color= "#148b47", on_change= self.update_receivenews),
                                                            expand_loose= True,
                                                            alignment= flet.alignment.center_left,
                                                            padding= flet.padding.only(left= 20, bottom= 10)
                                                        ),
                                                        flet.Container(
                                                            content= flet.Text("Enable Discord Rich Presence", size= 18, font_family= "NoxLauncher"),
                                                            expand_loose= True,
                                                            alignment= flet.alignment.center_left,
                                                            padding= flet.padding.only(left= 20, right= 20)
                                                        ),
                                                        flet.Container(
                                                            content= flet.Switch(value= get_discordrpc(), active_color= "#148b47", on_change= self.update_discordrpc),
                                                            expand_loose= True,
                                                            alignment= flet.alignment.center_left,
                                                            padding= flet.padding.only(left= 20)
                                                        )
                                                    ],
                                                    horizontal_alignment= flet.CrossAxisAlignment.CENTER,
                                                    expand= True,
                                                    expand_loose= True
                                                ),
                                                width= 380,
                                                height= 500,
                                                bgcolor= "#272727",
                                                border_radius= 20
                                            )
                                        ]
                                    )
                                ],
                                expand= True,
                                expand_loose= True,
                                alignment= flet.MainAxisAlignment.CENTER,
                                vertical_alignment= flet.CrossAxisAlignment.CENTER
                            ),
                        ],  
                        expand= True,
                        expand_loose= True
                    ),
                    expand= True,
                    expand_loose= True,
                    image= flet.DecorationImage(src= "assets/bgsettings.png", fit= flet.ImageFit.COVER, filter_quality= flet.FilterQuality.HIGH, repeat= flet.ImageRepeat.NO_REPEAT),
                    alignment= flet.alignment.center
                )
            ],
            padding= 0
        )
    
    def update_java(self, event: flet.ControlEvent) -> None: update_java(event.control.value)

    def update_jvm_args(self, event: flet.ControlEvent) -> None: update_jvm_args([arg for arg in event.control.value.split(" ") if arg != ""])
    
    def update_memory_in_jvm_args(self, event: flet.ControlEvent) -> None:

        time.sleep(0.5)

        jvm_args: List[str] = get_current_jvm_args()

        if len(jvm_args) >= 2: jvm_args[1] = f"-Xmx{round(event.control.value)}M"

        update_jvm_args(jvm_args)

        self.jvm_args_input.value = " ".join(get_current_jvm_args())
        self.jvm_args_input.update()

    def update_autoclose(self, event: flet.ControlEvent) -> None: update_autoclose(event.control.value)

    def update_receivenews(self, event: flet.ControlEvent) -> None: update_receivenews(event.control.value)

    def update_discordrpc(self, event: flet.ControlEvent) -> None: update_discordrpc(event.control.value)

class NoxLauncherInstallGUI:

    def __init__(self, page: flet.Page) -> None:

        self.page: flet.Page = page
        self.build()

    def build(self) -> flet.View:

        return flet.View(
            appbar= NoxLauncherInstallAppBar(self.page).build(),
            controls= [
                flet.Container(
                    image= flet.DecorationImage(src= "assets/bginstall.png", fit= flet.ImageFit.COVER, filter_quality= flet.FilterQuality.HIGH, repeat= flet.ImageRepeat.NO_REPEAT),
                    expand= True,
                    expand_loose= True,
                    content= flet.Column(
                        controls= [
                            flet.Container(
                                content= flet.Image(
                                    src= "mods.png", 
                                    width= 280, 
                                    height= 180, 
                                    filter_quality= flet.FilterQuality.HIGH,
                                    tooltip= flet.Tooltip(
                                        message= "Welcome to the NoxLauncher Forge, a a simple but powerful system that\n allows you to install mod loaders and mods via modrinth.",
                                        bgcolor= "#272727",
                                        text_style= flet.TextStyle(
                                            size= 14,
                                            color= "#FFFFFF",
                                            font_family= "NoxLauncher"
                                        )
                                    )
                                ),
                                alignment= flet.alignment.center,
                                expand_loose= True
                            ),
                            flet.Container(
                                content= flet.Text("NoxLauncher Forge", size= 40, font_family= "NoxLauncher", color= "#FFFFFF"),
                                alignment= flet.alignment.center,
                                expand_loose= True,
                                padding= flet.padding.only(top= 20),
                            )
                        ],
                        horizontal_alignment= flet.MainAxisAlignment.CENTER,  
                        alignment= flet.MainAxisAlignment.CENTER,
                        expand= True,
                        expand_loose= True
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
                                        width= 500,
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
            )
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
    
class NoxLauncherInstallForgeGUI:

    def __init__(self, page: flet.Page) -> None:

        self.page: flet.Page = page
        self.modrinth: ModrinthAPI = ModrinthAPI(self.page, "forge")
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
                                                    content= flet.Text("Forge Versions", size= 25, font_family= "NoxLauncher", color= "#FFFFFF"),
                                                    alignment= flet.alignment.center,
                                                    expand_loose= True,
                                                ),
                                                flet.Container(
                                                    content= flet.Dropdown(hint_text= "A forge version to install!", options= get_forge_versions(), border_color= "#717171", border_radius= 10, border_width= 2, hint_style= flet.TextStyle(size= 14, font_family= "NoxLauncher"), on_change= self.install),
                                                    alignment= flet.alignment.center,
                                                    expand_loose= True,
                                                    padding= flet.padding.only(left= 40, right= 40, bottom= 25, top= 10)
                                                )
                                            ],
                                            expand= True,
                                            expand_loose= True,
                                            horizontal_alignment= flet.CrossAxisAlignment.CENTER,
                                        ),
                                        width= 480,
                                        height= 170,
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
                                        width= 500,
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
                    image= flet.DecorationImage(src= "assets/bgforge.png", fit= flet.ImageFit.COVER, filter_quality= flet.FilterQuality.HIGH, repeat= flet.ImageRepeat.NO_REPEAT),
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
            icon= flet.Image(src= "assets/forge.png", width= 160, height= 130, filter_quality= flet.FilterQuality.HIGH),
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

            minecraft_launcher_lib.forge.install_forge_version(event.control.value, get_home(), {"setStatus": setStatus})

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
    
class NoxLauncherPlayGUI:

    def __init__(self, page: flet.Page) -> None:

        self.page: flet.Page = page
        self.console: flet.Container = flet.Container(expand= True, expand_loose= True, padding= 15, content= flet.Column(controls= [
            flet.Container(content= flet.Text("Nothing to display yet!", size= 25, font_family= "NoxLauncher", color= "#FFFFFF"), alignment= flet.alignment.center, expand= True, expand_loose= True)
        ], expand= True, expand_loose= True, scroll= flet.ScrollMode.AUTO), alignment= flet.alignment.center)
        self.build()

    def build(self) -> flet.View:

        return flet.View(
            appbar= NoxLauncherGenericAppBar(self.page, "Back to home", "/home").build(),
            controls= [
                flet.Container(
                    content= flet.Column(
                        controls= [
                            flet.Row(
                                controls= [
                                    flet.Container(
                                        content= flet.Row(
                                            controls= [
                                                flet.Dropdown(hint_text= "Select a version to play!", options= get_minecraft_versions(), border_color= "#717171", border_radius= 10, border_width= 2, hint_style= flet.TextStyle(size= 14, font_family= "NoxLauncher"), on_change= self.build_launch),
                                            ],
                                            expand= True,
                                            expand_loose= True,
                                            alignment= flet.MainAxisAlignment.CENTER,
                                            spacing= 20,
                                            run_spacing= 20
                                        ),
                                        bgcolor= "#272727",
                                        width= 370,
                                        height= 120,
                                        border_radius= 20
                                    ),
                                    flet.Container(
                                        content= flet.Column(
                                            controls= [
                                                flet.Container(
                                                    content= flet.Row(
                                                        controls= [
                                                            flet.Image(src= "console.png", width= 60, height= 60, filter_quality= flet.FilterQuality.HIGH),
                                                            flet.Text("Console", size= 25, font_family= "NoxLauncher", color= "#FFFFFF")  
                                                        ],
                                                        expand_loose= True,
                                                        alignment= flet.MainAxisAlignment.CENTER
                                                    ),
                                                    alignment= flet.alignment.center,
                                                    padding= flet.padding.only(top= 20)
                                                ),
                                                self.console,
                                                flet.Container(
                                                    content= flet.IconButton(icon= flet.icons.COPY, icon_size= 30, icon_color= "#717171", on_click= lambda _: self.page.set_clipboard(self.console.content.controls[0].value, wait_timeout= 60*3) if isinstance(self.console.content.controls[0], flet.Text) else None),
                                                    alignment= flet.alignment.center_right,
                                                    expand_loose= True,
                                                    padding= flet.padding.only(bottom= 20)
                                                )
                                            ],
                                            expand= True,
                                            expand_loose= True,
                                            horizontal_alignment= flet.CrossAxisAlignment.CENTER
                                        ),
                                        bgcolor= "#272727",
                                        width= 520,
                                        height= 560,
                                        border_radius= 20,
                                        padding= flet.padding.only(right= 20)
                                    )
                                ],
                                expand_loose= True,
                                expand= True,
                                spacing= 240,
                                run_spacing= 240,
                                alignment= flet.MainAxisAlignment.CENTER,
                                vertical_alignment= flet.CrossAxisAlignment.CENTER
                            )
                        ],
                        expand= True,
                        expand_loose= True,
                        horizontal_alignment= flet.CrossAxisAlignment.CENTER,
                        alignment= flet.MainAxisAlignment.CENTER
                    ),
                    image= flet.DecorationImage(src= "assets/bgplay.png", fit= flet.ImageFit.COVER, filter_quality= flet.FilterQuality.HIGH, repeat= flet.ImageRepeat.NO_REPEAT),
                    expand= True,
                    expand_loose= True,
                    alignment= flet.alignment.center,
                )
            ],
            padding= 0
        )
    
    def build_launch(self, event: flet.ControlEvent) -> None:

        match Account.get_selected():

            case (acc, "free"):
                FREE_ACC_OPTIONS: Dict[str, Any] = {
                    "username": acc["name"],
                    "uuid": uuid.uuid4().hex,
                    "token": "",
                    'jvmArguments': get_current_jvm_args(),
                    'executablePath': get_current_java_instance()
                }

                if FREE_ACC_OPTIONS["executablePath"] is None:

                    not_java_found_alert: flet.AlertDialog = flet.AlertDialog(
                        icon= flet.Image(src= "assets/java.png", width= 160, height= 130, filter_quality= flet.FilterQuality.HIGH),
                        title= flet.Container(
                            content= flet.Text(value= "Error at java", size= 30, font_family= "NoxLauncher", color= "#FFFFFF"),
                            alignment= flet.alignment.center,
                            expand_loose= True
                        ),
                        bgcolor= "#272727",
                        content= flet.Container(
                            content= flet.Text(value= "Java not found on your system, select a java source at settings section or download a java version at system and restart the launcher.", size= 18, font_family= "NoxLauncher", color= "#717171"),
                            alignment= flet.alignment.center,
                            expand_loose=  True,
                            padding= flet.padding.only(right= 15, left= 15),
                            height= 60
                        ),
                        on_dismiss= lambda _: self.page.close(not_java_found_alert)
                    )

                    self.page.open(not_java_found_alert)

                    return

                self.launch(minecraft_launcher_lib.command.get_minecraft_command(event.control.value, get_home(), FREE_ACC_OPTIONS))

            case (acc, "premiun"): ...

            case _:

                not_selected_acc_alert: flet.AlertDialog = flet.AlertDialog(
                    icon= flet.Image(src= "assets/accounts.png", width= 160, height= 130, filter_quality= flet.FilterQuality.HIGH),
                    title= flet.Container(
                        content= flet.Text(value= "Error at accounts", size= 30, font_family= "NoxLauncher", color= "#FFFFFF"),
                        alignment= flet.alignment.center,
                        expand_loose= True
                    ),
                    bgcolor= "#272727",
                    content= flet.Container(
                        content= flet.Text(value= "First select an account in the accounts section to start the game.", size= 18, font_family= "NoxLauncher", color= "#717171"),
                        alignment= flet.alignment.center,
                        expand_loose=  True,
                        padding= flet.padding.only(right= 15, left= 15),
                        height= 60
                    )
                )

                self.page.open(not_selected_acc_alert)

                return
            
    def launch(self, minecraft_command: List[str]) -> None:

        match get_autoclose():

            case True: self._launch_with_autoclose(minecraft_command)
            case False: self._launch_with_console(minecraft_command)

    def _launch_with_autoclose(self, minecraft_command: List[str]) -> None:
        
        self.page.window.destroy()
        threading.Thread(target= self._execute_mc_in_another_thread, args= [minecraft_command], daemon= True).run()

    def _execute_mc_in_another_thread(self, minecraft_command: List[str]) -> None:
        
        subprocess.call(minecraft_command, stdout= subprocess.PIPE, stderr= subprocess.PIPE, stdin= subprocess.PIPE, text= True)

    def _launch_with_console(self, minecraft_command: List[str]) -> None:

        mc_proccess: subprocess.Popen = subprocess.Popen(minecraft_command, stdout= subprocess.PIPE, stderr= subprocess.PIPE, stdin= subprocess.PIPE, text= True)
        NOXLAUNCHER_THREADPOOL.submit(self._update_console, mc_proccess)

    def _update_console(self, process: subprocess.Popen) -> None:

        self.console.content.controls.pop(0)

        self.console.content.controls.append(
            flet.Text(process.stdout.read(), size= 13, font_family= "NoxLauncher", color= "#FFFFFF")
        )

        self.console.update()

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
                                        flet.Image(src= "assets/freeaccounts.png", width= 240, height= 200, filter_quality= flet.FilterQuality.HIGH, repeat= flet.ImageRepeat.NO_REPEAT), 
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
                                on_click= lambda _: self.page.go("/accounts/free")
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
    
class NoxLauncherFreeAccountsGUI:

    def __init__(self, page: flet.Page) -> None:

        self.page: flet.Page = page
        self.select_account_dropdown: flet.Dropdown = flet.Dropdown(hint_text= "Select a default account!", options= [flet.dropdown.Option(account["name"], text_style= flet.TextStyle(size= 14, font_family= "NoxLauncher")) for account in FreeACC.get_accounts()], border_color= "#717171", border_radius= 10, border_width= 2, hint_style= flet.TextStyle(size= 14, font_family= "NoxLauncher"), on_change= self.select_account)
        self.delete_account_dropdown: flet.Dropdown = flet.Dropdown(hint_text= "Select a account to delete!", options= [flet.dropdown.Option(account["name"], text_style= flet.TextStyle(size= 14, font_family= "NoxLauncher")) for account in FreeACC.get_accounts()], border_color= "#717171", border_radius= 10, border_width= 2, hint_style= flet.TextStyle(size= 14, font_family= "NoxLauncher"), on_change= self.delete_account)
        self.build()

    def build(self) -> flet.View:

        return flet.View(
            appbar= NoxLauncherGenericAppBar(self.page, "Back", "/accounts").build(),
            controls= [
                flet.Container(
                    image= flet.DecorationImage(src= "assets/bgaccounts.png", fit= flet.ImageFit.COVER, filter_quality= flet.FilterQuality.HIGH, repeat= flet.ImageRepeat.NO_REPEAT),
                    content= flet.Row(
                        controls= [
                            flet.Container(
                                content= flet.Column(
                                    controls= [
                                        flet.Container(
                                            content= flet.Row(
                                                controls= [
                                                    flet.Icon(name= flet.icons.CREATE, color= "#717171", size= 40),
                                                    flet.Container(flet.Text("Create Account", size= 25, font_family= "NoxLauncher", color= "#FFFFFF"), alignment= flet.alignment.center, expand_loose= True, padding= flet.padding.only(top= 5)),  
                                                ],
                                                expand_loose= True,
                                                alignment= flet.MainAxisAlignment.CENTER
                                            ),
                                            padding= flet.padding.only(top= 20, bottom= 20)
                                        ),
                                        flet.Container(
                                            content= flet.TextField(multiline= False, expand_loose= True, height= 70, border_radius= 10, border_color= "#717171", label= "Create account by name", label_style= flet.TextStyle(size= 16, font_family= "NoxLauncher", color= "#FFFFFF"), hint_text= "Name of the account", hint_style= flet.TextStyle(size= 16, font_family= "NoxLauncher"), text_style= flet.TextStyle(size= 14, font_family= "NoxLauncher", color= "#FFFFFF"), on_submit= self.create_account),
                                            expand_loose= True,
                                            alignment= flet.alignment.center,
                                            padding= flet.padding.only(left= 15, right= 15)
                                        )
                                    ],
                                    expand= True,
                                    expand_loose= True,
                                    horizontal_alignment= flet.CrossAxisAlignment.CENTER
                                ),
                                bgcolor= "#272727",
                                border_radius= 20,
                                width= 340,
                                height= 180,
                            ),
                            flet.Container(
                                content= flet.Column(
                                    controls= [
                                        flet.Container(
                                            content= flet.Row(
                                                controls= [
                                                    flet.Icon(name= flet.icons.DELETE, color= "#717171", size= 40),
                                                    flet.Container(flet.Text("Delete Account", size= 25, font_family= "NoxLauncher", color= "#FFFFFF"), alignment= flet.alignment.center, expand_loose= True, padding= flet.padding.only(top= 5)) 
                                                ],
                                                expand_loose= True,
                                                alignment= flet.MainAxisAlignment.CENTER
                                            ),
                                            padding= flet.padding.only(top= 20, bottom= 20)
                                        ),
                                        flet.Container(
                                            content= self.delete_account_dropdown,
                                            expand_loose= True,
                                            alignment= flet.alignment.center,
                                            padding= flet.padding.only(left= 15, right= 15)
                                        )
                                    ],
                                    expand= True,
                                    expand_loose= True,
                                    horizontal_alignment= flet.CrossAxisAlignment.CENTER
                                ),
                                bgcolor= "#272727",
                                border_radius= 20,
                                width= 340,
                                height= 180,
                            ),
                            flet.Container(
                                content= flet.Column(
                                    controls= [
                                        flet.Container(
                                            content= flet.Row(
                                                controls= [
                                                    flet.Icon(name= flet.icons.SELECT_ALL, color= "#717171", size= 40),
                                                    flet.Container(flet.Text("Select Account", size= 25, font_family= "NoxLauncher", color= "#FFFFFF"), alignment= flet.alignment.center, expand_loose= True, padding= flet.padding.only(top= 5)) 
                                                ],
                                                expand_loose= True,
                                                alignment= flet.MainAxisAlignment.CENTER
                                            ),
                                            padding= flet.padding.only(top= 20, bottom= 20)
                                        ),
                                        flet.Container(
                                            content= self.select_account_dropdown,
                                            expand_loose= True,
                                            alignment= flet.alignment.center,
                                            padding= flet.padding.only(left= 15, right= 15)
                                        )
                                    ],
                                    expand= True,
                                    expand_loose= True,
                                    horizontal_alignment= flet.CrossAxisAlignment.CENTER
                                ),
                                bgcolor= "#272727",
                                border_radius= 20,
                                width= 340,
                                height= 180,
                            )
                        ],  
                        expand= True,
                        expand_loose= True,
                        alignment= flet.MainAxisAlignment.CENTER,
                        vertical_alignment= flet.CrossAxisAlignment.CENTER,
                        run_spacing= 80,
                        spacing= 80
                    ),
                    expand= True,
                    expand_loose= True,
                    alignment= flet.alignment.center
                ),
            ],
            padding= 0
        )
    
    def create_account(self, event: flet.ControlEvent) -> None:

        if event.control.value.isnumeric() or event.control.value == "" or event.control.value.isspace(): 

            event.control.value = ""
            event.control.update()

            created_account_banner: flet.Banner = flet.Banner(
                bgcolor= "#272727",
                leading= flet.Icon(name= flet.icons.WARNING, color= flet.colors.AMBER_400, size= 40),
                content= flet.Text(
                    value= f"The account name \" {event.control.value} \" is invalid name to minecraft!",
                    color= "#ffffff",
                    size= 20,
                    font_family= "NoxLauncher"
                ),
                actions= [
                    flet.TextButton(content= flet.Text("Ok", size= 20, font_family= "NoxLauncher"), style= flet.ButtonStyle(bgcolor= "#148b47", color= "#ffffff", shape= flet.RoundedRectangleBorder(radius= 5)), width= 150, height= 40, on_click= lambda _: self.page.close(created_account_banner))
                ]
            )

            self.page.open(created_account_banner)

            return

        FreeACC.new(event.control.value)

        created_account_banner: flet.Banner = flet.Banner(
            bgcolor= "#272727",
            leading= flet.Icon(name= flet.icons.CREATE, color= "#717171", size= 40),
            content= flet.Text(
                value= f"Free account \" {event.control.value} \" created successfully!",
                color= "#ffffff",
                size= 20,
                font_family= "NoxLauncher"
            ),
            actions= [
                flet.TextButton(content= flet.Text("Ok", size= 20, font_family= "NoxLauncher"), style= flet.ButtonStyle(bgcolor= "#148b47", color= "#ffffff", shape= flet.RoundedRectangleBorder(radius= 5)), width= 150, height= 40, on_click= lambda _: self.page.close(created_account_banner))
            ]
        )

        self.page.open(created_account_banner)

        self.delete_account_dropdown.options = [flet.dropdown.Option(account["name"], text_style= flet.TextStyle(size= 14, font_family= "NoxLauncher")) for account in FreeACC.get_accounts()]
        self.select_account_dropdown.options = [flet.dropdown.Option(account["name"], text_style= flet.TextStyle(size= 14, font_family= "NoxLauncher")) for account in FreeACC.get_accounts()]

        self.delete_account_dropdown.update()
        self.select_account_dropdown.update()

    def delete_account(self, event: flet.ControlEvent) -> None:

        FreeACC.delete(event.control.value)

        self.delete_account_dropdown.options = [flet.dropdown.Option(account["name"], text_style= flet.TextStyle(size= 14, font_family= "NoxLauncher")) for account in FreeACC.get_accounts()]
        self.select_account_dropdown.options = [flet.dropdown.Option(account["name"], text_style= flet.TextStyle(size= 14, font_family= "NoxLauncher")) for account in FreeACC.get_accounts()]

        self.delete_account_dropdown.update()
        self.select_account_dropdown.update()

        deleted_account_banner: flet.Banner = flet.Banner(
            bgcolor= "#272727",
            leading= flet.Icon(name= flet.icons.DELETE, color= "#717171", size= 40),
            content= flet.Text(
                value= f"Free account \" {event.control.value} \" deleted successfully!",
                color= "#ffffff",
                size= 20,
                font_family= "NoxLauncher"
            ),
            actions= [
                flet.TextButton(content= flet.Text("Ok", size= 20, font_family= "NoxLauncher"), style= flet.ButtonStyle(bgcolor= "#148b47", color= "#ffffff", shape= flet.RoundedRectangleBorder(radius= 5)), width= 150, height= 40, on_click= lambda _: self.page.close(deleted_account_banner))
            ]
        )

        self.page.open(deleted_account_banner)

    def select_account(self, event: flet.ControlEvent) -> None:

        FreeACC.select(event.control.value)

        selected_account_banner: flet.Banner = flet.Banner(
            bgcolor= "#272727",
            leading= flet.Icon(name= flet.icons.SELECT_ALL, color= "#717171", size= 40),
            content= flet.Text(
                value= f"Free account \" {event.control.value} \" is now the default account!",
                color= "#ffffff",
                size= 20,
                font_family= "NoxLauncher"
            ),
            actions= [
                flet.TextButton(content= flet.Text("Ok", size= 20, font_family= "NoxLauncher"), style= flet.ButtonStyle(bgcolor= "#148b47", color= "#ffffff", shape= flet.RoundedRectangleBorder(radius= 5)), width= 150, height= 40, on_click= lambda _: self.page.close(selected_account_banner))
            ]
        )

        self.page.open(selected_account_banner)

""" class NoxLauncherPremiumAccountsGUI:

    def __init__(self, page: flet.Page) -> None:

        self.page: flet.Page = page
        self.select_account_dropdown: flet.Dropdown = flet.Dropdown(hint_text= "Select a default account!", options= [flet.dropdown.Option(account["name"], text_style= flet.TextStyle(size= 14, font_family= "NoxLauncher")) for account in FreeACC.get_accounts()], border_color= "#717171", border_radius= 10, border_width= 2, hint_style= flet.TextStyle(size= 14, font_family= "NoxLauncher"), on_change= self.select_account)
        self.delete_account_dropdown: flet.Dropdown = flet.Dropdown(hint_text= "Select a account to delete!", options= [flet.dropdown.Option(account["name"], text_style= flet.TextStyle(size= 14, font_family= "NoxLauncher")) for account in FreeACC.get_accounts()], border_color= "#717171", border_radius= 10, border_width= 2, hint_style= flet.TextStyle(size= 14, font_family= "NoxLauncher"), on_change= self.delete_account)
        self.build()

    def build(self) -> flet.View:

        return flet.View(
            appbar= NoxLauncherGenericAppBar(self.page, "Back", "/accounts").build(),
            controls= [
                flet.Container(
                    image= flet.DecorationImage(src= "bgaccounts.png", fit= flet.ImageFit.COVER, filter_quality= flet.FilterQuality.HIGH, repeat= flet.ImageRepeat.NO_REPEAT),
                    content= flet.Row(
                        controls= [
                            flet.Container(
                                content= flet.Column(
                                    controls= [
                                        flet.Container(
                                            content= flet.Row(
                                                controls= [
                                                    flet.Icon(name= flet.icons.LOGIN, color= "#717171", size= 40),
                                                    flet.Container(flet.Text("Add Account", size= 25, font_family= "NoxLauncher", color= "#FFFFFF"), alignment= flet.alignment.center, expand_loose= True, padding= flet.padding.only(top= 5)),  
                                                ],
                                                expand_loose= True,
                                                alignment= flet.MainAxisAlignment.CENTER
                                            ),
                                            padding= flet.padding.only(top= 20, bottom= 20)
                                        ),
                                        flet.Container(
                                            content= flet.TextButton(
                                                icon= flet.icons.LOGIN,
                                                icon_color= "#717171",
                                                content= flet.Text("Login", size= 20, font_family= "NoxLauncher", color= "#FFFFFF"),
                                            ),
                                            expand_loose= True,
                                            alignment= flet.alignment.center,
                                            padding= flet.padding.only(left= 15, right= 15)
                                        )
                                    ],
                                    expand= True,
                                    expand_loose= True,
                                    horizontal_alignment= flet.CrossAxisAlignment.CENTER
                                ),
                                bgcolor= "#272727",
                                border_radius= 20,
                                width= 340,
                                height= 180,
                            ),
                            flet.Container(
                                content= flet.Column(
                                    controls= [
                                        flet.Container(
                                            content= flet.Row(
                                                controls= [
                                                    flet.Icon(name= flet.icons.DELETE, color= "#717171", size= 40),
                                                    flet.Container(flet.Text("Delete Account", size= 25, font_family= "NoxLauncher", color= "#FFFFFF"), alignment= flet.alignment.center, expand_loose= True, padding= flet.padding.only(top= 5)) 
                                                ],
                                                expand_loose= True,
                                                alignment= flet.MainAxisAlignment.CENTER
                                            ),
                                            padding= flet.padding.only(top= 20, bottom= 20)
                                        ),
                                        flet.Container(
                                            content= self.delete_account_dropdown,
                                            expand_loose= True,
                                            alignment= flet.alignment.center,
                                            padding= flet.padding.only(left= 15, right= 15)
                                        )
                                    ],
                                    expand= True,
                                    expand_loose= True,
                                    horizontal_alignment= flet.CrossAxisAlignment.CENTER
                                ),
                                bgcolor= "#272727",
                                border_radius= 20,
                                width= 340,
                                height= 180,
                            ),
                            flet.Container(
                                content= flet.Column(
                                    controls= [
                                        flet.Container(
                                            content= flet.Row(
                                                controls= [
                                                    flet.Icon(name= flet.icons.SELECT_ALL, color= "#717171", size= 40),
                                                    flet.Container(flet.Text("Select Account", size= 25, font_family= "NoxLauncher", color= "#FFFFFF"), alignment= flet.alignment.center, expand_loose= True, padding= flet.padding.only(top= 5)) 
                                                ],
                                                expand_loose= True,
                                                alignment= flet.MainAxisAlignment.CENTER
                                            ),
                                            padding= flet.padding.only(top= 20, bottom= 20)
                                        ),
                                        flet.Container(
                                            content= self.select_account_dropdown,
                                            expand_loose= True,
                                            alignment= flet.alignment.center,
                                            padding= flet.padding.only(left= 15, right= 15)
                                        )
                                    ],
                                    expand= True,
                                    expand_loose= True,
                                    horizontal_alignment= flet.CrossAxisAlignment.CENTER
                                ),
                                bgcolor= "#272727",
                                border_radius= 20,
                                width= 340,
                                height= 180,
                            )
                        ],  
                        expand= True,
                        expand_loose= True,
                        alignment= flet.MainAxisAlignment.CENTER,
                        vertical_alignment= flet.CrossAxisAlignment.CENTER,
                        run_spacing= 80,
                        spacing= 80
                    ),
                    expand= True,
                    expand_loose= True,
                    alignment= flet.alignment.center
                ),
            ],
            padding= 0
        )
    
    def create_account(self, event: flet.ControlEvent) -> None:

        if event.control.value.isnumeric() or event.control.value == "" or event.control.value.isspace(): 

            event.control.value = ""
            event.control.update()

            created_account_banner: flet.Banner = flet.Banner(
                bgcolor= "#272727",
                leading= flet.Icon(name= flet.icons.WARNING, color= flet.colors.AMBER_400, size= 40),
                content= flet.Text(
                    value= f"The account name \" {event.control.value} \" is invalid name to minecraft!",
                    color= "#ffffff",
                    size= 20,
                    font_family= "NoxLauncher"
                ),
                actions= [
                    flet.TextButton(content= flet.Text("Ok", size= 20, font_family= "NoxLauncher"), style= flet.ButtonStyle(bgcolor= "#148b47", color= "#ffffff", shape= flet.RoundedRectangleBorder(radius= 5)), width= 150, height= 40, on_click= lambda _: self.page.close(created_account_banner))
                ]
            )

            self.page.open(created_account_banner)

            return

        FreeACC.new(event.control.value)

        created_account_banner: flet.Banner = flet.Banner(
            bgcolor= "#272727",
            leading= flet.Icon(name= flet.icons.CREATE, color= "#717171", size= 40),
            content= flet.Text(
                value= f"Free account \" {event.control.value} \" created successfully!",
                color= "#ffffff",
                size= 20,
                font_family= "NoxLauncher"
            ),
            actions= [
                flet.TextButton(content= flet.Text("Ok", size= 20, font_family= "NoxLauncher"), style= flet.ButtonStyle(bgcolor= "#148b47", color= "#ffffff", shape= flet.RoundedRectangleBorder(radius= 5)), width= 150, height= 40, on_click= lambda _: self.page.close(created_account_banner))
            ]
        )

        self.page.open(created_account_banner)

        self.delete_account_dropdown.options = [flet.dropdown.Option(account["name"], text_style= flet.TextStyle(size= 14, font_family= "NoxLauncher")) for account in FreeACC.get_accounts()]
        self.select_account_dropdown.options = [flet.dropdown.Option(account["name"], text_style= flet.TextStyle(size= 14, font_family= "NoxLauncher")) for account in FreeACC.get_accounts()]

        self.delete_account_dropdown.update()
        self.select_account_dropdown.update()

    def delete_account(self, event: flet.ControlEvent) -> None:

        FreeACC.delete(event.control.value)

        self.delete_account_dropdown.options = [flet.dropdown.Option(account["name"], text_style= flet.TextStyle(size= 14, font_family= "NoxLauncher")) for account in FreeACC.get_accounts()]
        self.select_account_dropdown.options = [flet.dropdown.Option(account["name"], text_style= flet.TextStyle(size= 14, font_family= "NoxLauncher")) for account in FreeACC.get_accounts()]

        self.delete_account_dropdown.update()
        self.select_account_dropdown.update()

        deleted_account_banner: flet.Banner = flet.Banner(
            bgcolor= "#272727",
            leading= flet.Icon(name= flet.icons.DELETE, color= "#717171", size= 40),
            content= flet.Text(
                value= f"Free account \" {event.control.value} \" deleted successfully!",
                color= "#ffffff",
                size= 20,
                font_family= "NoxLauncher"
            ),
            actions= [
                flet.TextButton(content= flet.Text("Ok", size= 20, font_family= "NoxLauncher"), style= flet.ButtonStyle(bgcolor= "#148b47", color= "#ffffff", shape= flet.RoundedRectangleBorder(radius= 5)), width= 150, height= 40, on_click= lambda _: self.page.close(deleted_account_banner))
            ]
        )

        self.page.open(deleted_account_banner)

    def select_account(self, event: flet.ControlEvent) -> None:

        FreeACC.select(event.control.value)

        selected_account_banner: flet.Banner = flet.Banner(
            bgcolor= "#272727",
            leading= flet.Icon(name= flet.icons.SELECT_ALL, color= "#717171", size= 40),
            content= flet.Text(
                value= f"Free account \" {event.control.value} \" is now the default account!",
                color= "#ffffff",
                size= 20,
                font_family= "NoxLauncher"
            ),
            actions= [
                flet.TextButton(content= flet.Text("Ok", size= 20, font_family= "NoxLauncher"), style= flet.ButtonStyle(bgcolor= "#148b47", color= "#ffffff", shape= flet.RoundedRectangleBorder(radius= 5)), width= 150, height= 40, on_click= lambda _: self.page.close(selected_account_banner))
            ]
        )

     self.page.open(selected_account_banner)

"""

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
    
def open_github() -> None: webbrowser.open("https://github.com/KraysonStudios/NoxLauncher")

def open_discord() -> None: webbrowser.open("https://discord.com/invite/DWfuQRsxwb")

def open_kofi() -> None: webbrowser.open("https://ko-fi.com/kraysonstudios")