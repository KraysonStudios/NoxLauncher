import flet
import fs

from gui import *
from logs import *
from constants import *

from dspresence import DiscordRPC

log("")
log(f"Welcome to NoxLauncher - {VERSION}")
log("")
log("Creators: @DevCheckOG & @aaronwayas at Github")
log("")
log("Github Repo: https://github.com/KraysonStudios/NoxLauncher")
log("")

fs.check_noxlauncher_filesystem()

if fs.get_discordrpc(): DiscordRPC()

def main(page: flet.Page) -> None: 

    NoxLauncherStandardWindowConfig(page)
    NoxLauncher(page)

flet.app(target= main, name= f"NoxLauncher {VERSION}")