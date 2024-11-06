import os
import datetime

from colorama import Fore, Style

class Logging:

    @staticmethod
    def add_log(message: str) -> None:         

        if not os.path.exists("noxlauncher.log"): 
            with open("noxlauncher.log", "w") as file: file.write("")
    
        with open("noxlauncher.log", "a") as file: 

            file.write(message + "\n")
    
def log(message: str) -> None: 

    print(Style.BRIGHT + f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} " + "[" + Fore.LIGHTGREEN_EX + "LOG" + Style.RESET_ALL + Style.BRIGHT + "] " + Style.RESET_ALL + message)
    Logging.add_log(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [LOG] {message}")

def error(message: str) -> None:

    print(Style.BRIGHT + f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} " + "[" + Fore.LIGHTRED_EX + "ERROR" + Style.RESET_ALL + Style.BRIGHT + "] " + Style.RESET_ALL + message)
    Logging.add_log(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [ERROR] {message}")

def warn(message: str) -> None: 
    
    print(Style.BRIGHT + f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} " + "[" + Fore.LIGHTYELLOW_EX + "WARN" + Style.RESET_ALL + Style.BRIGHT + "] " + Style.RESET_ALL + message)
    Logging.add_log(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [WARN] {message}")

