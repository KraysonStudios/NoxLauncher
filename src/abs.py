try:

    import flet

    from typing import Callable, List

except Exception as e:

    print(f"Report this error to the developers: \n{e.args[0]}")
    exit(1)

##########################################################

# NoxLauncher Generic Widgets

##########################################################

class NoxLauncherContainer(flet.Container):

    def __init__(self, 
        content: flet.Control | None = None, 
        expand: bool | None = False, 
        expand_loose: bool | None = False, 
        width: int | None = None, 
        height: int | None = None,
        bgcolor: str | None = None,
        alignment: flet.alignment.Alignment | None = None,
        padding: flet.padding.Padding | None = None,
        border: flet.border.Border | None = None,
        border_radius: int | None = None,
        image_src: str | None = None,
        image_fit: flet.ImageFit | None = None,
        callback: Callable | None = None
    ) -> None:
        super().__init__(
            content= content, 
            expand= expand, 
            expand_loose= expand_loose, 
            width= width, 
            height= height, 
            bgcolor= bgcolor,
            alignment= alignment,
            border_radius= border_radius,
            padding= padding,
            border= border,
            image_src= image_src,
            image_fit= image_fit,
            on_click= callback
        )

    def destroy(self) -> None:
        self.page.remove(self)

class NoxLauncherColumn(flet.Column):

    def __init__(self, 
        controls: List[flet.Control] | None = None, 
        height: int | None = None,
        width: int | None = None,
        spacing: int = 0, 
        expand: bool = False, 
        expand_loose: bool = False,
        alignment: flet.MainAxisAlignment | None = None,
        horizontal_alignment: flet.CrossAxisAlignment | None = None,
        scroll: flet.ScrollMode | None = None
    ) -> None:
        super().__init__(
            controls= controls, 
            height= height,
            width= width,
            spacing= spacing, 
            expand= expand, 
            expand_loose= expand_loose,
            alignment= alignment,
            horizontal_alignment= horizontal_alignment,
            scroll= scroll
        )

    def extend(self, controls: List[flet.Control]) -> None:
        self.controls.extend(controls)
        self.update()

    def destroy(self) -> None:
        self.page.remove(self)

class NoxLauncherRow(flet.Row):

    def __init__(self, 
        controls: List[flet.Control] | None = None, 
        height: int | None = None,
        width: int | None = None,
        spacing: int | None = None, 
        expand: bool = False, 
        expand_loose: bool = False,
        alignment: flet.MainAxisAlignment | None = None,
        vertical_alignment: flet.CrossAxisAlignment | None = None,
        scroll: flet.ScrollMode | None = None
    ) -> None:
        super().__init__(
            controls= controls, 
            height= height,
            width= width,
            spacing= spacing, 
            expand= expand, 
            expand_loose= expand_loose,
            alignment= alignment,
            vertical_alignment= vertical_alignment,
            scroll= scroll
        )

class NoxLauncherView(flet.View):

    def __init__(self, controls: List[flet.Control] | None = None, padding: int = 0) -> None:
        super().__init__(controls= controls, padding= padding)

class NoxLauncherDropdown(flet.Dropdown):

    def __init__(self, 
        value: str | None = None,
        options: List[str] | None = None, 
        hint_text: str | None = None,
        label: str | None = None,
        border_radius: int = 20,
        border_color: str | None = None,
        border_width: int = 2,
        label_style: flet.TextStyle | None = None,
        on_change: Callable | None = None,
    ) -> None:
        super().__init__(
            value= value,
            options= options, 
            hint_text= hint_text,
            label= label,
            border_radius= border_radius,
            border_color= border_color,
            border_width= border_width,
            label_style= label_style,
            on_change= on_change
        )
    
    def disable(self) -> None:
        self.disabled = True
        self.update()

    def destroy(self) -> None:
        self.page.remove(self)

class NoxLauncherBanner(flet.Banner):

    def __init__(self, 
        leading: flet.Control | None = None,
        actions: List[flet.Control] | None = None,
        content: flet.Control | None = None, 
        bgcolor: str | None = None
    ) -> None:
        super().__init__(
            leading= leading,
            actions= actions,
            content= content, 
            bgcolor= bgcolor
        )

    def destroy(self) -> None:
        self.page.remove(self)