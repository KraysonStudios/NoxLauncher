import pypresence
import time
import psutil

from utils import NOXLAUNCHER_THREAD_POOL
from constants import constants

RPC: pypresence.Presence = pypresence.Presence(constants.DISCORD_CLIENT_ID.value)

rpc_connected, discord_opened = False, False

def _start() -> None:

    global discord_opened

    try:

        RPC.connect()
        rpc_connected = True

    except: rpc_connected = False

    if rpc_connected: 
        while True: 

            try: 
        
                RPC.update(
                    state= "Playing NoxLauncher...",
                    details= "Powerful and easy-to-use Minecraft Launcher develop by Krayson Studio.",
                    large_image= "discord_rpc",
                    large_text= "Krayson Studio",
                    start= int(time.time())
                )

                time.sleep(10)
            
            except:

                RPC.clear()
                RPC.close()
                discord_opened = False
                rpc_connected = False
                return

def DiscordRPC() -> None:

    global discord_opened

    while True:

        if not discord_opened:

            for program in psutil.process_iter():

                if program.name().find("Discord") != -1:

                    NOXLAUNCHER_THREAD_POOL.submit(_start)
                    discord_opened = True
                    break

            else: discord_opened = False

        time.sleep(10)