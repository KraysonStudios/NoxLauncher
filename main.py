import flet
import signal

from fs import *
from gui import *
from logs import *
from constants import *
from utils import *

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

    NoxLauncherStandardWindowConfig(page)
    NoxLauncher(page)

flet.app(target= main, name= f"NoxLauncher {VERSION}")

NOXLAUNCHER_THREADPOOL.shutdown(wait= False, cancel_futures= True)
os._exit(0)