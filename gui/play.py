import os
import platform
import flet
import threading
import subprocess
import uuid
import minecraft_launcher_lib

from gui.appbar import NoxLauncherGenericAppBar

from typing import List, Dict, Any

from constants import VERSION
from accounts import Account
from fs import get_current_jvm_args, get_current_java_instance, get_home, get_minecraft_versions, get_autoclose
from threadpool import NOXLAUNCHER_THREADPOOL

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
                                                flet.Dropdown(hint_text= "Install a Minecraft version first!" if len(get_minecraft_versions()) == 0 else "Select a version to play!", options= get_minecraft_versions(), border_color= "#717171", border_radius= 10, border_width= 2, hint_style= flet.TextStyle(size= 14, font_family= "NoxLauncher"), on_change= self.build_launch),
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

            case (acc, "offline"):

                OFFLINE_ACC_OPTIONS: Dict[str, Any] = {
                    "username": acc["name"],
                    "uuid": uuid.uuid4().hex,
                    "jvmArguments": get_current_jvm_args(),
                    "executablePath": get_current_java_instance(),
                    "launcherName": "NoxLauncher",
                    "launcherVersion": VERSION
                }

                if OFFLINE_ACC_OPTIONS["executablePath"] is None:

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
                
                self.launch(minecraft_launcher_lib.command.get_minecraft_command(event.control.value, get_home(), OFFLINE_ACC_OPTIONS))

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
        
        subprocess.call(minecraft_command, stdout= subprocess.PIPE, stderr= subprocess.PIPE, stdin= subprocess.PIPE, text= True, creationflags= 134217728) if platform.system() == "Windows" else subprocess.call(minecraft_command, stdout= subprocess.PIPE, stderr= subprocess.PIPE, stdin= subprocess.PIPE, text= True)

    def _launch_with_console(self, minecraft_command: List[str]) -> None:

        mc_proccess: subprocess.Popen = subprocess.Popen(minecraft_command, stdout= subprocess.PIPE, stderr= subprocess.PIPE, stdin= subprocess.PIPE, text= True)
        NOXLAUNCHER_THREADPOOL.submit(self._update_console, mc_proccess)

    def _update_console(self, process: subprocess.Popen) -> None:

        if process.wait():
            if process.returncode != 0:
                if not process.stderr.read().isspace() or process.stderr.read() != "":
                
                    self.console.content.controls.clear()
                    self.console.content.controls.append(flet.Text(process.stderr.read(), size= 13, font_family= "NoxLauncher", color= "#FFFFFF"))
                    self.console.update()

                elif not process.stdout.read().isspace() or process.stdout.read() != "":

                    self.console.content.controls.clear()
                    self.console.content.controls.append(flet.Text(process.stdout.read(), size= 13, font_family= "NoxLauncher", color= "#FFFFFF"))
                    self.console.update()