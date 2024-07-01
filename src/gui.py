import flet
import platform
import os
import json
import minecraft_launcher_lib as mc

from linux.fs import Linux
from skinlib.skin import Skin, Perspective
from constants import constants
from typing import Dict, List
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
                case "/news": page.views.append(flet.View(padding= 0))
                case "/info": page.views.append(NoxLauncher.info(page))

            page.update()

        page.on_view_pop = pop
        page.on_route_change = routing

        page.go("/play")

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

        JAVA_INFO: List[str] = Linux.get_java_info()

        if len(JAVA_INFO[0]) >= 20: JAVA_INFO[0] = JAVA_INFO[0][:19] + "..."
        if len(JAVA_INFO[1]) >= 20: JAVA_INFO[1] = JAVA_INFO[1][:19] + "..."

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
                        height= 600, 
                        bgcolor= "#272727", 
                        border_radius= 20, 
                        alignment= flet.alignment.center,
                        padding= flet.padding.all(20), 
                        content= flet.Column(expand= True, expand_loose= True, spacing= 5,
                            controls= [
                                flet.Container(content= flet.Text("Settings", size= 30, color= "#ffffff", font_family= "Minecraft"), expand_loose= True, alignment= flet.alignment.center),
                                flet.Row(expand_loose= True, height= 100, controls= [
                                    flet.Image(
                                        src= "java.png", 
                                        width= 70, 
                                        height= 70,
                                        filter_quality= flet.FilterQuality.HIGH
                                    ),
                                    flet.Column(
                                        controls= [
                                            flet.Text(f"Location: {JAVA_INFO[0]}", size= 20, color= "#ffffff", font_family= "Minecraft"),
                                            flet.Text(f"Arguments: {JAVA_INFO[1]}", size= 20, color= "#ffffff", font_family= "Minecraft")
                                        ],
                                        spacing= 10,
                                        horizontal_alignment= flet.MainAxisAlignment.CENTER,
                                        alignment= flet.MainAxisAlignment.CENTER,
                                        expand= True,
                                        expand_loose= True,
                                    ),
                                ], spacing= 20, vertical_alignment= flet.CrossAxisAlignment.CENTER),
                                flet.Text("Java source", size= 20, color= "#ffffff", font_family= "Minecraft"),
                                flet.Dropdown(label= "Java source", hint_text= "Select the Java source!", options= [flet.dropdown.Option("System"), flet.dropdown.Option("Custom")], border_color= "#717171", border_radius= 10, label_style= flet.TextStyle(color= "#ffffff"))
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

            account_rename.disabled = True
            account_rename.update()

            event.control.disabled = True
            event.control.update()

            if account_rename is not None:

                AccountManager.rename(account_rename.value.replace(" ", "_"))
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

        if len(ACC["name"]) >= 6: ACC["name"] = ACC["name"][:5] + "..."

        return flet.View("/play", 
            controls= [
                flet.Container(content = flet.Row(expand= True, expand_loose= True, controls= NoxLauncher.minecraft_news(), 
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
                    flet.TextButton(content= flet.Text("Install", size= 25, font_family= "Minecraft"), style= flet.ButtonStyle(bgcolor= "#148b47", color= "#ffffff", shape= flet.RoundedRectangleBorder(radius= 5)), width= 150, height= 45),
                    flet.Container(expand= True),
                    flet.Dropdown(label= "Installed Versions", hint_text= "Minecraft version to play!", options= [flet.dropdown.Option("1.16.5")], border_color= "#717171", border_radius= 10, label_style= flet.TextStyle(color= "#ffffff")),
                    flet.TextButton(content= flet.Text("Play", size= 25, font_family= "Minecraft"), style= flet.ButtonStyle(bgcolor= "#148b47", color= "#ffffff", shape= flet.RoundedRectangleBorder(radius= 5)), width= 150, height= 45),
                    flet.Container(expand= True),
                    flet.Container(expand= True, border_radius= 20, 
                        border= flet.border.all(1, "#717171"), 
                        content= flet.Row(expand= True, spacing= 0, controls= [
                            skin,
                            flet.TextButton(
                                content= flet.Text(ACC["name"], 
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
    
    def minecraft_news() -> List[flet.Container]:

        containers: List[flet.Container] = []

        for articles in mc.utils.get_minecraft_news(10).values():
            if type(articles) is not int:
                for article in articles:
                    
                    containers.append(flet.Container(
                        content= flet.Column(controls= [
                            flet.Text(article["default_tile"]["title"], size= 15, color= "#ffffff", font_family= "Minecraft"),
                            flet.FilledButton(text= "Read", icon= flet.icons.OPEN_IN_NEW, icon_color= "#ffffff", url_target= "article", url= "https://minecraft.net" + article["article_url"], style= flet.ButtonStyle(bgcolor= "#148b47", color= "#ffffff", shape= flet.RoundedRectangleBorder(radius= 5)), width= 120, height= 40),
                        ], spacing= 8),
                        height= 180,
                        width= 180,
                        border_radius= 20,
                        bgcolor= "#272727",
                        padding= flet.padding.all(20)
                    ))

        return containers
    
class AccountManager:

    def offline() -> Dict[str, str]:

        match platform.system():
            case "Windows":
                ...
            case "Linux":
                if not os.path.exists(constants.LINUX_HOME.value + "/Nox Launcher/settings/profiles/profiles.json"): Linux.config()

                with open(constants.LINUX_HOME.value + "/Nox Launcher/settings/profiles/profiles.json", "r") as f:
                    profiles = json.load(f)

                    if "profiles" in profiles.keys():
                        if type(profiles["profiles"]) is dict:
                            if len(profiles["profiles"]) > 0:
                                if "default" in profiles["profiles"].keys():
                                    if isinstance(profiles["profiles"]["default"], dict):
                                        if "type" in profiles["profiles"]["default"].keys():
                                            if profiles["profiles"]["default"]["type"] == "offline": return profiles["profiles"]["default"]
                                        else:
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
                                            
                                    else:

                                        profiles["profiles"].update({
                                            "default": {
                                                "name": "Default",
                                                "type": "offline",
                                                "selected": True,
                                                "skin": constants.LINUX_HOME.value + "/Nox Launcher/skins/steve.png"
                                            }
                                        })
                                        with open(constants.LINUX_HOME.value + "/Nox Launcher/settings/profiles/profiles.json", "w") as f:
                                            json.dump(profiles, f, indent= 4)

                                        return profiles["profiles"]["default"]        

    def determinate() -> Dict[str, str]:

        match platform.system():
            case "Windows":
                ...
            case "Linux":
                if not os.path.exists(constants.LINUX_HOME.value + "/Nox Launcher/settings/profiles/profiles.json"): Linux.config()

                with open(constants.LINUX_HOME.value + "/Nox Launcher/settings/profiles/profiles.json", "r") as f:
                    profiles = json.load(f)

                    if "profiles" in profiles.keys():
                        if type(profiles["profiles"]) is dict:
                            if len(profiles["profiles"]) > 0:
                                for profile in profiles["profiles"].values():
                                    if "selected" in profile:
                                        if profile["selected"] == True:
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
                                    "no-premium": {}
                                })

                                with open(constants.LINUX_HOME.value + "/Nox Launcher/settings/profiles/profiles.json", "w") as f:
                                    json.dump(profiles, f, indent= 4)

                                return profiles["profiles"]["default"]
                        
    def get_all_offlines() -> List[flet.dropdown.Option]:

        match platform.system():
            case "Windows":
                ...
            case "Linux":
                if not os.path.exists(constants.LINUX_HOME.value + "/Nox Launcher/settings/profiles/profiles.json"): Linux.config()

                accounts: List[flet.dropdown.Option] = []

                with open(constants.LINUX_HOME.value + "/Nox Launcher/settings/profiles/profiles.json", "r") as f:
                    profiles = json.load(f)

                    if "profiles" in profiles.keys():
                        if type(profiles["profiles"]) is dict:
                            if len(profiles["profiles"]) > 0:
                                for profile in profiles["profiles"].values():
                                    if "type" in profile:
                                        if profile["type"] == "offline":
                                            accounts.append(flet.dropdown.Option(profile["name"]))

                return accounts
    
    def rename(new: str) -> None:

        match platform.system():
            case "Windows":
                ...
            case "Linux":
                if not os.path.exists(constants.LINUX_HOME.value + "/Nox Launcher/settings/profiles/profiles.json"): Linux.config()

                with open(constants.LINUX_HOME.value + "/Nox Launcher/settings/profiles/profiles.json", "r") as f:
                    profiles = json.load(f)

                    if "profiles" in profiles.keys():
                        if type(profiles["profiles"]) is dict:
                            if len(profiles["profiles"]) > 0:
                                for profile in profiles["profiles"].values():
                                    if "selected" in profile:
                                        if profile["selected"] == True:
                                            AccountManager.delete_skin_from_cache(profile["name"])
                                            profile["name"] = new
                                            break

                                with open(constants.LINUX_HOME.value + "/Nox Launcher/settings/profiles/profiles.json", "w") as f: 
                                    json.dump(profiles, f, indent= 4)

    def select(name: str) -> Dict[str, str]:

        match platform.system():
            case "Windows":
                ...
            case "Linux":
                if not os.path.exists(constants.LINUX_HOME.value + "/Nox Launcher/settings/profiles/profiles.json"): Linux.config()

                with open(constants.LINUX_HOME.value + "/Nox Launcher/settings/profiles/profiles.json", "r") as f:
                    profiles = json.load(f)

                    if "profiles" in profiles.keys():
                        if type(profiles["profiles"]) is dict:
                            if len(profiles["profiles"]) > 0:
                                for profile in profiles["profiles"].values():
                                    if "selected" in profile:
                                        profile["selected"] = False

                                with open(constants.LINUX_HOME.value + "/Nox Launcher/settings/profiles/profiles.json", "w") as f: 
                                    json.dump(profiles, f, indent= 4)

                                for profile in profiles["profiles"].values():
                                    if "name" in profile:
                                        if profile["name"] == name:
                                            profile["selected"] = True
                                            with open(constants.LINUX_HOME.value + "/Nox Launcher/settings/profiles/profiles.json", "w") as f: 
                                                json.dump(profiles, f, indent= 4)

                                            return profile
                    
    def get_skin(skin: str, name: str, size: int = 20, width: int = 50, height: int = 50) -> flet.Image:

        skin: Skin = Skin.from_image(Image.open(skin).convert("RGBA"))

        perspective: Perspective = Perspective(
            x= "left",
            y= "front",
            z= "up",
            scaling_factor= size
        )

        skin.to_isometric_image(perspective).save(f"{constants.LINUX_HOME.value}/Nox Launcher/cache/{name}.png")

        if os.path.exists(os.path.dirname(__file__) + "/test.png") or os.path.exists(os.path.dirname(os.path.dirname(__file__)) + "/test.png"):
            os.remove(os.path.dirname(__file__) + "/test.png")
            os.remove(os.path.dirname(os.path.dirname(__file__)) + "/test.png")

        return flet.Image(src= f"{constants.LINUX_HOME.value}/Nox Launcher/cache/{name}.png", width= width, height= height)
    
    def delete_skin_from_cache(name: str) -> None:

        match platform.system():
            case "Windows":
                ...
            case "Linux":
                if os.path.exists(f"{constants.LINUX_HOME.value}/Nox Launcher/cache/{name}.png"):
                    os.remove(f"{constants.LINUX_HOME.value}/Nox Launcher/cache/{name}.png")
