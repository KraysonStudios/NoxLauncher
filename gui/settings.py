import flet
import time

import flet_contrib.color_picker

from gui.buttons import BackToPlayButton
from fs import *

class NoxLauncherSettingsGUI:

    def __init__(self, page: flet.Page) -> None:

        self.page: flet.Page = page
        self.titles_color: str = get_titlescolor() 
        self.subtitles_color: str = get_subtitlescolor()
        self.bgcolor: str = get_bgcolor()
        self.filled_color : str = get_filledcolor()
        self.jvm_args_input: flet.TextField = flet.TextField(value= " ".join(get_current_jvm_args()), multiline= False, expand_loose= True, height= 70, border_radius= 10, border_color= self.subtitles_color, on_submit= self.update_jvm_args)
        
        self.title_color_picker = flet_contrib.color_picker.ColorPicker(self.titles_color)
        self.subtitles_color_picker = flet_contrib.color_picker.ColorPicker(self.subtitles_color)
        self.bg_color_picker = flet_contrib.color_picker.ColorPicker(self.bgcolor)  
        self.filled_color_picker = flet_contrib.color_picker.ColorPicker(self.filled_color)

        self.set_border_color_file_picker(self.title_color_picker)
        self.set_border_color_file_picker(self.subtitles_color_picker)
        self.set_border_color_file_picker(self.bg_color_picker)
        self.set_border_color_file_picker(self.filled_color_picker)

        self.build()

    def build(self) -> flet.View:

        return flet.View(
            controls= [
                flet.Container(
                    content= flet.Column(
                        controls= [
                            flet.Row(
                                controls= [
                                    BackToPlayButton(self.page, bgcolor= self.bgcolor, icon_color= self.subtitles_color, text_color= self.titles_color).build(),
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
                                                                    flet.Container(content= flet.Text("Java Settings", size= 30, font_family= "NoxLauncher", color= self.titles_color), expand_loose= True, alignment= flet.alignment.center, padding= flet.padding.only(top= 25))
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
                                                            content= flet.Text("All Java Instances Available", size= 23, font_family= "NoxLauncher", color= self.titles_color),
                                                            expand_loose= True,
                                                            alignment= flet.alignment.center_left,
                                                            padding= flet.padding.only(left= 40, top= 30)
                                                        ),
                                                        flet.Container(
                                                            content= flet.Dropdown(hint_text= "Select a Java source!", options= get_all_java_instances(), border_color= self.subtitles_color, border_radius= 10, border_width= 2, label_style= flet.TextStyle(color= self.titles_color), value= get_current_java_instance(), on_change= self.update_java),
                                                            alignment= flet.alignment.center,
                                                            expand_loose= True,
                                                            padding= flet.padding.only(left= 40, bottom= 10, right= 40)
                                                        ),
                                                        flet.Container(
                                                            content= flet.Text("JVM Arguments", size= 23, font_family= "NoxLauncher", color= self.titles_color),
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
                                                            content= flet.Slider(value= parse_memory(get_current_jvm_args()), min= 1000, max= get_available_memory_ram(), expand_loose= True, height= 40, active_color= self.filled_color, thumb_color= self.titles_color, on_change= self.update_memory_in_jvm_args),
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
                                                bgcolor= self.bgcolor,
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
                                                            content= flet.Text("Close NoxLauncher when Minecraft starts", size= 18, font_family= "NoxLauncher", color= self.titles_color),
                                                            expand_loose= True,
                                                            alignment= flet.alignment.center_left,
                                                            padding= flet.padding.only(left= 20, right= 20)
                                                        ),
                                                        flet.Container(
                                                            content= flet.Switch(value= get_autoclose(), active_color= self.filled_color, on_change= self.update_autoclose, inactive_thumb_color= self.subtitles_color),
                                                            expand_loose= True,
                                                            alignment= flet.alignment.center_left,
                                                            padding= flet.padding.only(left= 20, bottom= 10)
                                                        ),
                                                        flet.Container(
                                                            content= flet.Text("Receive yes or no news in the launcher section", size= 18, font_family= "NoxLauncher", color= self.titles_color),
                                                            expand_loose= True,
                                                            alignment= flet.alignment.center_left,
                                                            padding= flet.padding.only(left= 20, right= 20)
                                                        ),
                                                        flet.Container(
                                                            content= flet.Switch(value= get_receivenews(), active_color= self.filled_color, on_change= self.update_receivenews, inactive_thumb_color= self.subtitles_color),
                                                            expand_loose= True,
                                                            alignment= flet.alignment.center_left,
                                                            padding= flet.padding.only(left= 20, bottom= 10)
                                                        ),
                                                        flet.Container(
                                                            content= flet.Text("Enable Discord Rich Presence", size= 18, font_family= "NoxLauncher", color= self.titles_color),
                                                            expand_loose= True,
                                                            alignment= flet.alignment.center_left,
                                                            padding= flet.padding.only(left= 20, right= 20)
                                                        ),
                                                        flet.Container(
                                                            content= flet.Switch(value= get_discordrpc(), active_color= self.filled_color, on_change= self.update_discordrpc, inactive_thumb_color= self.subtitles_color),
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
                                                bgcolor= self.bgcolor,
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
                            flet.Container(
                                expand_loose= True,
                                height= 40  
                            ),
                            flet.Row(
                                controls= [
                                    flet.Container(
                                        content= flet.Column(
                                            controls= [
                                                flet.Container(
                                                    content= flet.Row(
                                                        controls= [
                                                            flet.Icon(name= flet.icons.FORMAT_PAINT, color= self.subtitles_color, size= 50),
                                                            flet.Text("Customization", size= 25, font_family= "NoxLauncher", color= self.titles_color)
                                                        ],
                                                        alignment= flet.MainAxisAlignment.CENTER,
                                                        expand_loose= True 
                                                    ),
                                                    expand_loose= True,
                                                    alignment= flet.alignment.center,
                                                    padding= flet.padding.only(top= 40)
                                                ),
                                                flet.Container(
                                                    content= flet.Row(
                                                        controls= [
                                                            flet.Column(
                                                                controls= [
                                                                    flet.Container(
                                                                        content= flet.Row(
                                                                            controls= [
                                                                                flet.Icon(name= flet.icons.COLORIZE_SHARP, color= self.subtitles_color, size= 50),
                                                                                flet.Text("Theme", size= 25, font_family= "NoxLauncher", color= self.titles_color)
                                                                            ],
                                                                            alignment= flet.MainAxisAlignment.CENTER,
                                                                            expand_loose= True
                                                                        ),
                                                                        alignment= flet.alignment.center,  
                                                                    ),
                                                                    flet.Container(
                                                                        content= flet.Dropdown(hint_text= "NoxLauncher Theme", options= [
                                                                            flet.dropdown.Option("Light", text_style= flet.TextStyle(size= 14, font_family= "NoxLauncher", color= self.titles_color)),
                                                                            flet.dropdown.Option("Dark", text_style= flet.TextStyle(size= 14, font_family= "NoxLauncher", color= self.titles_color)),
                                                                        ], border_color= self.subtitles_color, border_radius= 10, border_width= 2, hint_style= flet.TextStyle(size= 14, font_family= "NoxLauncher", color= self.titles_color), width= 230, value= get_theme(), on_change= self.update_theme),
                                                                        alignment= flet.alignment.center,
                                                                        expand_loose= True,
                                                                        padding= flet.padding.only(left= 40, right= 40, bottom= 25, top= 10)
                                                                    )
                                                                ],
                                                                horizontal_alignment= flet.CrossAxisAlignment.CENTER,
                                                                alignment= flet.MainAxisAlignment.CENTER,
                                                            ),
                                                            flet.Column(
                                                                controls= [
                                                                    flet.Container(
                                                                        content= flet.Row(
                                                                            controls= [
                                                                                flet.Icon(name= flet.icons.COLORIZE_SHARP, color= self.subtitles_color, size= 50),
                                                                                flet.Text("Colors", size= 25, font_family= "NoxLauncher", color= self.titles_color)
                                                                            ],
                                                                            alignment= flet.MainAxisAlignment.CENTER
                                                                        ),
                                                                        alignment= flet.alignment.center,  
                                                                        padding= flet.padding.only(right= 25, bottom= 10),
                                                                    ),
                                                                    flet.Row(
                                                                        controls= [
                                                                            flet.Column(
                                                                                controls= [
                                                                                    flet.Container(
                                                                                        content= flet.Text("Titles", size= 20, font_family= "NoxLauncher", color= self.titles_color),
                                                                                        alignment= flet.alignment.center,  
                                                                                    ),
                                                                                    flet.Container(
                                                                                        content= self.title_color_picker,
                                                                                        alignment= flet.alignment.center,
                                                                                        expand_loose= True,
                                                                                        padding= flet.padding.only(left= 10, right= 10, bottom= 25, top= 5)
                                                                                    ),
                                                                                    flet.Container(
                                                                                        content= flet.Text("Background", size= 20, font_family= "NoxLauncher", color= self.titles_color),
                                                                                        alignment= flet.alignment.center,  
                                                                                    ),
                                                                                    flet.Container(
                                                                                        content= self.bg_color_picker,
                                                                                        alignment= flet.alignment.center,
                                                                                        expand_loose= True,
                                                                                        padding= flet.padding.only(left= 10, right= 10, bottom= 25, top= 5)
                                                                                    ),
                                                                                    flet.Container(
                                                                                        content= flet.FilledButton(
                                                                                            text= "Reset",
                                                                                            style= flet.ButtonStyle(
                                                                                                color= self.titles_color,
                                                                                                bgcolor= self.filled_color,
                                                                                                text_style= flet.TextStyle(font_family= "NoxLauncher", size= 18, color= self.titles_color),
                                                                                                shape= flet.RoundedRectangleBorder(radius= 10)
                                                                                            ),
                                                                                            height= 50,
                                                                                            width= 150,
                                                                                            on_click= self.reset_colors,
                                                                                        ),
                                                                                        alignment= flet.alignment.center,
                                                                                        expand_loose= True,
                                                                                        padding= flet.padding.only(left= 10, right= 10, bottom= 25, top= 5)
                                                                                    )
                                                                                ],
                                                                                alignment= flet.MainAxisAlignment.CENTER,
                                                                                horizontal_alignment= flet.CrossAxisAlignment.CENTER
                                                                            ),
                                                                            flet.Column(
                                                                                controls= [
                                                                                    flet.Container(
                                                                                        content= flet.Text("SubTitles", size= 20, font_family= "NoxLauncher", color= self.titles_color),
                                                                                        alignment= flet.alignment.center,  
                                                                                    ),
                                                                                    flet.Container(
                                                                                        content= self.subtitles_color_picker,
                                                                                        alignment= flet.alignment.center,
                                                                                        expand_loose= True,
                                                                                        padding= flet.padding.only(left= 10, right= 10, bottom= 25, top= 5)
                                                                                    ),
                                                                                    flet.Container(
                                                                                        content= flet.Text("Filled", size= 20, font_family= "NoxLauncher", color= self.titles_color),
                                                                                        alignment= flet.alignment.center,  
                                                                                    ),
                                                                                    flet.Container(
                                                                                        content= self.filled_color_picker,
                                                                                        alignment= flet.alignment.center,
                                                                                        expand_loose= True,
                                                                                        padding= flet.padding.only(left= 10, right= 10, bottom= 25, top= 5)
                                                                                    ),
                                                                                    flet.Container(
                                                                                        content= flet.FilledButton(
                                                                                            text= "Apply",
                                                                                            style= flet.ButtonStyle(
                                                                                                color= self.titles_color,
                                                                                                bgcolor= self.filled_color,
                                                                                                text_style= flet.TextStyle(font_family= "NoxLauncher", size= 18, color= self.titles_color),
                                                                                                shape= flet.RoundedRectangleBorder(radius= 10)
                                                                                            ),
                                                                                            height= 50,
                                                                                            width= 150,
                                                                                            on_click= self.update_colors
                                                                                        ),
                                                                                        alignment= flet.alignment.center,
                                                                                        expand_loose= True,
                                                                                        padding= flet.padding.only(left= 10, right= 10, bottom= 25, top= 5)
                                                                                    )
                                                                                ],
                                                                                alignment= flet.MainAxisAlignment.CENTER,
                                                                                horizontal_alignment= flet.CrossAxisAlignment.CENTER
                                                                            )
                                                                        ],
                                                                        alignment= flet.MainAxisAlignment.CENTER,
                                                                        vertical_alignment= flet.CrossAxisAlignment.CENTER
                                                                    )
                                                                ],
                                                                horizontal_alignment= flet.CrossAxisAlignment.CENTER,
                                                                expand= True,
                                                                expand_loose= True,
                                                                alignment= flet.MainAxisAlignment.CENTER,
                                                            )
                                                        ],
                                                        alignment= flet.MainAxisAlignment.CENTER,
                                                        expand_loose= True,
                                                        expand= True,
                                                        vertical_alignment= flet.CrossAxisAlignment.CENTER,
                                                    ),
                                                    alignment= flet.alignment.center,
                                                    expand_loose= True,
                                                    expand= True,
                                                )
                                            ],
                                            horizontal_alignment= flet.CrossAxisAlignment.CENTER,
                                            expand= True,
                                            expand_loose= True
                                        ),
                                        width= 1100,
                                        height= 1050,
                                        bgcolor= self.bgcolor,
                                        border_radius= 20
                                    )
                                ],
                                alignment= flet.MainAxisAlignment.CENTER,
                                vertical_alignment= flet.CrossAxisAlignment.CENTER,
                                expand_loose= True
                            ),
                            flet.Container(
                                expand_loose= True,
                                height= 20  
                            ),
                        ],  
                        expand= True,
                        expand_loose= True,
                        scroll= flet.ScrollMode.AUTO,
                    ),
                    expand= True,
                    expand_loose= True,
                    image= flet.DecorationImage(src= "assets/bgsettings.png", fit= flet.ImageFit.COVER, filter_quality= flet.FilterQuality.HIGH, repeat= flet.ImageRepeat.NO_REPEAT),
                    alignment= flet.alignment.center
                )
            ],
            padding= 0
        )
    
    def update_theme(self, event: flet.ControlEvent) -> None:

        match event.control.value:
            case "Dark": 
                update_theme("Dark")
                self.page.theme_mode = flet.ThemeMode.DARK
                update_bgcolor("#272727")
                update_titlescolor("#FFFFFF")
            case "Light": 
                update_theme("Light")
                self.page.theme_mode = flet.ThemeMode.LIGHT
                update_bgcolor("#FFFFFF")
                update_titlescolor("#272727")

        UPDATE_THEME_BANNER: flet.Banner = flet.Banner(
            bgcolor= self.bgcolor,
            leading= flet.Icon(name= flet.icons.COLORIZE, color= self.subtitles_color, size= 40),
            content= flet.Container(content= flet.Text(
                value= f"NoxLauncher theme updated successfully, reload this section or the app!",
                color= self.titles_color,
                size= 20,
                font_family= "NoxLauncher"
            ), padding= flet.padding.only(bottom= 20, top= 20)),
            actions= [
                flet.TextButton(content= flet.Text("Ok", size= 20, font_family= "NoxLauncher", color= self.titles_color), style= flet.ButtonStyle(bgcolor= self.filled_color, color= self.titles_color, shape= flet.RoundedRectangleBorder(radius= 5)), width= 150, height= 40, on_click= lambda _: self.page.close(UPDATE_THEME_BANNER))
            ]
        )

        self.page.open(UPDATE_THEME_BANNER)

    def update_colors(self, _: flet.ControlEvent) -> None:

        update_bgcolor(self.bg_color_picker.color)
        update_titlescolor(self.title_color_picker.color)
        update_subtitlescolor(self.subtitles_color_picker.color)
        update_filledcolor(self.filled_color_picker.color)

        UPDATE_BANNER: flet.Banner = flet.Banner(
            bgcolor= self.bgcolor,
            leading= flet.Icon(name= flet.icons.COLORIZE, color= self.subtitles_color, size= 40),
            content= flet.Container(content= flet.Text(
                value= f"Color scheme update successfully, reload this section!",
                color= self.titles_color,
                size= 20,
                font_family= "NoxLauncher"
            ), padding= flet.padding.only(bottom= 20, top= 20)),
            actions= [
                flet.TextButton(content= flet.Text("Ok", size= 20, font_family= "NoxLauncher", color= self.titles_color), style= flet.ButtonStyle(bgcolor= self.filled_color, color= self.titles_color, shape= flet.RoundedRectangleBorder(radius= 5)), width= 150, height= 40, on_click= lambda _: self.page.close(UPDATE_BANNER))
            ]
        )

        self.page.open(UPDATE_BANNER)

    def reset_colors(self, _: flet.ControlEvent) -> None:

        update_bgcolor("#272727")
        update_titlescolor("#FFFFFF")
        update_subtitlescolor("#717171")
        update_filledcolor("#148b47")

        RESET_BANNER: flet.Banner = flet.Banner(
            bgcolor= self.bgcolor,
            leading= flet.Icon(name= flet.icons.COLORIZE, color= self.subtitles_color, size= 40),
            content= flet.Container(content= flet.Text(
                value= f"Color scheme reset successfully, reload this section!",
                color= self.titles_color,
                size= 20,
                font_family= "NoxLauncher"
            ), padding= flet.padding.only(bottom= 20, top= 20)),
            actions= [
                flet.TextButton(content= flet.Text("Ok", size= 20, font_family= "NoxLauncher", color= self.titles_color), style= flet.ButtonStyle(bgcolor= self.filled_color, color= self.titles_color, shape= flet.RoundedRectangleBorder(radius= 5)), width= 150, height= 40, on_click= lambda _: self.page.close(RESET_BANNER))
            ],
        )

        self.page.open(RESET_BANNER)

    
    def set_border_color_file_picker(self, control: flet_contrib.color_picker) -> None:

        for control in [control for control in [control for control in control.controls if isinstance(control, flet.Column)][0].controls if isinstance(control, flet.Row)][1].controls:

            if isinstance(control, flet.TextField):

                control.border_color = self.subtitles_color
                control.border_width = 2
                control.border_radius = 10
    
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
