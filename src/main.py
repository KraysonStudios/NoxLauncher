import flet
import platform

from gui import NoxLauncher
from constants import constants
from linux.fs import Linux
from tkinter.messagebox import showerror

if __name__ == "__main__":

    if not platform.system() in ["Linux", "Windows"]:
        showerror(title= "Nox Launcher", message= "Unsupported platform.", type= "ok")
        exit(1)

    match platform.system():

        case "Windows": ...
        case "Linux": Linux.config()

    def main(page: flet.Page) -> None:

        page.title = "Nox Launcher"

        page.window_max_height = constants.MAX_HEIGHT.value
        page.window_max_width = constants.MAX_WIDTH.value

        page.window_min_height = constants.MIN_HEIGHT.value
        page.window_min_width = constants.MIN_WIDTH.value

        page.fonts = {"Minecraft": "fonts/Minecraft.ttf"}

        page.update()

        NoxLauncher.build(page)

    flet.app(target= main, name= "Nox Launcher")