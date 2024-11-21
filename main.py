import os
import flet
import sys
import signal

from fs import check_noxlauncher_filesystem, get_discordrpc
from logs import log
from constants import *
from launcher import NoxLauncher
from threadpool import NOXLAUNCHER_THREADPOOL

from dspresence import DiscordRPC

signal.signal(signal.SIGINT, signal.SIG_IGN)

log("")
log(f"Welcome to NoxLauncher ({DEPLOYMENT_TYPE}) - v{VERSION}")
log("")
log("Creators: @DevCheckOG & @aaronwayas at Github")
log("")
log("Github Repo: https://github.com/KraysonStudios/NoxLauncher")
log("")

check_noxlauncher_filesystem()

if get_discordrpc(): DiscordRPC()

def main(page: flet.Page) -> None: 

    page.title = f"NoxLauncher ({DEPLOYMENT_TYPE}) - v{VERSION}"

    page.window.icon = os.path.join(os.getcwd().replace("\\", "/"), "assets/icon.ico")

    page.fonts = {
        "NoxLauncher": "assets/fonts/minecraft.ttf",
    }
    
    page.window.width = 1280
    page.window.height = 720
    page.theme_mode = flet.ThemeMode.DARK

    page.update()

    NoxLauncher(page)

flet.app(target= main, name= f"NoxLauncher {VERSION}")

NOXLAUNCHER_THREADPOOL.shutdown(wait= False, cancel_futures= True)
sys.exit(0)