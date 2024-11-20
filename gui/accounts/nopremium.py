import flet

from accounts import NoPremium
from gui.appbar import NoxLauncherGenericAppBar
from gui.utils import has_internet

class NoxLauncherNoPremiumAccountsGUI:

    def __init__(self, page: flet.Page) -> None:

        self.page: flet.Page = page
        self.select_account_dropdown: flet.Dropdown = flet.Dropdown(hint_text= "Select a default account!", options= [flet.dropdown.Option(account["name"], text_style= flet.TextStyle(size= 14, font_family= "NoxLauncher")) for account in NoPremium.get_accounts()], border_color= "#717171", border_radius= 10, border_width= 2, hint_style= flet.TextStyle(size= 14, font_family= "NoxLauncher"), on_change= self.select_account)
        self.delete_account_dropdown: flet.Dropdown = flet.Dropdown(hint_text= "Select a account to delete!", options= [flet.dropdown.Option(account["name"], text_style= flet.TextStyle(size= 14, font_family= "NoxLauncher")) for account in NoPremium.get_accounts()], border_color= "#717171", border_radius= 10, border_width= 2, hint_style= flet.TextStyle(size= 14, font_family= "NoxLauncher"), on_change= self.delete_account)
        self.email_textfield: flet.TextField = flet.TextField(multiline= False, expand_loose= True, height= 70, border_radius= 10, border_color= "#717171", label= "Email", label_style= flet.TextStyle(size= 16, font_family= "NoxLauncher", color= "#FFFFFF"), hint_text= "Email of the account in elyby", hint_style= flet.TextStyle(size= 16, font_family= "NoxLauncher"), text_style= flet.TextStyle(size= 14, font_family= "NoxLauncher", color= "#FFFFFF"))
        self.password_textfield: flet.TextField = flet.TextField(multiline= False, expand_loose= True, height= 70, border_radius= 10, border_color= "#717171", label= "Password", label_style= flet.TextStyle(size= 16, font_family= "NoxLauncher", color= "#FFFFFF"), hint_text= "Password of the account in elyby", hint_style= flet.TextStyle(size= 16, font_family= "NoxLauncher"), text_style= flet.TextStyle(size= 14, font_family= "NoxLauncher", color= "#FFFFFF"), password= True, can_reveal_password= True)

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
                                                    flet.Icon(name= flet.icons.LOGIN, color= "#717171", size= 40),
                                                    flet.Container(flet.Text("Login", size= 25, font_family= "NoxLauncher", color= "#FFFFFF"), alignment= flet.alignment.center, expand_loose= True, padding= flet.padding.only(top= 5)),  
                                                ],
                                                expand_loose= True,
                                                alignment= flet.MainAxisAlignment.CENTER
                                            ),
                                            padding= flet.padding.only(top= 20, bottom= 20)
                                        ),
                                        flet.Container(
                                            content= flet.Row(
                                                controls= [
                                                    flet.Icon(name= flet.icons.ACCOUNT_BOX, color= "#717171", size= 35),
                                                    flet.Text("First create a account at https://ely.by/", size= 18, font_family= "NoxLauncher", color= "#FFFFFF"),
                                                ],
                                                expand_loose= True,
                                                alignment= flet.MainAxisAlignment.CENTER,
                                                vertical_alignment= flet.CrossAxisAlignment.CENTER
                                            ),
                                            expand_loose= True,
                                            alignment= flet.alignment.center,
                                            padding= flet.padding.only(left= 10, right= 10, bottom= 15)
                                        ),
                                        flet.Container(
                                            content= self.email_textfield,
                                            expand_loose= True,
                                            alignment= flet.alignment.center,
                                            padding= flet.padding.only(left= 15, right= 15)
                                        ),
                                        flet.Container(
                                            content= self.password_textfield,
                                            expand_loose= True,
                                            alignment= flet.alignment.center,
                                            padding= flet.padding.only(left= 15, right= 15)
                                        ),
                                        flet.Container(
                                            content= flet.FilledButton(
                                                icon= flet.icons.LOGIN,
                                                icon_color= "#717171",
                                                text= "Login at Elyby",
                                                style= flet.ButtonStyle(bgcolor= "#272727", color= "#FFFFFF", text_style= flet.TextStyle(size= 20, font_family= "NoxLauncher")),
                                                height= 50,
                                                on_click= self.login_account
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
                                width= 480,
                                height= 380
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
                        run_spacing= 30,
                        spacing= 30
                    ),
                    expand= True,
                    expand_loose= True,
                    alignment= flet.alignment.center
                ),
            ],
            padding= 0
        )
    
    def login_account(self, event: flet.ControlEvent) -> None:

        if self.email_textfield.value == "" or self.email_textfield.value.isspace() or self.email_textfield.value.find("@") == -1: 

            email_account_banner: flet.Banner = flet.Banner(
                bgcolor= "#272727",
                leading= flet.Icon(name= flet.icons.WARNING, color= flet.colors.AMBER_400, size= 40),
                content= flet.Text(
                    value= f"The email \" {self.email_textfield.value} \" is invalid name to be signed!",
                    color= "#ffffff",
                    size= 20,
                    font_family= "NoxLauncher"
                ),
                actions= [
                    flet.TextButton(content= flet.Text("Ok", size= 20, font_family= "NoxLauncher"), style= flet.ButtonStyle(bgcolor= "#148b47", color= "#ffffff", shape= flet.RoundedRectangleBorder(radius= 5)), width= 150, height= 40, on_click= lambda _: self.page.close(email_account_banner))
                ]
            )

            self.page.open(email_account_banner)

            self.email_textfield.value = ""
            self.email_textfield.update()

            return
        
        elif self.password_textfield.value == "" or self.password_textfield.value.isspace():

            password_account_banner: flet.Banner = flet.Banner(
                bgcolor= "#272727",
                leading= flet.Icon(name= flet.icons.WARNING, color= flet.colors.AMBER_400, size= 40),
                content= flet.Text(
                    value= f"The password \" {self.password_textfield.value} \" is invalid name to be signed!",
                    color= "#ffffff",
                    size= 20,
                    font_family= "NoxLauncher"
                ),
                actions= [
                    flet.TextButton(content= flet.Text("Ok", size= 20, font_family= "NoxLauncher"), style= flet.ButtonStyle(bgcolor= "#148b47", color= "#ffffff", shape= flet.RoundedRectangleBorder(radius= 5)), width= 150, height= 40, on_click= lambda _: self.page.close(password_account_banner))
                ]
            )

            self.page.open(password_account_banner)

            self.password_textfield.value = ""
            self.password_textfield.update() 

            return
        
        if not has_internet():
            internet_banner: flet.Banner = flet.Banner(
                bgcolor= "#272727",
                leading= flet.Icon(name= flet.icons.ERROR, color= flet.colors.RED_500, size= 40),
                content= flet.Text(
                    value= f"You have no internet connection! Please check your internet connection and try again.",
                    color= "#ffffff",
                    size= 20,
                    font_family= "NoxLauncher"
                ),
                actions= [
                    flet.TextButton(content= flet.Text("Ok", size= 20, font_family= "NoxLauncher"), style= flet.ButtonStyle(bgcolor= "#148b47", color= "#ffffff", shape= flet.RoundedRectangleBorder(radius= 5)), width= 150, height= 40, on_click= lambda _: self.page.close(internet_banner))
                ]
            )

            self.page.open(internet_banner)

        account: str | None = NoPremium().new(self.email_textfield.value, self.password_textfield.value)

        if account is None:
            
            account_error_banner: flet.Banner = flet.Banner(
                bgcolor= "#272727",
                leading= flet.Icon(name= flet.icons.ERROR, color= flet.colors.RED_500, size= 40),
                content= flet.Text(
                    value= f"Failed to login account! Please check your email and password and try again.",
                    color= "#ffffff",
                    size= 20,
                    font_family= "NoxLauncher"
                ),
                actions= [
                    flet.TextButton(content= flet.Text("Ok", size= 20, font_family= "NoxLauncher"), style= flet.ButtonStyle(bgcolor= "#148b47", color= "#ffffff", shape= flet.RoundedRectangleBorder(radius= 5)), width= 150, height= 40, on_click= lambda _: self.page.close(account_error_banner))
                ]
            )

            self.page.open(account_error_banner)

            return

        created_account_banner: flet.Banner = flet.Banner(
            bgcolor= "#272727",
            leading= flet.Icon(name= flet.icons.CREATE, color= "#717171", size= 40),
            content= flet.Text(
                value= f"Logged as \" {account} \" successfully!",
                color= "#ffffff",
                size= 20,
                font_family= "NoxLauncher"
            ),
            actions= [
                flet.TextButton(content= flet.Text("Ok", size= 20, font_family= "NoxLauncher"), style= flet.ButtonStyle(bgcolor= "#148b47", color= "#ffffff", shape= flet.RoundedRectangleBorder(radius= 5)), width= 150, height= 40, on_click= lambda _: self.page.close(created_account_banner))
            ]
        )

        self.email_textfield.value = ""
        self.password_textfield.value = ""

        self.email_textfield.update()
        self.password_textfield.update()

        self.page.open(created_account_banner)

        self.delete_account_dropdown.options = [flet.dropdown.Option(account["name"], text_style= flet.TextStyle(size= 14, font_family= "NoxLauncher")) for account in NoPremium.get_accounts()]
        self.select_account_dropdown.options = [flet.dropdown.Option(account["name"], text_style= flet.TextStyle(size= 14, font_family= "NoxLauncher")) for account in NoPremium.get_accounts()]

        self.delete_account_dropdown.update()
        self.select_account_dropdown.update()

    def delete_account(self, event: flet.ControlEvent) -> None:

        NoPremium.delete(event.control.value)

        self.delete_account_dropdown.options = [flet.dropdown.Option(account["name"], text_style= flet.TextStyle(size= 14, font_family= "NoxLauncher")) for account in NoPremium.get_accounts()]
        self.select_account_dropdown.options = [flet.dropdown.Option(account["name"], text_style= flet.TextStyle(size= 14, font_family= "NoxLauncher")) for account in NoPremium.get_accounts()]

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

        NoPremium.select(event.control.value)

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
