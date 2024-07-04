import flet
import platform

from gui import NoxLauncher
from constants import constants
from fs import Config
from tkinter.messagebox import showerror

if __name__ == "__main__":

    if not platform.system() in ["Linux", "Windows"]:
        showerror(title= "Nox Launcher", message= "Unsupported platform.", type= "ok")
        exit(1)

    def main(page: flet.Page) -> None:

        Config.check()

        page.title = "Nox Launcher"

        page.window.max_height = constants.MAX_HEIGHT.value
        page.window.max_width = constants.MAX_WIDTH.value

        page.window.min_height = constants.MIN_HEIGHT.value
        page.window.min_width = constants.MIN_WIDTH.value

        page.fonts = {"Minecraft": "fonts/Minecraft.ttf"}

        page.update()

        NoxLauncher.build(page)

    flet.app(target= main, name= "Nox Launcher")