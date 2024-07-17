try:

    import platform
    import flet
    import os
    import json
    import time
    import uuid
    import subprocess
    import minecraft_launcher_lib
    
    from abs import NoxLauncherView, NoxLauncherContainer, NoxLauncherDropdown, NoxLauncherColumn, NoxLauncherBanner, NoxLauncherRow
    from fs import Config
    from skinlib.skin import Skin, Perspective
    from constants import constants
    from tkinter.messagebox import showerror
    from typing import Any, Callable, Dict, List
    from PIL import Image

except Exception as e: 
    
    print(f"Report this error to the developers: \n{e.args[0]}\n")
    exit(1)

class NoxLauncher: 

    def build(page: flet.Page) -> None:

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

        page.on_route_change = routing
        page.go("/play")

    def news(page: flet.Page) -> flet.View:

        return NoxLauncherView(
            controls= [
                NoxLauncherContainer(
                    height= 80,
                    expand_loose= True,
                    content= NoxLauncherRow(
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

                NoxLauncherColumn(
                    expand= True, 
                    expand_loose= True,
                    alignment= flet.MainAxisAlignment.CENTER,
                    horizontal_alignment= flet.CrossAxisAlignment.CENTER,
                    scroll= flet.ScrollMode.AUTO,
                    controls= []
                )
            ]
        )

    def install(page: flet.Page) -> flet.View:

        global fabric
        global vanilla
        global forge

        forge, fabric, vanilla = False, False, False

        def install_versions(event: flet.ControlEvent) -> None:

            def ok_install(_: flet.ControlEvent) -> None:

                def close() -> None:

                    page.close(INSTALLING_INFO)
                    page.go("/play")

                    SUCCESFULL_BANNER: NoxLauncherBanner = NoxLauncherBanner(
                        bgcolor= "#272727",
                        leading= flet.Icon(name= flet.icons.CHECK, color= '#148b47', size= 40),
                        content= flet.Text(
                            value= "New minecraft version's has been installed!",
                            color= "#ffffff",
                            size= 20,
                            font_family= "Minecraft"
                        ),
                        actions= [
                            flet.TextButton(content= flet.Text("Ok", size= 20, font_family= "Minecraft"), style= flet.ButtonStyle(bgcolor= "#148b47", color= "#ffffff", shape= flet.RoundedRectangleBorder(radius= 5)), width= 150, height= 40, on_click= lambda _: page.close(BANNER))
                        ]
                    )

                    page.open(SUCCESFULL_BANNER)

                page.close(BANNER_INFO)
                page.update()

                event.control.disabled = True
                event.control.update()

                if fabric:
                    constants.FABRIC_SNAPSHOTS.value.disable()
                    constants.FABRIC_RELEASES.value.disable()
                elif vanilla:
                    constants.VANILLA_RELEASES.value.disable()
                    constants.VANILLA_SNAPSHOTS.value.disable()
                elif forge:
                    constants.FORGE.value.disable()

                back_to_play.disabled = True
                back_to_play.update() 

                VERSIONS: flet.Text | NoxLauncherContainer = flet.Text("Waiting for user...", size= 20, font_family= "Minecraft", color= "#ffffff") if (fabric and constants.FABRIC_RELEASES.value.value is not None) or (vanilla and constants.VANILLA_RELEASES.value.value is not None) or (forge and constants.FORGE.value.value is not None) else NoxLauncherContainer()
                SNAPSHOTS: flet.Text | NoxLauncherContainer = flet.Text("Waiting for user...", size= 20, font_family= "Minecraft", color= "#ffffff") if (fabric and constants.FABRIC_SNAPSHOTS.value.value is not None) or (vanilla and constants.VANILLA_SNAPSHOTS.value.value is not None) else NoxLauncherContainer()

                VERSION_DATA: Dict[str, str] | None = {
                    "type": "fabric release" if (constants.FABRIC_RELEASES.value.value is not None) else "vanilla release" if (constants.VANILLA_RELEASES.value.value is not None) else "forge version" if (constants.FORGE.value.value is not None) else None,
                    "version": constants.FABRIC_RELEASES.value.value if (constants.FABRIC_RELEASES.value.value is not None) else constants.VANILLA_RELEASES.value.value if (constants.VANILLA_RELEASES.value.value is not None) else constants.FORGE.value if (constants.FORGE.value.value is not None) else None
                } if (constants.FABRIC_RELEASES.value.value is not None) or (constants.VANILLA_RELEASES.value.value is not None) or (constants.FORGE.value.value is not None) else None

                SNAPSHOT_DATA: Dict[str, str] | None = {
                    "type": "fabric snapshot" if (constants.FABRIC_SNAPSHOTS.value.value is not None) else "vanilla snapshot" if (constants.VANILLA_SNAPSHOTS.value.value is not None) else None,
                    "version": constants.FABRIC_SNAPSHOTS.value.value if (constants.FABRIC_SNAPSHOTS.value.value is not None) else constants.VANILLA_SNAPSHOTS.value.value if (constants.VANILLA_SNAPSHOTS.value.value is not None) else None
                } if (constants.FABRIC_SNAPSHOTS.value.value is not None) or (constants.VANILLA_SNAPSHOTS.value.value is not None) else None

                INSTALLING_INFO: flet.AlertDialog = flet.AlertDialog(
                    modal= True,
                    icon= flet.Icon(name= flet.icons.DOWNLOADING_ROUNDED, color= '#148b47', size= 40),
                    title= NoxLauncherContainer(
                        content= flet.Text("Installing resources..", size= 25, font_family= "Minecraft"),
                        alignment= flet.alignment.center,
                        expand_loose= True
                    ),
                    bgcolor= "#272727",
                    content= NoxLauncherColumn(
                        controls= [
                            NoxLauncherColumn(
                                controls= [
                                    VERSIONS,
                                    flet.ProgressBar(expand_loose= True, color= "#148b47")
                                ],
                                expand_loose= True,
                                alignment= flet.MainAxisAlignment.CENTER,
                                horizontal_alignment= flet.CrossAxisAlignment.CENTER,
                                spacing= 10
                            ) if (constants.FABRIC_RELEASES.value.value is not None) or (constants.VANILLA_RELEASES.value.value is not None) or (constants.FORGE.value.value is not None) else NoxLauncherContainer(),
                            NoxLauncherColumn(
                                controls= [
                                    SNAPSHOTS,
                                    flet.ProgressBar(expand_loose= True, color= "#148b47")
                                ],
                                expand_loose= True,
                                alignment= flet.MainAxisAlignment.CENTER,
                                horizontal_alignment= flet.CrossAxisAlignment.CENTER,
                                spacing= 10
                            ) if (constants.FABRIC_SNAPSHOTS.value.value is not None) or (constants.VANILLA_SNAPSHOTS.value.value is not None) else NoxLauncherContainer()
                        ],
                        spacing= 20,
                        height= 160,
                        width= 600,
                        alignment= flet.MainAxisAlignment.CENTER,
                        horizontal_alignment= flet.CrossAxisAlignment.CENTER
                    ),
                    on_dismiss= lambda _: None
                )

                page.open(INSTALLING_INFO)

                MinecraftDownloader([VERSION_DATA, SNAPSHOT_DATA], [VERSIONS, SNAPSHOTS], close)

            if (fabric and constants.FABRIC_RELEASES.value is None and constants.FABRIC_SNAPSHOTS.value is None) or (vanilla and constants.VANILLA_RELEASES.value is None and constants.VANILLA_SNAPSHOTS.value is None) or (forge and constants.FORGE.value is None): 
    
                BANNER: NoxLauncherBanner = NoxLauncherBanner(
                    bgcolor= "#272727",
                    leading= flet.Icon(name= flet.icons.WARNING_AMBER_ROUNDED, color= flet.colors.YELLOW_400, size= 40),
                    content= flet.Text(
                        value= "Please select a release or snapshot or otherwise leave!",
                        color= "#ffffff",
                        size= 20,
                        font_family= "Minecraft"
                    ),
                    actions= [
                        flet.TextButton(content= flet.Text("Ok", size= 20, font_family= "Minecraft"), style= flet.ButtonStyle(bgcolor= "#148b47", color= "#ffffff", shape= flet.RoundedRectangleBorder(radius= 5)), width= 150, height= 40, on_click= lambda _: page.close(BANNER))
                    ]
                )

                page.open(BANNER)
                return

            banner_info_text: str = ''

            if fabric: banner_info_text = f"The Next versions of Fabric to install:  {constants.FABRIC_RELEASES.value.value if constants.FABRIC_RELEASES.value.value is not None else ''}{f' and {constants.FABRIC_SNAPSHOTS.value.value}' if constants.FABRIC_SNAPSHOTS.value.value is not None else ''}" 
            elif vanilla: banner_info_text = f"The Next versions of Vanilla to install:  {constants.VANILLA_RELEASES.value.value if constants.VANILLA_RELEASES.value.value is not None else ''}{f' and {constants.VANILLA_SNAPSHOTS.value.value}' if constants.VANILLA_SNAPSHOTS.value.value is not None else ''}" 
            elif forge: banner_info_text = f"The next version of Forge to install: {constants.FORGE.value.value}"

            BANNER_INFO: NoxLauncherBanner = NoxLauncherBanner(
                bgcolor= "#272727",
                leading= flet.Icon(name= flet.icons.DOWNLOADING, color= "#148b47", size= 40),
                content= flet.Text(
                    value= banner_info_text,
                    color= "#ffffff",
                    size= 20,
                    font_family= "Minecraft"
                ),
                actions= [
                    flet.TextButton(content= flet.Text("Ok", size= 20, font_family= "Minecraft"), style= flet.ButtonStyle(bgcolor= "#148b47", color= "#ffffff", shape= flet.RoundedRectangleBorder(radius= 5)), width= 150, height= 40, on_click= ok_install)
                ]
            )

            page.open(BANNER_INFO)                

        INSTALL_BUTTON: flet.TextButton = flet.TextButton(content= flet.Text("Install", size= 20, font_family= "Minecraft"), style= flet.ButtonStyle(bgcolor= "#148b47", color= "#ffffff", shape= flet.RoundedRectangleBorder(radius= 5)), width= 190, height= 45, on_click= install_versions)
        
        def select_versions(event: flet.ControlEvent) -> None:

            match event.control.key:

                case "fabric":

                    global fabric
                    fabric = True

                    main_row.controls.clear()
                    main_row.update()

                    main_container.width = 500
                    main_container.height = 460
                    
                    main_container.update()

                    title.value = "Fabric"
                    title.update()

                    title_row.controls.remove(title_icon)
                    title_row.controls.insert(0, flet.Image(src= "fabric.png", width= 50, height= 50, filter_quality= flet.FilterQuality.HIGH))   

                    title_row.update()

                    main_column.controls.remove(main_row)

                    main_column.extend(
                        [   
                            NoxLauncherRow(
                                controls= [
                                    NoxLauncherContainer(
                                        content= flet.Text("Fabric Releases", size= 25, font_family= "Minecraft"), 
                                        expand_loose= True,
                                        alignment= flet.alignment.center, 
                                        padding= flet.padding.all(20)
                                    )

                                ],
                                expand_loose= True,
                                alignment= flet.MainAxisAlignment.CENTER
                            ),
                            constants.FABRIC_RELEASES.value,
                            NoxLauncherRow(
                                controls= [
                                    NoxLauncherContainer(content= 
                                        flet.Text("Fabric Snapshots", size= 25, font_family= "Minecraft"), 
                                        expand_loose= True,
                                        alignment= flet.alignment.center, 
                                        padding= flet.padding.all(20)
                                    )

                                ],
                                expand_loose= True,
                                alignment= flet.MainAxisAlignment.CENTER
                            ),
                            constants.FABRIC_SNAPSHOTS.value,
                            NoxLauncherContainer(
                                content= INSTALL_BUTTON,
                                alignment= flet.alignment.center,
                                padding= flet.padding.all(30)
                            )
                        ]
                    )

                case "vanilla":

                    global vanilla
                    vanilla = True

                    main_row.controls.clear()
                    main_row.update()

                    main_container.width = 500
                    main_container.height = 460
                    
                    main_container.update()

                    title.value = "Vanilla"
                    title.update()

                    title_row.controls.remove(title_icon)
                    title_row.controls.insert(0, flet.Image(src= "vanilla.png", width= 50, height= 50, filter_quality= flet.FilterQuality.HIGH))   

                    title_row.update()

                    main_column.controls.remove(main_row)

                    main_column.extend(
                        [ 
                            NoxLauncherRow(
                                controls= [
                                    NoxLauncherContainer(content= 
                                        flet.Text("Vanilla Releases", size= 25, font_family= "Minecraft"), 
                                        expand_loose= True,
                                        alignment= flet.alignment.center, 
                                        padding= flet.padding.all(20)
                                    )

                                ],
                                expand_loose= True,
                                alignment= flet.MainAxisAlignment.CENTER
                            ),
                            constants.VANILLA_RELEASES.value,
                            NoxLauncherRow(
                                controls= [
                                    NoxLauncherContainer(content= 
                                        flet.Text("Vanilla Snapshots", size= 25, font_family= "Minecraft"), 
                                        expand_loose= True,
                                        alignment= flet.alignment.center, 
                                        padding= flet.padding.all(20)
                                    )

                                ],
                                expand_loose= True,
                                alignment= flet.MainAxisAlignment.CENTER
                            ),
                            constants.VANILLA_SNAPSHOTS.value,
                            NoxLauncherContainer(
                                content= INSTALL_BUTTON,
                                alignment= flet.alignment.center,
                                padding= flet.padding.all(30)
                            )
                        ]
                    )

                case "forge":

                    global forge
                    forge = True

                    main_row.controls.clear()
                    main_row.update()

                    main_container.width = 500
                    main_container.height = 300
                    
                    main_container.update()

                    title.value = "Forge"
                    title.update()

                    title_row.controls.remove(title_icon)
                    title_row.controls.insert(0, flet.Image(src= "forge.png", width= 50, height= 50, filter_quality= flet.FilterQuality.HIGH))   

                    title_row.update()

                    main_column.controls.remove(main_row)

                    main_column.extend(
                        [
                            NoxLauncherRow(
                                controls= [
                                    NoxLauncherContainer(content= 
                                        flet.Text("Forge Versions", size= 25, font_family= "Minecraft"), 
                                        expand_loose= True,
                                        alignment= flet.alignment.center, 
                                        padding= flet.padding.all(20)
                                    )

                                ],
                                expand_loose= True,
                                alignment= flet.MainAxisAlignment.CENTER
                            ),
                            constants.FORGE.value,
                            NoxLauncherContainer(
                                content= INSTALL_BUTTON,
                                alignment= flet.alignment.center,
                                padding= flet.padding.all(30)
                            )
                        ]
                    )

        title_icon: flet.Icon = flet.Icon(name= flet.icons.DOWNLOAD, color= "#717171", size= 30)
        title: flet.Text = flet.Text("Install versions", size= 30, color= "#ffffff", font_family= "Minecraft")

        title_row: NoxLauncherRow = NoxLauncherRow(
            controls= [
                title_icon,
                NoxLauncherContainer(content= title, expand_loose= True, alignment= flet.alignment.center)
            ],
            spacing= 15,
            expand_loose= True,
            alignment= flet.MainAxisAlignment.CENTER,
            vertical_alignment= flet.CrossAxisAlignment.CENTER
        )

        main_row: NoxLauncherRow = NoxLauncherRow(
            controls= [
                NoxLauncherContainer(
                    expand_loose= True,    
                    expand= True,
                    content= flet.ElevatedButton(
                        content= flet.Image(src= "fabric.png", width= 90, height= 90, filter_quality= flet.FilterQuality.HIGH), 
                        width= 120, height= 120, bgcolor= '#272727', key= "fabric", on_click= select_versions,
                        style= flet.ButtonStyle(side= flet.BorderSide(width= 2, color= "#717171"))
                    ),
                    alignment= flet.alignment.center
                ),
                NoxLauncherContainer(
                    expand_loose= True,    
                    expand= True,
                    content= flet.ElevatedButton(
                        content= flet.Image(src= "vanilla.png", width= 90, height= 90, filter_quality= flet.FilterQuality.HIGH), 
                        width= 120, height= 120, bgcolor= '#272727', key= "vanilla", on_click= select_versions,
                        style= flet.ButtonStyle(side= flet.BorderSide(width= 2, color= "#717171"))
                    ),
                    alignment= flet.alignment.center
                ),
                NoxLauncherContainer(
                    expand_loose= True,    
                    expand= True,
                    content= flet.ElevatedButton(
                        content= flet.Image(src= "forge.png", width= 90, height= 90, filter_quality= flet.FilterQuality.HIGH), 
                        width= 120, height= 120, bgcolor= '#272727', key= "forge", on_click= select_versions,
                        style= flet.ButtonStyle(side= flet.BorderSide(width= 2, color= "#717171"))
                    ),
                    alignment= flet.alignment.center
                )      
            ],
            alignment= flet.MainAxisAlignment.CENTER,
            vertical_alignment= flet.CrossAxisAlignment.CENTER,
            expand= True, 
            expand_loose= True
        )

        main_column: NoxLauncherColumn = NoxLauncherColumn(expand= True, expand_loose= True, spacing= 5,
            controls= [
                title_row,
                main_row
            ]
        )

        main_container: NoxLauncherContainer = NoxLauncherContainer(
            width= 500,
            height= 250,
            alignment= flet.alignment.center,
            padding= flet.padding.all(20),
            bgcolor= "#272727",
            border_radius= 20,
            content= main_column
        )

        back_to_play: flet.TextButton = flet.TextButton(content= flet.Text("Back to play", size= 20, font_family= "Minecraft"), style= flet.ButtonStyle(bgcolor= "#148b47", color= "#ffffff", shape= flet.RoundedRectangleBorder(radius= 5)), width= 190, height= 45, on_click= lambda _: page.go("/play"))

        return flet.View(
            controls= [
                NoxLauncherContainer(
                    height= 80,
                    expand_loose= True,
                    content= NoxLauncherRow(
                        controls= [
                            flet.Icon(name= flet.icons.ARROW_BACK, color= "#717171", size= 40),
                            back_to_play
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
                NoxLauncherContainer(
                    expand= True,
                    expand_loose= True, 
                    alignment= flet.alignment.center,
                    content= main_container
                )
            ],
            padding= 0,
        )

    def info(page: flet.Page) -> flet.View:

        return flet.View(
            controls= [
                NoxLauncherContainer(
                    height= 80,
                    expand_loose= True,
                    content= NoxLauncherRow(
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
                NoxLauncherContainer(
                    expand= True, 
                    expand_loose= True, 
                    alignment= flet.alignment.center,
                    content= NoxLauncherContainer(
                        width= 500, 
                        height= 510, 
                        bgcolor= "#272727", 
                        border_radius= 20, 
                        alignment= flet.alignment.center,
                        padding= flet.padding.all(20), 
                        content= NoxLauncherColumn(expand= True, expand_loose= True,
                            controls= [
                                NoxLauncherContainer(image_src= "icon.png", expand_loose= True, height= 180),
                                NoxLauncherContainer(content= flet.Text("NoxLauncher is a powerful and easy-to-use Minecraft launcher develop by Krayson Studio.", size= 15, color= "#ffffff", font_family= "Minecraft"), expand_loose= True, alignment= flet.alignment.center),
                                NoxLauncherColumn(controls= [
                                    flet.Text("Developed by: ", color= "#ffffff", size= 15, font_family= "Minecraft"),
                                    NoxLauncherRow(controls= [
                                        flet.TextButton(content= flet.Image(src= "github.png", width= 60, height= 60, filter_quality= flet.FilterQuality.HIGH), width= 60, height= 60, url_target= flet.UrlTarget.BLANK, url= "https://github.com/DevCheckOG"),
                                        flet.Text("DevCheckOG", color= "#ffffff", size= 15, font_family= "Minecraft")
                                    ], expand_loose= True, alignment= flet.MainAxisAlignment.START, vertical_alignment= flet.CrossAxisAlignment.CENTER, spacing= 10),
                                    NoxLauncherRow(controls= [
                                        flet.TextButton(content= flet.Image(src= "github.png", width= 60, height= 60, filter_quality= flet.FilterQuality.HIGH), width= 60, height= 60, url_target= flet.UrlTarget.BLANK, url= "https://github.com/aaronwayas"),
                                        flet.Text("AaronWayas", color= "#ffffff", size= 15, font_family= "Minecraft")
                                    ], expand_loose= True, alignment= flet.MainAxisAlignment.START, vertical_alignment= flet.CrossAxisAlignment.CENTER, spacing= 10)
                                ], horizontal_alignment= flet.MainAxisAlignment.START, alignment= flet.CrossAxisAlignment.CENTER, spacing= 5, expand_loose= True),
                                NoxLauncherRow(
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

        def patch_memory_java_allocated(_: flet.ControlEvent) -> None:

            Config.update_java_memory_allocated(JAVA_INFO[1], Config.get_memory_ram())
            page.go("/play")

        def update_settings(_: flet.ControlEvent) -> None:

            if java_path.value != "System": 
                Config.update_java_path(java_path.value)

            version.value = f"Version: {Config.get_java_version(java_path.value)}"
            version.update()
            
            location.value = f"Location: {java_path.value if len(java_path.value) <= 15 else f'{java_path.value[:15]}...'}" 
            location.update()

            java_args.value = " ".join(Config.update_java_memory_allocated([arg for arg in java_args.value.split(" ") if isinstance(arg, str) and arg != ""], str(round(java_allocated_memory.value))))
            java_args.update()

            Config.update_close_when_playing(close_when_playing.value)
            Config.update_debug_mode(debug_mode.value)

            def ok(_: flet.ControlEvent) -> None:

                page.close(UPDATE_JAVA_SETTINGS_BANNER)
                page.update()

            UPDATE_JAVA_SETTINGS_BANNER: NoxLauncherBanner = NoxLauncherBanner(
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

            page.open(UPDATE_JAVA_SETTINGS_BANNER)

        if JAVA_INFO is False:

            page.open(flet.AlertDialog(
                modal= True,
                icon= flet.Icon(name= flet.icons.ERROR_ROUNDED, color= flet.colors.RED_ACCENT, size= 40),
                title= NoxLauncherContainer(
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
        
        MEMORY_REACHED_ALERT: flet.AlertDialog = flet.AlertDialog(
            modal= True,
            icon= flet.Icon(name= flet.icons.ERROR_ROUNDED, color= flet.colors.RED_ACCENT, size= 40),
            title= NoxLauncherContainer(
                content= flet.Text("Available memory reached", size= 25, font_family= "Minecraft"),
                alignment= flet.alignment.center,
                expand_loose= True
            ),
            bgcolor= "#272727",
            content= flet.Text("Java allocated memory is higher than the available memory! Press Ok and fix it!", size= 20, font_family= "Minecraft"),
            actions= [
                flet.TextButton(content= flet.Text("Ok", size= 20, font_family= "Minecraft"), style= flet.ButtonStyle(bgcolor= "#148b47", color= "#ffffff", shape= flet.RoundedRectangleBorder(radius= 5)), width= 120, height= 45, on_click= patch_memory_java_allocated),
            ],
            on_dismiss= lambda _: None
        )

        if Config.parse_memory(JAVA_INFO[1]) > Config.get_memory_ram(): 
            page.open(MEMORY_REACHED_ALERT)
            return flet.View()

        java_args: flet.TextField = flet.TextField(value= " ".join(JAVA_INFO[1]), multiline= False, expand_loose= True, height= 70, border_radius= 10, border_color= "#717171")
        java_path: NoxLauncherDropdown = NoxLauncherDropdown(label= "Java source", hint_text= "Select the Java source!", options= Config.get_java_list(), border_color= "#717171", border_radius= 10, border_width= 2,  label_style= flet.TextStyle(color= "#ffffff"), value= Config.determinate_java_path(JAVA_INFO[0]))
        java_allocated_memory: flet.Slider = flet.Slider(value= Config.parse_memory(JAVA_INFO[1]), min= 1000, max= Config.get_memory_ram(), label= "{value}MB", expand_loose= True, height= 40, active_color= "#148b47", thumb_color= "#ffffff")
        version: flet.Text = flet.Text(f"Version: {Config.get_java_version(JAVA_INFO[0])}", size= 20, color= "#ffffff", font_family= "Minecraft")
        location: flet.Text = flet.Text(f"Location: {JAVA_INFO[0][:14]}...", size= 20, color= "#ffffff", font_family= "Minecraft")
        close_when_playing: flet.Switch = flet.Switch(value= Config.get_close_when_playing(), active_color= "#148b47")
        debug_mode: flet.Switch = flet.Switch(value= Config.get_debug_mode(), active_color= "#148b47")

        return flet.View(
            controls= [
                NoxLauncherContainer(
                    height= 80,
                    expand_loose= True,
                    content= NoxLauncherRow(
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
                NoxLauncherContainer(
                    expand= True, 
                    expand_loose= True, 
                    alignment= flet.alignment.center,
                    content= NoxLauncherContainer(
                        width= 500, 
                        height= 610, 
                        bgcolor= "#272727", 
                        border_radius= 20, 
                        alignment= flet.alignment.center,
                        padding= flet.padding.all(20), 
                        content= NoxLauncherColumn(expand= True, expand_loose= True, spacing= 5,
                            controls= [
                                NoxLauncherContainer(content= flet.Text("Settings", size= 30, color= "#ffffff", font_family= "Minecraft"), expand_loose= True, alignment= flet.alignment.center),
                                NoxLauncherRow(expand_loose= True, height= 100, controls= [
                                    NoxLauncherContainer(content= flet.Image(
                                        src= "java.png", 
                                        width= 90, 
                                        height= 90,
                                        filter_quality= flet.FilterQuality.HIGH
                                    ), alignment= flet.alignment.center_left, padding= flet.padding.only(bottom= 28)),
                                    NoxLauncherColumn(
                                        controls = [
                                            NoxLauncherContainer(content= location, expand_loose= True, alignment= flet.alignment.center_left),
                                            NoxLauncherContainer(content= version, expand_loose= True, alignment= flet.alignment.center_left)
                                        ],
                                        spacing= 15,
                                        expand_loose= True
                                    )
                                ], vertical_alignment= flet.CrossAxisAlignment.CENTER, alignment= flet.MainAxisAlignment.CENTER, spacing= 0),
                                flet.Text("Java settings", size= 20, color= "#ffffff", font_family= "Minecraft"),
                                java_path,
                                flet.Text("JVM arguments", size= 20, color= "#ffffff", font_family= "Minecraft"),
                                java_args,
                                NoxLauncherContainer(content= flet.Text("Memory dedicated", size= 20, color= "#ffffff", font_family= "Minecraft"), expand_loose= True, alignment= flet.alignment.center),
                                java_allocated_memory,
                                NoxLauncherRow(
                                    controls = [
                                        NoxLauncherContainer(content= flet.Text("close the launcher when playing", size= 20, color= "#ffffff", font_family= "Minecraft"), expand_loose= True, alignment= flet.alignment.center),
                                        close_when_playing
                                    ],
                                    expand_loose= True,
                                    alignment= flet.MainAxisAlignment.CENTER,
                                    vertical_alignment= flet.CrossAxisAlignment.CENTER
                                ),
                                NoxLauncherRow(
                                    controls = [
                                        NoxLauncherContainer(content= flet.Text("Debug mode", size= 20, color= "#ffffff", font_family= "Minecraft"), expand_loose= True, alignment= flet.alignment.center),
                                        debug_mode
                                    ],
                                    expand_loose= True,
                                    alignment= flet.MainAxisAlignment.CENTER,
                                    vertical_alignment= flet.CrossAxisAlignment.CENTER
                                ),
                                NoxLauncherContainer(content= flet.TextButton(content= flet.Text("Save", size= 20, font_family= "Minecraft"), on_click= update_settings, style= flet.ButtonStyle(bgcolor= "#148b47", color= "#ffffff", shape= flet.RoundedRectangleBorder(radius= 5)), width= 190, height= 45), alignment= flet.alignment.center, expand_loose= True, expand= True)
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

        if not os.path.exists(ACC["skin"]):
            showerror(title= "Nox Launcher", message= "Skin not found. Please fix this editing profiles.json and try again.", type= "ok")
            page.window.destroy()
            return flet.View()

        skin: flet.Image = AccountManager.get_skin(ACC["skin"], ACC["name"], size= 50, width= 120, height= 120)

        return flet.View("/accounts",  
            controls= [
                NoxLauncherContainer(expand= True, expand_loose= True, alignment= flet.alignment.center, 
                content= NoxLauncherContainer(width= 420, height= 420, bgcolor= "#272727", border_radius= 20, alignment= flet.alignment.center,
                padding= flet.padding.all(20), 
                content= NoxLauncherColumn(expand= True, expand_loose= True, spacing= 5,
                controls= [
                    NoxLauncherContainer(content= flet.Text("Accounts", size= 30, color= "#ffffff", font_family= "Minecraft"), expand_loose= True, alignment= flet.alignment.center),
                    NoxLauncherRow(controls= [
                            skin, 
                            NoxLauncherContainer(expand_loose= True),
                            NoxLauncherColumn(controls= [
                            flet.Text(ACC["name"], size= 20, color= "#ffffff", font_family= "Minecraft"),
                            flet.Text("Type: " + ACC["type"], size= 20, color= "#ffffff", font_family= "Minecraft"),
                        ],
                        expand_loose= True),
                    ], spacing= 5, expand_loose= True),
                    NoxLauncherContainer(expand= True),
                    NoxLauncherContainer(content= NoxLauncherColumn(controls= [
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

        if not os.path.exists(ACC["skin"]):
            showerror(title= "Nox Launcher", message= "Skin not found. Please fix this editing profiles.json and try again.", type= "ok")
            page.window.destroy()
            return flet.View()

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
                
                if isinstance(control, NoxLauncherColumn):
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

            if account_rename.value is not None and not account_rename.value.isspace() and account_rename.value != "":

                if len(account_rename.value) > 13: 

                    def ok(_: flet.ControlEvent) -> None:

                        page.close(BANNER)
                        page.update()

                        account_rename.disabled = False
                        account_rename.value = ""
                        account_rename.update()

                        event.control.disabled = False
                        event.control.update()
                
                    BANNER: NoxLauncherBanner = NoxLauncherBanner(
                        bgcolor= "#272727",
                        leading= flet.Icon(name= flet.icons.ERROR_ROUNDED, color= flet.colors.RED_ACCENT, size= 40),
                        content= flet.Text(
                            value= "Account name is too long!",
                            color= "#ffffff",
                            size= 20,
                            font_family= "Minecraft"
                        ),
                        actions= [
                            flet.TextButton(content= flet.Text("Ok", size= 20, font_family= "Minecraft"), style= flet.ButtonStyle(bgcolor= "#148b47", color= "#ffffff", shape= flet.RoundedRectangleBorder(radius= 5)), width= 150, height= 40, on_click= ok)
                        ]
                    )

                    page.open(BANNER)

                rename: bool = AccountManager.rename(account_rename.value.replace(" ", "_"))

                if not rename:

                    page.open(flet.AlertDialog(
                        modal= True,
                        icon= flet.Icon(name= flet.icons.ERROR_ROUNDED, color= flet.colors.RED_ACCENT, size= 40),
                        title= NoxLauncherContainer(
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
                
                BANNER: NoxLauncherBanner = NoxLauncherBanner(
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
                
                BANNER: NoxLauncherBanner = NoxLauncherBanner(
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

        skin_row: NoxLauncherRow = NoxLauncherRow(controls= [
            skin, 
            NoxLauncherContainer(expand_loose= True),
            NoxLauncherColumn(controls= [
                flet.Text(ACC["name"], size= 20, color= "#ffffff", font_family= "Minecraft"),
                flet.Text("Type: " + ACC["type"], size= 20, color= "#ffffff", font_family= "Minecraft"),
            ], expand_loose= True)], 
            spacing= 5, 
            expand_loose= True
        )

        back_to_play_button: NoxLauncherContainer = NoxLauncherContainer(expand_loose= True, alignment= flet.alignment.center,
            content= NoxLauncherRow(
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

        main_column: NoxLauncherColumn = NoxLauncherColumn(expand= True, expand_loose= True, spacing= 20, controls= [
            NoxLauncherContainer(content= flet.Text("Offline", size= 30, color= "#ffffff", font_family= "Minecraft"), expand_loose= True, alignment= flet.alignment.center),
            skin_row,
            NoxLauncherContainer(height= 150, expand_loose= True, alignment= flet.alignment.center,
                content= NoxLauncherColumn(
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

        main_container: NoxLauncherContainer = NoxLauncherContainer(width= 520, height= 450, bgcolor= "#272727", border_radius= 20, 
            alignment= flet.alignment.center,
            padding= flet.padding.all(20),
            content= main_column
        )

        return flet.View("/offline",
            controls= [
                NoxLauncherContainer(expand= True, expand_loose= True, alignment= flet.alignment.center,
                        content= main_container
                )
            ],

            horizontal_alignment= flet.MainAxisAlignment.CENTER, 
            vertical_alignment= flet.CrossAxisAlignment.CENTER, 
            padding= 0
        )  

    def play(page: flet.Page) -> flet.View:

        ACC: Dict[str, str] = AccountManager.determinate()

        if not os.path.exists(ACC["skin"]):
            showerror(title= "Nox Launcher", message= "Skin not found. Please fix this editing profiles.json and try again.", type= "ok")
            page.window.destroy()
            return flet.View()

        skin: flet.Image = AccountManager.get_skin(ACC["skin"], ACC["name"])

        def start_launcher(_: flet.ControlEvent) -> None: 
            if VERSIONS.value is not None and VERSIONS.value != "Install an minecraft version!": 
                Launcher(VERSIONS.value, page)

        VERSIONS: NoxLauncherDropdown = NoxLauncherDropdown(label= "Installed Versions", hint_text= "Minecraft version to play!", options= Config.get_versions_available(), border_color= "#717171", border_radius= 10, label_style= flet.TextStyle(color= "#ffffff"), border_width= 2)

        return flet.View("/play", 
            controls= [
                NoxLauncherContainer(content = NoxLauncherRow(expand= True, expand_loose= True, controls= constants.MINECRAFT_NEWS.value, 
                alignment= flet.MainAxisAlignment.CENTER, vertical_alignment= flet.CrossAxisAlignment.CENTER, spacing= 30, scroll= flet.ScrollMode.AUTO), expand= True, expand_loose= True, alignment= flet.alignment.center),
            ],

            appbar= flet.AppBar(
                leading= flet.Image(src= "icon.png", width= 150, height= 100, filter_quality= flet.FilterQuality.HIGH),
                leading_width= 170,
                bgcolor= "#272727", 
                actions= [
                    NoxLauncherContainer(
                        width= 120,
                        height= 44, 
                        alignment= flet.alignment.center,
                        content= NoxLauncherRow(
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
                                    on_click= lambda _: page.go("/info")
                                ),
                                flet.IconButton(
                                    icon= flet.icons.NEWSPAPER_ROUNDED,
                                    icon_size= 26,
                                    icon_color= "#717171",
                                    height= 42,
                                    width= 42,
                                    on_click= lambda _: page.go("/news")
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
                content= NoxLauncherRow(expand= True, spacing= 10, alignment= flet.MainAxisAlignment.CENTER, controls= [
                    flet.TextButton(content= flet.Text("Install", size= 25, font_family= "Minecraft"), style= flet.ButtonStyle(bgcolor= "#148b47", color= "#ffffff", shape= flet.RoundedRectangleBorder(radius= 5)), width= 150, height= 45, on_click= lambda _: page.go("/install")),
                    NoxLauncherContainer(expand= True),
                    VERSIONS,
                    flet.TextButton(content= flet.Text("Play", size= 25, font_family= "Minecraft"), style= flet.ButtonStyle(bgcolor= "#148b47", color= "#ffffff", shape= flet.RoundedRectangleBorder(radius= 5)), width= 150, height= 45, on_click= start_launcher),
                    NoxLauncherContainer(expand= True),
                    NoxLauncherContainer(expand= True, border_radius= 20, 
                        border= flet.border.all(2, "#717171"), 
                        content= NoxLauncherRow(expand= True, spacing= 0, controls= [
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
        
class MinecraftDownloader:

    def __init__(self, versions: List[Dict[str, Any]], controls: List[flet.Text], close: Callable[[], None]) -> None:

        self.versions: List[Dict[str, Any]] = versions
        self.controls: List[flet.Text] = controls
        self.close: Callable[[], None] = close

        self.downloader(self.versions, self.controls)

    def downloader(self, versions: List[Dict[str, Any]], controls: List[flet.Text]) -> None: 

        def setStatus(status: str) -> None:

            controls[n].value = status
            controls[n].size = 15
            controls[n].update()

        n: int = 0
        
        for version in versions:

            if version is None or isinstance(controls[n], NoxLauncherContainer): 
                n += 1
                continue

            match version["type"]:
                case "fabric release" | "fabric snapshot":
                    controls[n].value = f"Downloading Fabric {version['version']}..."
                    controls[n].update()

                    time.sleep(2)

                    minecraft_launcher_lib.fabric.install_fabric(
                        version["version"], 
                        f"{Config.get_path()}/NoxLauncher/",
                        callback= {"setStatus": setStatus}
                    )

                case "vanilla release" | "vanilla snapshot":
                    controls[n].value = f"Downloading Vanilla {version['version']}..."
                    controls[n].update()

                    time.sleep(2)

                    minecraft_launcher_lib.install.install_minecraft_version(
                        version["version"], 
                        f"{Config.get_path()}/NoxLauncher/",
                        {"setStatus": setStatus}
                    )

                case "forge version": 
                    controls[n].value = f"Downloading Forge {version['version']}..."
                    controls[n].update()

                    time.sleep(2)

                    minecraft_launcher_lib.forge.install_forge_version(
                        version["version"], 
                        f"{Config.get_path()}/NoxLauncher/",
                        {"setStatus": setStatus}
                    )

            n += 1

        self.close()

class Launcher:

    def __init__(self,  version: str, page: flet.Page) -> None:

        self.java_args: List[str] | bool = Config.get_java_info()[1]
        self.java_path: str | bool = Config.get_java_info()[0]
        self.version: str = version
        self.page: flet.Page = page

        def close_alert(control: flet.ControlEvent) -> None:
            page.close(control.control)

        if self.java_path is False or self.java_args is False:

            page.open(flet.AlertDialog(
                modal= True,
                icon= flet.Icon(name= flet.icons.ERROR_ROUNDED, color= flet.colors.RED_ACCENT, size= 40),
                title= NoxLauncherContainer(
                    content= flet.Text("Java not found!", size= 25, font_family= "Minecraft"),
                    alignment= flet.alignment.center,
                    expand_loose= True
                ),
                bgcolor= "#272727",
                content= flet.Text("Java not found, please set it up in settings!", size= 20, font_family= "Minecraft"),
                actions= [
                    flet.TextButton(content= flet.Text("Ok", size= 20, font_family= "Minecraft"), style= flet.ButtonStyle(bgcolor= "#148b47", color= "#ffffff", shape= flet.RoundedRectangleBorder(radius= 5)), width= 120, height= 45, on_click= close_alert),
                ],
                on_dismiss= lambda _: None
            ))

            return
        
        self.launch()
        
    def launch(self) -> None:

        DEBUG_MODE: bool = Config.get_debug_mode()
        CLOSE_WHEN_PLAYING: bool = Config.get_close_when_playing()
        ACCOUNT: Dict[str, str] = AccountManager.determinate()

        match ACCOUNT["type"]:

            case "offline": 

                OPTIONS: Dict[str, Any] = {
                    "username": ACCOUNT["name"],
                    "uuid": uuid.uuid4().hex,
                    "token": "",
                    'jvmArguments': self.java_args,
                    'executablePath': self.java_path
                }

                minecraft_args: str = " ".join(minecraft_launcher_lib.command.get_minecraft_command(self.version, f"{Config.get_path()}/NoxLauncher/", OPTIONS))

                match CLOSE_WHEN_PLAYING:

                    case True:
                        match platform.system():
                            case "Windows": 
                                match DEBUG_MODE:
                                    case True:
                                        self.page.window.destroy()
                                        subprocess.call(f'start /i cmd /k {minecraft_args}', shell= True, stdout= subprocess.PIPE, stderr= subprocess.PIPE, stdin= subprocess.PIPE, text= True)
                                    case False:
                                        self.page.window.destroy()
                                        subprocess.call(f'start /b cmd /k {minecraft_args}', shell= True, stdout= subprocess.PIPE, stderr= subprocess.PIPE, stdin= subprocess.PIPE, text= True)
                            case "Linux": 
                                match DEBUG_MODE:
                                    case True: 
                                        self.page.window.destroy()
                                        subprocess.call(f'nohup alacritty -e {minecraft_args}', shell= True, stdout= subprocess.PIPE, stderr= subprocess.PIPE, stdin= subprocess.PIPE, text= True)
                                    case False:
                                        self.page.window.destroy()
                                        subprocess.call(f'nohup {minecraft_args}', shell= True, stdout= subprocess.PIPE, stderr= subprocess.PIPE, stdin= subprocess.PIPE, text= True)

                    case False: 
                        match platform.system():
                            case "Windows":
                                match DEBUG_MODE:
                                    case True: subprocess.call(f'start /i cmd /k {minecraft_args}', shell= True, stdout= subprocess.PIPE, stderr= subprocess.PIPE, stdin= subprocess.PIPE, text= True)
                                    case False: subprocess.call(f'start /b cmd /k {minecraft_args}', shell= True, stdout= subprocess.PIPE, stderr= subprocess.PIPE, stdin= subprocess.PIPE, text= True)
                            case "Linux": 
                                match DEBUG_MODE:
                                    case True: 
                                        # HAY QUE DETERMINAR LA TERMINAL O USAR UNO UNIVERSAL, en mi caso es alacritty.
                                        subprocess.call(f'nohup alacritty -e {minecraft_args}', shell= True, stdout= subprocess.PIPE, stderr= subprocess.PIPE, stdin= subprocess.PIPE, text= True)
                                    case False: subprocess.call(f'nohup {minecraft_args}', shell= True, stdout= subprocess.PIPE, stderr= subprocess.PIPE, stdin= subprocess.PIPE, text= True)
            case _: ...
        
class AccountManager:

    def offline() -> Dict[str, str]:

        if not os.path.exists(Config.get_path() + "/NoxLauncher/settings/profiles/profiles.json"): Config.repair()

        with open(Config.get_path() + "/NoxLauncher/settings/profiles/profiles.json", "r", encoding= "utf-8") as f:
            profiles = json.load(f)

            if not "profiles" in profiles:
                profiles["profiles"] = {}
                with open(Config.get_path() + "/NoxLauncher/settings/profiles/profiles.json", "w", encoding= "utf-8") as f:
                    json.dump(profiles, f, indent= 4)

            elif not isinstance(profiles["profiles"], dict):
                profiles["profiles"] = {}
                with open(Config.get_path() + "/NoxLauncher/settings/profiles/profiles.json", "w", encoding= "utf-8") as f:
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

        if not os.path.exists(Config.get_path() + "/NoxLauncher/settings/profiles/profiles.json"): Config.repair()

        with open(Config.get_path() + "/NoxLauncher/settings/profiles/profiles.json", "r", encoding= "utf-8") as f:
            profiles = json.load(f)

            if not "profiles" in profiles:
                profiles["profiles"] = {}
                with open(Config.get_path() + "/NoxLauncher/settings/profiles/profiles.json", "w", encoding= "utf-8") as f:
                    json.dump(profiles, f, indent= 4)

            elif not isinstance(profiles["profiles"], dict):
                profiles["profiles"] = {}
                with open(Config.get_path() + "/NoxLauncher/settings/profiles/profiles.json", "w", encoding= "utf-8") as f:
                    json.dump(profiles, f, indent= 4)

            if len(profiles["profiles"]) > 0:
                for profile in profiles["profiles"].values():
                    if not isinstance(profile, dict):
                        continue
                    elif not "selected" in profile:
                        profile["selected"] = False
                        continue
                    elif profile["selected"] == True:
                        if "name" in profile:
                            if not isinstance(profile["name"], str): profile["name"] = "Default"
                            if profile["name"].isspace() or profile["name"] == "": profile["name"] = "Default"
                            
                        return profile
            else:

                profiles["profiles"].update({
                    "default": {
                        "name": "Default",
                        "type": "offline",
                        "selected": True,
                        "skin": "extensions/assets/steve.png"
                    },
                    "premium": {},
                    "no_premium": {}

                })

                with open(Config.get_path() + "/NoxLauncher/settings/profiles/profiles.json", "w", encoding= "utf-8") as f:
                    json.dump(profiles, f, indent= 4)
                    
                return profiles["profiles"]["default"]
                        
    def rename(new: str) -> bool:

        if not os.path.exists(Config.get_path() + "/NoxLauncher/settings/profiles/profiles.json"): Config.repair()

        with open(Config.get_path() + "/NoxLauncher/settings/profiles/profiles.json", "r", encoding= "utf-8") as f:
            profiles = json.load(f)

            if not "profiles" in profiles:
                profiles["profiles"] = {}
                with open(Config.get_path() + "/NoxLauncher/settings/profiles/profiles.json", "w", encoding= "utf-8") as f:
                    json.dump(profiles, f, indent= 4)
            elif not isinstance(profiles["profiles"], dict):
                profiles["profiles"] = {}
                with open(Config.get_path() + "/NoxLauncher/settings/profiles/profiles.json", "w", encoding= "utf-8") as f:
                    json.dump(profiles, f, indent= 4)

            if len(profiles["profiles"]) > 0:

                for profile in profiles["profiles"].values():
                    if "selected" not in profile: continue
                    elif profile["selected"] == True:
                        AccountManager.delete_skin_from_cache(profile["name"])
                        profile["name"] = new
                        break

                with open(Config.get_path() + "/NoxLauncher/settings/profiles/profiles.json", "w", encoding= "utf-8") as f: 
                    json.dump(profiles, f, indent= 4)

                return True

            return False

    def select(name: str) -> Dict[str, str]:

        if not os.path.exists(Config.get_path() + "/NoxLauncher/settings/profiles/profiles.json"): Config.repair()

        with open(Config.get_path() + "/NoxLauncher/settings/profiles/profiles.json", "r", encoding= "utf-8") as f:
            profiles = json.load(f)

            if "profiles" not in profiles: 

                profiles["profiles"] = {}
                with open(Config.get_path() + "/NoxLauncher/settings/profiles/profiles.json", "w", encoding= "utf-8") as f:
                    json.dump(profiles, f, indent= 4)

            elif not isinstance(profiles["profiles"], dict):
                profiles["profiles"] = {}
                with open(Config.get_path() + "/NoxLauncher/settings/profiles/profiles.json", "w", encoding= "utf-8") as f:
                    json.dump(profiles, f, indent= 4)

            if len(profiles["profiles"]) > 0:
                for profile in profiles["profiles"].values():
                    if "name" not in profile or "selected" not in profile:
                        continue
                    elif profile["name"] == name:
                        profile["selected"] = True
                        with open(Config.get_path() + "/NoxLauncher/settings/profiles/profiles.json", "w", encoding= "utf-8") as f: 
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

        with open(Config.get_path() + "/NoxLauncher/settings/profiles/profiles.json", "w", encoding= "utf-8") as f:
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

        skin.to_isometric_image(perspective).save(f"{Config.get_path()}/NoxLauncher/cache/{name}.png")

        if os.path.exists(os.path.dirname(__file__) + "/test.png") or os.path.exists(os.path.dirname(os.path.dirname(__file__)) + "/test.png"):
            os.remove(os.path.dirname(__file__) + "/test.png")
            os.remove(os.path.dirname(os.path.dirname(__file__)) + "/test.png")

        return flet.Image(src= f"{Config.get_path()}/NoxLauncher/cache/{name}.png", width= width, height= height)
    
    def delete_skin_from_cache(name: str) -> None:

        if os.path.exists(f"{Config.get_path()}/NoxLauncher/cache/{name}.png"):
            os.remove(f"{Config.get_path()}/NoxLauncher/cache/{name}.png")
