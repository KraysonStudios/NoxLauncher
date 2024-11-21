import flet
import sys

from gui import NoxLauncherAccountsGUI, NoxLauncherHelpGUI, NoxLauncherHomeGUI, NoxLauncherInfoGUI, NoxLauncherPlayGUI, NoxLauncherInstallFabricGUI, NoxLauncherInstallForgeGUI, NoxLauncherInstallGUI, NoxLauncherInstallVanillaGUI, NoxLauncherNoPremiumAccountsGUI, NoxLauncherSettingsGUI, NoxLauncherMCLogsGUI
from gui.utils import open_github, open_discord
from logs import error

from types import TracebackType

class NoxLauncher:

    def __init__(self, page: flet.Page) -> None:

        self.page: flet.Page = page
        self.routing: Routing = Routing(self.page)

        sys.excepthook = self.handle_uncaught_exception

        self.build()

    def build(self):

        self.routing.go("/home")

    def handle_uncaught_exception(self, type : type[BaseException], value : BaseException, traceback : TracebackType | None) -> None:   

        error(f"Exception Type: {type}")
        error(f"Exception: {value}")

        if traceback is not None: error(f"Traceback: {traceback}")

        self.page.open(
            flet.AlertDialog(
                icon= flet.Icon(name= flet.icons.ERROR, color= flet.colors.RED_600, size= 40),
                title= flet.Container(
                    content= flet.Text(value= "Uncaught Exception", size= 30, font_family= "NoxLauncher", color= "#FFFFFF"),
                    alignment= flet.alignment.center,
                    expand_loose= True
                ),
                bgcolor= "#272727",
                content= flet.Column(
                    [
                        flet.Text(value= f"Exception Type: {type}\nException: {value}\nTraceback: {traceback if traceback is not None else 'none'}", size= 18, font_family= "NoxLauncher", color= "#FFFFFF"),
                        flet.Container(height= 10),
                        flet.Text(value= f"Please report this error to our Discord Server or GitHub.", size= 18, font_family= "NoxLauncher", color= "#717171"),
                        flet.Container(height= 10),
                        flet.Row(
                            controls= [
                                flet.Container(content= flet.Image(src= "assets/discord.png", width= 52, height= 52, filter_quality= flet.FilterQuality.HIGH), on_click= lambda _: open_discord()),
                                flet.Container(content= flet.Image(src= "assets/github.png", width= 52, height= 52, filter_quality= flet.FilterQuality.HIGH), on_click= lambda _: open_github()),
                            ],
                            expand_loose= True,
                            alignment= flet.MainAxisAlignment.CENTER,
                            vertical_alignment= flet.CrossAxisAlignment.CENTER,
                            height= 55,
                            spacing= 40,
                            run_spacing= 40
                        )
                    ],
                    alignment= flet.MainAxisAlignment.CENTER,
                    horizontal_alignment= flet.CrossAxisAlignment.CENTER,
                    height= 200,
                    expand_loose= True
                )
            )
        ) 

class Routing:

    def __init__(self, page: flet.Page) -> None:

        self.page: flet.Page = page
        self.build()

    def build(self):

        def routing(_: flet.RouteChangeEvent) -> None:
            self.page.views.clear()

            match self.page.route:
                case "/home": self.append(NoxLauncherHomeGUI(self.page).build())
                case "/settings": self.append(NoxLauncherSettingsGUI(self.page).build())
                case "/help": self.append(NoxLauncherHelpGUI(self.page).build())
                case "/play": self.append(NoxLauncherPlayGUI(self.page).build())
                case "/accounts": self.append(NoxLauncherAccountsGUI(self.page).build())
                case "/accounts/nopremium": self.append(NoxLauncherNoPremiumAccountsGUI(self.page).build())
                case "/info": self.append(NoxLauncherInfoGUI(self.page).build())
                case "/install": self.append(NoxLauncherInstallGUI(self.page).build())
                case "/install/fabric": self.append(NoxLauncherInstallFabricGUI(self.page).build())
                case "/install/forge": self.append(NoxLauncherInstallForgeGUI(self.page).build())
                case "/install/vanilla": self.append(NoxLauncherInstallVanillaGUI(self.page).build())
                case "/mclogs": self.append(NoxLauncherMCLogsGUI(self.page).build())

            self.page.update()

        self.page.on_route_change = routing

    def append(self, view: flet.View) -> None: self.page.views.append(view)

    def go(self, route: str) -> None: self.page.go(route)