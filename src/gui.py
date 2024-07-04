import flet
import platform
import os
import json
import time

from fs import Config
from skinlib.skin import Skin, Perspective
from constants import constants
from typing import Any, Dict, List
from PIL import Image

class NoxLauncher: 

    def build(page: flet.Page) -> None:

        def pop(_: flet.View) -> None:
            page.views.pop()
            page.go(page.views[-1].route)

        def routing(_: flet.RouteChangeEvent) -> None:
            page.views.clear()

            match page.route:
                case "/play": page.views.append(NoxLauncher.play(page))
                case "/settings": page.views.append(NoxLauncher.settings(page))
                case "/accounts": page.views.append(NoxLauncher.accounts(page))
                case "/offline": page.views.append(NoxLauncher.offline(page))
                case "/news": page.views.append(NoxLauncher.news(page))
                case "/info": page.views.append(NoxLauncher.info(page))
                case "/install": page.views.append(NoxLauncher.install(page))

            page.update()

        page.on_view_pop = pop
        page.on_route_change = routing

        page.go("/play")

    def news(page: flet.Page) -> flet.View:

        return flet.View(
            controls= [
                flet.Container(
                    height= 80,
                    expand_loose= True,
                    content= flet.Row(
                        controls= [
                            flet.Icon(name= flet.icons.ARROW_BACK, color= "#717171", size= 40),
                            flet.TextButton(content= flet.Text("Back to play", size= 20, font_family= "Minecraft"), style= flet.ButtonStyle(bgcolor= "#148b47", color= "#ffffff", shape= flet.RoundedRectangleBorder(radius= 5)), width= 190, height= 45, on_click= lambda _: page.go("/play")),
                        ],
                        alignment= flet.MainAxisAlignment.START,
                        vertical_alignment= flet.CrossAxisAlignment.CENTER,
                        expand= True,
                        expand_loose= True,
                        spacing= 10
                    ),
                    alignment= flet.alignment.center_left,
                    padding= flet.padding.all(20)
                )
            ],
            padding= 0,
        )

    def install(page: flet.Page) -> flet.View:

        return flet.View(
            controls= [
                flet.Container(
                    height= 80,
                    expand_loose= True,
                    content= flet.Row(
                        controls= [
                            flet.Icon(name= flet.icons.ARROW_BACK, color= "#717171", size= 40),
                            flet.TextButton(content= flet.Text("Back to play", size= 20, font_family= "Minecraft"), style= flet.ButtonStyle(bgcolor= "#148b47", color= "#ffffff", shape= flet.RoundedRectangleBorder(radius= 5)), width= 190, height= 45, on_click= lambda _: page.go("/play")),
                        ],
                        alignment= flet.MainAxisAlignment.START,
                        vertical_alignment= flet.CrossAxisAlignment.CENTER,
                        expand= True,
                        expand_loose= True,
                        spacing= 10
                    ),
                    alignment= flet.alignment.center_left,
                    padding= flet.padding.all(20)
                )
            ],
            padding= 0,
        )

    def info(page: flet.Page) -> flet.View:

        return flet.View(
            controls= [
                flet.Container(
                    height= 80,
                    expand_loose= True,
                    content= flet.Row(
                        controls= [
                            flet.Icon(name= flet.icons.ARROW_BACK, color= "#717171", size= 40),
                            flet.TextButton(content= flet.Text("Back to play", size= 20, font_family= "Minecraft"), style= flet.ButtonStyle(bgcolor= "#148b47", color= "#ffffff", shape= flet.RoundedRectangleBorder(radius= 5)), width= 190, height= 45, on_click= lambda _: page.go("/play")),
                        ],
                        alignment= flet.MainAxisAlignment.START,
                        vertical_alignment= flet.CrossAxisAlignment.CENTER,
                        expand= True,
                        expand_loose= True,
                        spacing= 10
                    ),
                    alignment= flet.alignment.center_left,
                    padding= flet.padding.all(20)
                ),
                flet.Container(
                    expand= True, 
                    expand_loose= True, 
                    alignment= flet.alignment.center,
                    content= flet.Container(
                        width= 500, 
                        height= 560, 
                        bgcolor= "#272727", 
                        border_radius= 20, 
                        alignment= flet.alignment.center,
                        padding= flet.padding.all(20), 
                        content= flet.Column(expand= True, expand_loose= True, spacing= 5,
                            controls= [
                                flet.Container(content= flet.Image(src= "krayson_studio.png", width= 140, height= 140, filter_quality= flet.FilterQuality.HIGH), expand_loose= True, alignment= flet.alignment.center),
                                flet.Container(content= flet.Text("Nox Launcher", size= 30, color= "#ffffff", font_family= "Minecraft"), expand_loose= True, alignment= flet.alignment.center),
                                flet.Container(content= flet.Text("Nox Launcher is a powerful and easy-to-use launcher for Minecraft develop by Krayson Studio.", size= 15, color= "#ffffff", font_family= "Minecraft"), expand_loose= True, alignment= flet.alignment.center),
                                flet.Column(controls= [
                                    flet.Text("Developed by: ", color= "#ffffff", size= 15, font_family= "Minecraft"),
                                    flet.Row(controls= [
                                        flet.TextButton(content= flet.Image(src= "github.png", width= 60, height= 60, filter_quality= flet.FilterQuality.HIGH), width= 60, height= 60, url_target= flet.UrlTarget.BLANK, url= "https://github.com/DevCheckOG"),
                                        flet.Text("DevCheckOG", color= "#ffffff", size= 15, font_family= "Minecraft")
                                    ], expand_loose= True, alignment= flet.MainAxisAlignment.START, vertical_alignment= flet.CrossAxisAlignment.CENTER, spacing= 10),
                                    flet.Row(controls= [
                                        flet.TextButton(content= flet.Image(src= "github.png", width= 60, height= 60, filter_quality= flet.FilterQuality.HIGH), width= 60, height= 60, url_target= flet.UrlTarget.BLANK, url= "https://github.com/aaronwayas"),
                                        flet.Text("AaronWayas", color= "#ffffff", size= 15, font_family= "Minecraft")
                                    ], expand_loose= True, alignment= flet.MainAxisAlignment.START, vertical_alignment= flet.CrossAxisAlignment.CENTER, spacing= 10),
                                    flet.Row(controls= [
                                        flet.TextButton(content= flet.Image(src= "github.png", width= 60, height= 60, filter_quality= flet.FilterQuality.HIGH), width= 60, height= 60, url_target= flet.UrlTarget.BLANK, url= "https://github.com/FrannDV"),
                                        flet.Text("FranDV", color= "#ffffff", size= 15, font_family= "Minecraft")
                                    ], expand_loose= True, alignment= flet.MainAxisAlignment.START, vertical_alignment= flet.CrossAxisAlignment.CENTER, spacing= 10),
                                ], horizontal_alignment= flet.MainAxisAlignment.START, alignment= flet.CrossAxisAlignment.CENTER, spacing= 5, expand_loose= True),
                                flet.Row(
                                    controls= [
                                        flet.TextButton(content= flet.Image(src= "github.png", width= 60, height= 60, filter_quality= flet.FilterQuality.HIGH), width= 60, height= 60),
                                        flet.TextButton(content= flet.Image(src= "discord.png", width= 60, height= 60, filter_quality= flet.FilterQuality.HIGH), width= 60, height= 60, url_target= flet.UrlTarget.BLANK, url= "https://discord.com/invite/DWfuQRsxwb"),
                                        flet.TextButton(content= flet.Image(src= "kofi.png", width= 80, height= 60, filter_quality= flet.FilterQuality.HIGH), width= 60, height= 60, url_target= flet.UrlTarget.BLANK, url= "https://ko-fi.com/kraysonstudios")
                                    ],
                                    alignment= flet.MainAxisAlignment.CENTER,
                                    vertical_alignment= flet.CrossAxisAlignment.CENTER,
                                    spacing= 10,
                                    expand_loose= True
                                )
                            ]
                        )
                    )
                )
            ],
            padding= 0,
            horizontal_alignment= flet.CrossAxisAlignment.CENTER,
            vertical_alignment= flet.CrossAxisAlignment.CENTER
        )

    def settings(page: flet.Page) -> flet.View:

        JAVA_INFO: List[str] | bool = Config.get_java_info()

        def update_java_settings(_: flet.ControlEvent) -> None:

            if java_path.value != "System": 
                Config.update_java_path(java_path.value)
            
            location.value = java_path.value
            location.update()

            java_args.value = " ".join(Config.update_java_memory_dedicated([arg for arg in java_args.value.split(" ") if isinstance(arg, str) and arg != ""], str(round(java_alloc_memory.value))))
            java_args.update()

            def ok(_: flet.ControlEvent) -> None:

                page.close(BANNER)
                page.update()

            BANNER: flet.Banner = flet.Banner(
                bgcolor= "#272727",
                leading= flet.Icon(name= flet.icons.CHECK, color= "#148b47", size= 40),
                content= flet.Text(
                    value= "Java settings updated!",
                    color= "#ffffff",
                    size= 20,
                    font_family= "Minecraft"
                ),
                actions= [
                    flet.TextButton(content= flet.Text("Ok", size= 20, font_family= "Minecraft"), style= flet.ButtonStyle(bgcolor= "#148b47", color= "#ffffff", shape= flet.RoundedRectangleBorder(radius= 5)), width= 150, height= 40, on_click= ok)
                ]
            )

            page.open(BANNER)

        if JAVA_INFO is False:

            page.open(flet.AlertDialog(
                modal= True,
                icon= flet.Icon(name= flet.icons.ERROR_ROUNDED, color= flet.colors.RED_ACCENT, size= 40),
                title= flet.Container(
                    content= flet.Text("Corrupted java settings", size= 25, font_family= "Minecraft"),
                    alignment= flet.alignment.center,
                    expand_loose= True
                ),
                bgcolor= "#272727",
                content= flet.Text("Reopen the launcher for fixed the settings!", size= 20, font_family= "Minecraft"),
                actions= [
                    flet.TextButton(content= flet.Text("Ok", size= 20, font_family= "Minecraft"), style= flet.ButtonStyle(bgcolor= "#148b47", color= "#ffffff", shape= flet.RoundedRectangleBorder(radius= 5)), width= 120, height= 45, on_click= lambda _: page.window.destroy()),
                ],
                on_dismiss= lambda _: page.window.destroy()
            ))

            return flet.View()

        java_args: flet.TextField = flet.TextField(value= " ".join(JAVA_INFO[1]), multiline= False, expand_loose= True, height= 70, border_radius= 10, border_color= "#717171")
        java_path: flet.Dropdown = flet.Dropdown(label= "Java source", hint_text= "Select the Java source!", options= Config.get_java_list(), border_color= "#717171", border_radius= 10, label_style= flet.TextStyle(color= "#ffffff"), value= Config.determinate_java_path(JAVA_INFO[0]))
        java_alloc_memory: flet.Slider = flet.Slider(value= Config.parse_memory(JAVA_INFO[1]), min= 1000, max= Config.get_memory_ram(), label= "{value}MB", expand_loose= True, height= 40, divisions= 500, active_color= "#148b47", thumb_color= "#ffffff")
        location: flet.Text = flet.Text(f"Location: {JAVA_INFO[0][:14] + "..."}", size= 20, color= "#ffffff", font_family= "Minecraft")

        return flet.View(
            controls= [
                flet.Container(
                    height= 80,
                    expand_loose= True,
                    content= flet.Row(
                        controls= [
                            flet.Icon(name= flet.icons.ARROW_BACK, color= "#717171", size= 40),
                            flet.TextButton(content= flet.Text("Back to play", size= 20, font_family= "Minecraft"), style= flet.ButtonStyle(bgcolor= "#148b47", color= "#ffffff", shape= flet.RoundedRectangleBorder(radius= 5)), width= 190, height= 45, on_click= lambda _: page.go("/play")),
                        ],
                        alignment= flet.MainAxisAlignment.START,
                        vertical_alignment= flet.CrossAxisAlignment.CENTER,
                        expand= True,
                        expand_loose= True,
                        spacing= 10
                    ),
                    alignment= flet.alignment.center_left,
                    padding= flet.padding.all(20)
                ),
                flet.Container(
                    expand= True, 
                    expand_loose= True, 
                    alignment= flet.alignment.center,
                    content= flet.Container(
                        width= 500, 
                        height= 560, 
                        bgcolor= "#272727", 
                        border_radius= 20, 
                        alignment= flet.alignment.center,
                        padding= flet.padding.all(20), 
                        content= flet.Column(expand= True, expand_loose= True, spacing= 5,
                            controls= [
                                flet.Container(content= flet.Text("Settings", size= 30, color= "#ffffff", font_family= "Minecraft"), expand_loose= True, alignment= flet.alignment.center),
                                flet.Row(expand_loose= True, height= 100, controls= [
                                    flet.Container(content= flet.Image(
                                        src= "java.png", 
                                        width= 90, 
                                        height= 90,
                                        filter_quality= flet.FilterQuality.HIGH
                                    ), alignment= flet.alignment.center_left, padding= flet.padding.only(bottom= 28)),
                                    flet.Container(content= location, expand_loose= True, alignment= flet.alignment.center_left, expand= True),
                                ], vertical_alignment= flet.CrossAxisAlignment.CENTER, alignment= flet.MainAxisAlignment.CENTER),
                                flet.Text("Java settings", size= 20, color= "#ffffff", font_family= "Minecraft"),
                                java_path,
                                flet.Text("JVM arguments", size= 20, color= "#ffffff", font_family= "Minecraft"),
                                java_args,
                                flet.Container(content= flet.Text("Memory dedicated", size= 20, color= "#ffffff", font_family= "Minecraft"), expand_loose= True, alignment= flet.alignment.center),
                                java_alloc_memory,
                                flet.Container(content= flet.TextButton(content= flet.Text("Save", size= 20, font_family= "Minecraft"), on_click= update_java_settings, style= flet.ButtonStyle(bgcolor= "#148b47", color= "#ffffff", shape= flet.RoundedRectangleBorder(radius= 5)), width= 190, height= 45), alignment= flet.alignment.center, expand_loose= True, expand= True)
                            ]
                        )
                    )
                )
            ],
            padding= 0,
            horizontal_alignment= flet.MainAxisAlignment.CENTER, 
            vertical_alignment= flet.CrossAxisAlignment.CENTER
        )
    
    def accounts(page: flet.Page) -> flet.View:

        ACC: Dict[str, str] = AccountManager.determinate()
        skin: flet.Image = AccountManager.get_skin(ACC["skin"], ACC["name"], size= 50, width= 120, height= 120)

        return flet.View("/accounts",  
            controls= [
                flet.Container(expand= True, expand_loose= True, alignment= flet.alignment.center, 
                content= flet.Container(width= 420, height= 420, bgcolor= "#272727", border_radius= 20, alignment= flet.alignment.center,
                padding= flet.padding.all(20), 
                content= flet.Column(expand= True, expand_loose= True, spacing= 5,
                controls= [
                    flet.Container(content= flet.Text("Accounts", size= 30, color= "#ffffff", font_family= "Minecraft"), expand_loose= True, alignment= flet.alignment.center),
                    flet.Row(controls= [
                            skin, 
                            flet.Container(expand_loose= True),
                            flet.Column(controls= [
                            flet.Text(ACC["name"], size= 20, color= "#ffffff", font_family= "Minecraft"),
                            flet.Text("Type: " + ACC["type"], size= 20, color= "#ffffff", font_family= "Minecraft"),
                        ],
                        expand_loose= True),
                    ], spacing= 5, expand_loose= True),
                    flet.Container(expand= True),
                    flet.Container(content= flet.Column(controls= [
                        flet.TextButton(content= flet.Text("Offline", size= 20, font_family= "Minecraft"), style= flet.ButtonStyle(bgcolor= "#148b47", color= "#ffffff", shape= flet.RoundedRectangleBorder(radius= 5)), width= 190, height= 45, on_click= lambda _: page.go("/offline")),
                        flet.TextButton(content= flet.Text("Auth", size= 20, font_family= "Minecraft"), style= flet.ButtonStyle(bgcolor= "#148b47", color= "#ffffff", shape= flet.RoundedRectangleBorder(radius= 5)), width= 190, height= 45),
                        flet.TextButton(content= flet.Text("Premiun", size= 20, font_family= "Minecraft"), style= flet.ButtonStyle(bgcolor= "#148b47", color= "#ffffff", shape= flet.RoundedRectangleBorder(radius= 5)), width= 190, height= 45),
                        flet.TextButton(content= flet.Text("Back to play", size= 20, font_family= "Minecraft"), style= flet.ButtonStyle(bgcolor= "#148b47", color= "#ffffff", shape= flet.RoundedRectangleBorder(radius= 5)), width= 190, height= 45, on_click= lambda _: page.go("/play")),
                    ], expand_loose= True, expand= True, spacing= 5, alignment= flet.MainAxisAlignment.CENTER), alignment= flet.alignment.center),
                ], alignment= flet.MainAxisAlignment.START)))
            ],
            
       horizontal_alignment= flet.MainAxisAlignment.CENTER, vertical_alignment= flet.CrossAxisAlignment.CENTER, padding= 0)

    def offline(page: flet.Page) -> flet.View:

        ACC: Dict[str, str] = AccountManager.offline()
        skin: flet.Image = AccountManager.get_skin(ACC["skin"], ACC["name"], size= 50, width= 120, height= 120)

        def update_account_info(account: Dict[str, str]) -> None:

            global ACC, skin
            
            for control in skin_row.controls:

                if isinstance(control, flet.Image):
                    ACC = AccountManager.offline()
                    skin = AccountManager.get_skin(account["skin"], account["name"], size= 50, width= 120, height= 120)

                    skin_row.controls.insert(skin_row.controls.index(control), skin)
                    skin_row.controls.pop(skin_row.controls.index(control))

                    skin_row.update()
                    break
            
            for control in skin_row.controls:
                
                if isinstance(control, flet.Column):
                    for sub_control in control.controls:

                        if isinstance(sub_control, flet.Text):
                            if sub_control.value.startswith("Type: "):
                                sub_control.value = "Type: " + account["type"]
                                sub_control.update()
                            else:
                                sub_control.value = account["name"]
                                sub_control.update()

                    control.update()

        def change_name(event: flet.ControlEvent) -> None:     

            def fix_up_account(_: flet.ControlEvent) -> None:

                page.go("/play")
                time.sleep(1)
                page.go("/settings")       

            account_rename.disabled = True
            account_rename.update()

            event.control.disabled = True
            event.control.update()

            if account_rename is not None:

                rename: bool = AccountManager.rename(account_rename.value.replace(" ", "_"))

                if not rename:

                    page.open(flet.AlertDialog(
                        modal= True,
                        icon= flet.Icon(name= flet.icons.ERROR_ROUNDED, color= flet.colors.RED_ACCENT, size= 40),
                        title= flet.Container(
                            content= flet.Text("Corrupted account settings", size= 25, font_family= "Minecraft"),
                            alignment= flet.alignment.center,
                            expand_loose= True
                        ),
                        bgcolor= "#272727",
                        content= flet.Text("Corrupted account settings, press ok to fix up!", size= 20, font_family= "Minecraft"),
                        actions= [
                            flet.TextButton(content= flet.Text("Ok", size= 20, font_family= "Minecraft"), style= flet.ButtonStyle(bgcolor= "#148b47", color= "#ffffff", shape= flet.RoundedRectangleBorder(radius= 5)), width= 120, height= 45, on_click= fix_up_account),
                        ],
                        on_dismiss= fix_up_account
                    ))

                    return

                update_account_info(AccountManager.select(account_rename.value.replace(" ", "_")))

                def ok(_: flet.ControlEvent) -> None:

                    page.close(BANNER)
                    page.update()

                    account_rename.disabled = False
                    account_rename.value = ""
                    account_rename.update()

                    event.control.disabled = False
                    event.control.update()
                
                BANNER: flet.Banner = flet.Banner(
                    bgcolor= "#272727",
                    leading= flet.Icon(name= flet.icons.CHECK, color= "#148b47", size= 40),
                    content= flet.Text(
                        value= "Account correctly renamed!",
                        color= "#ffffff",
                        size= 20,
                        font_family= "Minecraft"
                    ),
                    actions= [
                        flet.TextButton(content= flet.Text("Ok", size= 20, font_family= "Minecraft"), style= flet.ButtonStyle(bgcolor= "#148b47", color= "#ffffff", shape= flet.RoundedRectangleBorder(radius= 5)), width= 150, height= 40, on_click= ok)
                    ]
                )

                page.open(BANNER)
            
            else:
            
                def ok(_: flet.ControlEvent) -> None:

                    page.close(BANNER)
                    page.update()

                    account_rename.disabled = False
                    account_rename.update()

                    event.control.disabled = False
                    event.control.update()
                
                BANNER: flet.Banner = flet.Banner(
                    bgcolor= "#272727",
                    leading= flet.Icon(name= flet.icons.WARNING_AMBER_ROUNDED, color= flet.colors.YELLOW_400, size= 40),
                    content= flet.Text(
                        value= "Account name cannot be empty!",
                        color= "#ffffff",
                        size= 20,
                        font_family= "Minecraft"
                    ),
                    actions= [
                        flet.TextButton(content= flet.Text("Ok", size= 20, font_family= "Minecraft"), style= flet.ButtonStyle(bgcolor= "#148b47", color= "#ffffff", shape= flet.RoundedRectangleBorder(radius= 5)), width= 150, height= 40, on_click= ok)
                    ]
                )

                page.open(BANNER)

        account_rename: flet.TextField = flet.TextField(value= "New name", multiline= False, max_length= 15, width= 250, height= 70, border_radius= 10, border_color= "#717171")

        skin_row: flet.Row = flet.Row(controls= [
            skin, 
            flet.Container(expand_loose= True),
            flet.Column(controls= [
                flet.Text(ACC["name"], size= 20, color= "#ffffff", font_family= "Minecraft"),
                flet.Text("Type: " + ACC["type"], size= 20, color= "#ffffff", font_family= "Minecraft"),
            ], expand_loose= True)], 
            spacing= 5, 
            expand_loose= True
        )

        back_to_play_button: flet.Container = flet.Container(expand_loose= True, alignment= flet.alignment.center,
            content= flet.Row(
                controls= [
                    flet.Icon(name= flet.icons.ARROW_BACK, color= "#717171", size= 40),
                    flet.TextButton(content= flet.Text("Back to accounts", size= 20, font_family= "Minecraft"), style= flet.ButtonStyle(bgcolor= "#148b47", color= "#ffffff", shape= flet.RoundedRectangleBorder(radius= 5)), width= 250, height= 45, on_click= lambda _: page.go("/accounts")),
                ],
                expand_loose= True,
                expand= True,
                alignment= flet.MainAxisAlignment.CENTER
            ),
            padding= flet.padding.only(right= 50)               
        )

        main_column: flet.Column = flet.Column(expand= True, expand_loose= True, spacing= 20, controls= [
            flet.Container(content= flet.Text("Offline", size= 30, color= "#ffffff", font_family= "Minecraft"), expand_loose= True, alignment= flet.alignment.center),
            skin_row,
            flet.Container(height= 150, expand_loose= True, alignment= flet.alignment.center,
                content= flet.Column(
                    controls= [
                        flet.Text("Edit Account Name", size= 18, color= "#ffffff", font_family= "Minecraft"),
                        account_rename,
                        flet.IconButton(icon= flet.icons.CHECK, icon_color= "#717171", icon_size= 30, on_click= change_name)
                    ], 
                    spacing= 5, 
                    expand_loose= True, 
                    height= 150
                )
            ),
            back_to_play_button
        ])

        main_container: flet.Container = flet.Container(width= 520, height= 450, bgcolor= "#272727", border_radius= 20, 
            alignment= flet.alignment.center,
            padding= flet.padding.all(20),
            content= main_column
        )

        return flet.View("/offline",
            controls= [
                flet.Container(expand= True, expand_loose= True, alignment= flet.alignment.center,
                        content= main_container
                )
            ],

            horizontal_alignment= flet.MainAxisAlignment.CENTER, 
            vertical_alignment= flet.CrossAxisAlignment.CENTER, 
            padding= 0
        )  

    def play(page: flet.Page) -> flet.View:

        ACC: Dict[str, str] = AccountManager.determinate()
        skin: flet.Image = AccountManager.get_skin(ACC["skin"], ACC["name"])

        return flet.View("/play", 
            controls= [
                flet.Container(content = flet.Row(expand= True, expand_loose= True, controls= constants.MINECRAFT_NEWS.value, 
                alignment= flet.MainAxisAlignment.CENTER, vertical_alignment= flet.CrossAxisAlignment.CENTER, spacing= 10, scroll= flet.ScrollMode.AUTO), expand= True, expand_loose= True, alignment= flet.alignment.center),
            ],

            appbar= flet.AppBar(
                title= flet.Text("Nox Launcher", 
                    size= 25, 
                    font_family= "Minecraft"
                ), 
                bgcolor= "#272727", 
                center_title= False,
                actions= [
                    flet.Container(
                        width= 120,
                        height= 40, 
                        border_radius= 20, 
                        border= flet.border.all(1, "#717171"), 
                        alignment= flet.alignment.center,
                        content= flet.Row(
                            expand= True,
                            expand_loose= True,
                            spacing= 12,
                            controls= [
                                flet.IconButton(
                                    icon= flet.icons.INFO,
                                    icon_size= 25,
                                    icon_color= "#717171",
                                    height= 40,
                                    width= 40,
                                    on_click= lambda _: page.go("/info")
                                ),
                                flet.IconButton(
                                    icon= flet.icons.NEWSPAPER_ROUNDED,
                                    icon_size= 25,
                                    icon_color= "#717171",
                                    height= 40,
                                    width= 40,
                                ),
                            ],
                            alignment= flet.MainAxisAlignment.CENTER,
                            vertical_alignment= flet.CrossAxisAlignment.CENTER
                        )
                    )
                ]
            ),
                                    
            bottom_appbar= flet.BottomAppBar(
                bgcolor= "#272727",
                content= flet.Row(expand= True, spacing= 10, alignment= flet.MainAxisAlignment.CENTER, controls= [
                    flet.TextButton(content= flet.Text("Install", size= 25, font_family= "Minecraft"), style= flet.ButtonStyle(bgcolor= "#148b47", color= "#ffffff", shape= flet.RoundedRectangleBorder(radius= 5)), width= 150, height= 45, on_click= lambda _: page.go("/install")),
                    flet.Container(expand= True),
                    flet.Dropdown(label= "Installed Versions", hint_text= "Minecraft version to play!", options= [flet.dropdown.Option("1.16.5")], border_color= "#717171", border_radius= 10, label_style= flet.TextStyle(color= "#ffffff")),
                    flet.TextButton(content= flet.Text("Play", size= 25, font_family= "Minecraft"), style= flet.ButtonStyle(bgcolor= "#148b47", color= "#ffffff", shape= flet.RoundedRectangleBorder(radius= 5)), width= 150, height= 45),
                    flet.Container(expand= True),
                    flet.Container(expand= True, border_radius= 20, 
                        border= flet.border.all(1, "#717171"), 
                        content= flet.Row(expand= True, spacing= 0, controls= [
                            skin,
                            flet.TextButton(
                                content= flet.Text(ACC["name"][:5] + "..." if len(ACC["name"]) > 5 else ACC["name"], 
                                size= 25, font_family= "Minecraft"), 
                                height= 50, style= flet.ButtonStyle(color= "#ffffff", shape= flet.RoundedRectangleBorder(radius= 5)), 
                                on_click= lambda _: page.go("/accounts"), 
                                expand= True
                            ),
                        ]), 
                        alignment= flet.alignment.center,
                    ),
                    flet.IconButton(icon= flet.icons.SETTINGS_ROUNDED, icon_color= "#717171", icon_size= 30, on_click= lambda _: page.go("/settings")),
                ])
            ), 
            
        padding= 0)
    
class AccountManager:

    def offline() -> Dict[str, str]:

        match platform.system():
            case "Windows":
                if not os.path.exists(constants.WINDOWS_HOME.value + "/Nox Launcher/settings/profiles/profiles.json"): Config.check()

                with open(constants.WINDOWS_HOME.value + "/Nox Launcher/settings/profiles/profiles.json", "r") as f:
                    profiles = json.load(f)

                    if not "profiles" in profiles:
                        profiles["profiles"] = {}
                        with open(constants.WINDOWS_HOME.value + "/Nox Launcher/settings/profiles/profiles.json", "w") as f:
                            json.dump(profiles, f, indent= 4)

                    elif not isinstance(profiles["profiles"], dict):
                        profiles["profiles"] = {}
                        with open(constants.WINDOWS_HOME.value + "/Nox Launcher/settings/profiles/profiles.json", "w") as f:
                            json.dump(profiles, f, indent= 4)

                    if len(profiles["profiles"]) > 0 and "default" in profiles["profiles"]:

                        if not isinstance(profiles["profiles"]["default"], dict): return AccountManager.build_default_offline(profiles)
                        elif "type" not in profiles["profiles"]["default"]: return AccountManager.build_default_offline(profiles)
                        elif not isinstance(profiles["profiles"]["default"]["type"], str) or profiles["profiles"]["default"]["type"] != "offline": return AccountManager.build_default_offline(profiles)
                        elif "selected" not in profiles["profiles"]["default"]: return AccountManager.build_default_offline(profiles)
                        elif not isinstance(profiles["profiles"]["default"]["selected"], bool): return AccountManager.build_default_offline(profiles)
                        
                    return profiles["profiles"]["default"]
            case "Linux":
                if not os.path.exists(constants.LINUX_HOME.value + "/Nox Launcher/settings/profiles/profiles.json"): Config.check()

                with open(constants.LINUX_HOME.value + "/Nox Launcher/settings/profiles/profiles.json", "r") as f:
                    profiles = json.load(f)

                    if not "profiles" in profiles:
                        profiles["profiles"] = {}
                        with open(constants.LINUX_HOME.value + "/Nox Launcher/settings/profiles/profiles.json", "w") as f:
                            json.dump(profiles, f, indent= 4)

                    elif not isinstance(profiles["profiles"], dict):
                        profiles["profiles"] = {}
                        with open(constants.LINUX_HOME.value + "/Nox Launcher/settings/profiles/profiles.json", "w") as f:
                            json.dump(profiles, f, indent= 4)

                    if len(profiles["profiles"]) > 0 and "default" in profiles["profiles"]:

                        if not isinstance(profiles["profiles"]["default"], dict): return AccountManager.build_default_offline(profiles)
                        elif "type" not in profiles["profiles"]["default"]: return AccountManager.build_default_offline(profiles)
                        elif not isinstance(profiles["profiles"]["default"]["type"], str) or profiles["profiles"]["default"]["type"] != "offline": return AccountManager.build_default_offline(profiles)
                        elif "selected" not in profiles["profiles"]["default"]: return AccountManager.build_default_offline(profiles)
                        elif not isinstance(profiles["profiles"]["default"]["selected"], bool): return AccountManager.build_default_offline(profiles)
                        
                        return profiles["profiles"]["default"]
                    
                    return AccountManager.determinate()

    def determinate() -> Dict[str, str]:

        match platform.system():
            case "Windows":
                if not os.path.exists(constants.WINDOWS_HOME.value + "/Nox Launcher/settings/profiles/profiles.json"): Config.check()

                with open(constants.WINDOWS_HOME.value + "/Nox Launcher/settings/profiles/profiles.json", "r") as f:
                    profiles = json.load(f)

                    if not "profiles" in profiles:
                        profiles["profiles"] = {}
                        with open(constants.WINDOWS_HOME.value + "/Nox Launcher/settings/profiles/profiles.json", "w") as f:
                            json.dump(profiles, f, indent= 4)

                    elif not isinstance(profiles["profiles"], dict):
                        profiles["profiles"] = {}
                        with open(constants.WINDOWS_HOME.value + "/Nox Launcher/settings/profiles/profiles.json", "w") as f:
                            json.dump(profiles, f, indent= 4)

                    if len(profiles["profiles"]) > 0:
                        for profile in profiles["profiles"].values():
                            if not isinstance(profile, dict):
                                continue
                            elif not "selected" in profile:
                                profile["selected"] = False
                                continue
                            elif profile["selected"] == True:
                                return profile
                            
                    else:
                        
                        profiles["profiles"].update({
                            "default": {
                                "name": "Default",
                                "type": "offline",
                                "selected": True,
                                "skin": "assets/steve.png"
                            },
                            "premium": {},
                            "no_premium": {}

                        })

                        with open(constants.WINDOWS_HOME.value + "/Nox Launcher/settings/profiles/profiles.json", "w") as f:
                            json.dump(profiles, f, indent= 4)
                            
                        return profiles["profiles"]["default"]
                    
            case "Linux":
                if not os.path.exists(constants.LINUX_HOME.value + "/Nox Launcher/settings/profiles/profiles.json"): Config.check()

                with open(constants.LINUX_HOME.value + "/Nox Launcher/settings/profiles/profiles.json", "r") as f:
                    profiles = json.load(f)

                    if not "profiles" in profiles:
                        profiles["profiles"] = {}
                        with open(constants.LINUX_HOME.value + "/Nox Launcher/settings/profiles/profiles.json", "w") as f:
                            json.dump(profiles, f, indent= 4)

                    elif not isinstance(profiles["profiles"], dict):
                        profiles["profiles"] = {}
                        with open(constants.LINUX_HOME.value + "/Nox Launcher/settings/profiles/profiles.json", "w") as f:
                            json.dump(profiles, f, indent= 4)

                    if len(profiles["profiles"]) > 0:
                        for profile in profiles["profiles"].values():
                            if not isinstance(profile, dict):
                                continue
                            elif not "selected" in profile:
                                profile["selected"] = False
                                continue
                            elif profile["selected"] == True:
                                return profile
                            
                    else:

                        profiles["profiles"].update({
                            "default": {
                                "name": "Default",
                                "type": "offline",
                                "selected": True,
                                "skin": "assets/steve.png"
                            },
                            "premium": {},
                            "no_premium": {}

                        })

                        with open(constants.LINUX_HOME.value + "/Nox Launcher/settings/profiles/profiles.json", "w") as f:
                            json.dump(profiles, f, indent= 4)
                            
                        return profiles["profiles"]["default"]
                        
    def rename(new: str) -> bool:

        match platform.system():
            case "Windows":
                ...
            case "Linux":
                if not os.path.exists(constants.LINUX_HOME.value + "/Nox Launcher/settings/profiles/profiles.json"): Config.check()

                with open(constants.LINUX_HOME.value + "/Nox Launcher/settings/profiles/profiles.json", "r") as f:
                    profiles = json.load(f)

                    if not "profiles" in profiles:
                        profiles["profiles"] = {}
                        with open(constants.LINUX_HOME.value + "/Nox Launcher/settings/profiles/profiles.json", "w") as f:
                            json.dump(profiles, f, indent= 4)
                    elif not isinstance(profiles["profiles"], dict):
                        profiles["profiles"] = {}
                        with open(constants.LINUX_HOME.value + "/Nox Launcher/settings/profiles/profiles.json", "w") as f:
                            json.dump(profiles, f, indent= 4)

                    if len(profiles["profiles"]) > 0:

                        for profile in profiles["profiles"].values():
                            if "selected" not in profile: continue
                            elif profile["selected"] == True:
                                AccountManager.delete_skin_from_cache(profile["name"])
                                profile["name"] = new
                                break

                        with open(constants.LINUX_HOME.value + "/Nox Launcher/settings/profiles/profiles.json", "w") as f: 
                            json.dump(profiles, f, indent= 4)

                        return True

                    return False

    def select(name: str) -> Dict[str, str]:

        match platform.system():
            case "Windows":
                if not os.path.exists(constants.WINDOWS_HOME.value + "/Nox Launcher/settings/profiles/profiles.json"): Config.check()

                with open(constants.WINDOWS_HOME.value + "/Nox Launcher/settings/profiles/profiles.json", "r") as f:
                    profiles = json.load(f)

                    if "profiles" not in profiles: 

                        profiles["profiles"] = {}
                        with open(constants.WINDOWS_HOME.value + "/Nox Launcher/settings/profiles/profiles.json", "w") as f:
                            json.dump(profiles, f, indent= 4)

                    elif not isinstance(profiles["profiles"], dict):
                        profiles["profiles"] = {}
                        with open(constants.WINDOWS_HOME.value + "/Nox Launcher/settings/profiles/profiles.json", "w") as f:
                            json.dump(profiles, f, indent= 4)

                    if len(profiles["profiles"]) > 0:
                        for profile in profiles["profiles"].values():
                            if "name" not in profile or "selected" not in profile:
                                continue
                            elif profile["name"] == name:
                                profile["selected"] = True
                                with open(constants.WINDOWS_HOME.value + "/Nox Launcher/settings/profiles/profiles.json", "w") as f: 
                                    json.dump(profiles, f, indent= 4)

                                return profile
                    
                    return AccountManager.determinate()

            case "Linux":
                if not os.path.exists(constants.LINUX_HOME.value + "/Nox Launcher/settings/profiles/profiles.json"): Config.check()

                with open(constants.LINUX_HOME.value + "/Nox Launcher/settings/profiles/profiles.json", "r") as f:
                    profiles = json.load(f)

                    if "profiles" not in profiles: 

                        profiles["profiles"] = {}
                        with open(constants.LINUX_HOME.value + "/Nox Launcher/settings/profiles/profiles.json", "w") as f:
                            json.dump(profiles, f, indent= 4)

                    elif not isinstance(profiles["profiles"], dict):
                        profiles["profiles"] = {}
                        with open(constants.LINUX_HOME.value + "/Nox Launcher/settings/profiles/profiles.json", "w") as f:
                            json.dump(profiles, f, indent= 4)

                    if len(profiles["profiles"]) > 0:
                        for profile in profiles["profiles"].values():
                            if "name" not in profile or "selected" not in profile:
                                continue
                            elif profile["name"] == name:
                                profile["selected"] = True
                                with open(constants.LINUX_HOME.value + "/Nox Launcher/settings/profiles/profiles.json", "w") as f: 
                                    json.dump(profiles, f, indent= 4)

                                return profile
                    
                    return AccountManager.determinate()

    def build_default_offline(profiles: Dict[str, Any]) -> Dict[str, Any]:

        profiles["profiles"].update({
            "default": {
                "name": "Default",
                "type": "offline",
                "selected": True,
                "skin": "assets/steve.png"
            }
        })
        with open(constants.LINUX_HOME.value + "/Nox Launcher/settings/profiles/profiles.json", "w") as f:
            json.dump(profiles, f, indent= 4)

        return profiles["profiles"]["default"]          

    def get_skin(skin: str, name: str, size: int = 20, width: int = 50, height: int = 50) -> flet.Image:

        skin: Skin = Skin.from_image(Image.open(skin).convert("RGBA"))

        perspective: Perspective = Perspective(
            x= "left",
            y= "front",
            z= "up",
            scaling_factor= size
        )

        image_path = f"{constants.LINUX_HOME.value}/Nox Launcher/cache/{name}.png" if platform.system() == "Linux" else f"{constants.WINDOWS_HOME.value}/Nox Launcher/cache/{name}.png"

        skin.to_isometric_image(perspective).save(image_path)

        if os.path.exists(os.path.dirname(__file__) + "/test.png") or os.path.exists(os.path.dirname(os.path.dirname(__file__)) + "/test.png"):
            os.remove(os.path.dirname(__file__) + "/test.png")
            os.remove(os.path.dirname(os.path.dirname(__file__)) + "/test.png")

        return flet.Image(src= image_path, width= width, height= height)
    
    def delete_skin_from_cache(name: str) -> None:

        match platform.system():
            case "Windows":
                if os.path.exists(f"{constants.WINDOWS_HOME.value}/Nox Launcher/cache/{name}.png"):
                    os.remove(f"{constants.WINDOWS_HOME.value}/Nox Launcher/cache/{name}.png")

            case "Linux":
                if os.path.exists(f"{constants.LINUX_HOME.value}/Nox Launcher/cache/{name}.png"):
                    os.remove(f"{constants.LINUX_HOME.value}/Nox Launcher/cache/{name}.png")
