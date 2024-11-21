import flet
import time

from gui.buttons import BackToPlayButton
from fs import *

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
                                                            content= flet.Dropdown(hint_text= "Select a Java source!", options= get_all_java_instances(), border_color= "#717171", border_radius= 10, border_width= 2, label_style= flet.TextStyle(color= "#ffffff"), value= get_current_java_instance(), on_change= self.update_java),
                                                            alignment= flet.alignment.center,
                                                            expand_loose= True,
                                                            padding= flet.padding.only(left= 40, bottom= 10, right= 40)
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
