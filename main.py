import os
import flet
import sys
import signal

from fs import check_noxlauncher_filesystem, get_discordrpc
from logs import info
from constants import DEPLOYMENT_TYPE, VERSION
from launcher import NoxLauncher
from threadpool import NOXLAUNCHER_THREADPOOL
from noxupdater import NoxLauncherUpdater

from dspresence import DiscordRPC

signal.signal(signal.SIGINT, signal.SIG_IGN)

info("")
info(f"Welcome to NoxLauncher ({DEPLOYMENT_TYPE}) - v{VERSION}")
info("")
info("Creators: @DevCheckOG & @aaronwayas at Github")
info("")
info("Github Repo: https://github.com/KraysonStudios/NoxLauncher")
info("")

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

    NOXLAUNCHER_THREADPOOL.submit(NoxLauncherUpdater(page).check_for_updates())

flet.app(target= main, name= f"NoxLauncher ({DEPLOYMENT_TYPE}) - v{VERSION}")

NOXLAUNCHER_THREADPOOL.shutdown(wait= False, cancel_futures= True)
sys.exit(0)