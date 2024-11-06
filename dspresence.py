import time
import psutil
import pypresence

from threadpool import NOXLAUNCHER_THREADPOOL
from constants import DISCORD_CLIENT_ID

RPC: pypresence.Presence = pypresence.Presence(DISCORD_CLIENT_ID)

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
                    details= "NoxLauncher is a powerful Open Source launcher created by Krayson Studio and its main developers, to provide secure access to a minecraft launcher.",
                    large_image= "discord_rpc",
                    large_text= "Krayson Studio"
                )

                time.sleep(10)
            
            except:

                RPC.clear()
                RPC.close()
                discord_opened = False
                rpc_connected = False
                return

def DiscordRPC() -> None:

    def _init() -> None: 

        global discord_opened

        while True:

            if not discord_opened:

                for program in psutil.process_iter():

                    if program.name().find("Discord") != -1:

                        NOXLAUNCHER_THREADPOOL.submit(_start)
                        discord_opened = True
                        break

                else: discord_opened = False

            time.sleep(10)

    NOXLAUNCHER_THREADPOOL.submit(_init)