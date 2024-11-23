import os
import datetime

class Logging:

    @staticmethod
    def add_log(message: str) -> None:         

        if not os.path.exists("noxlauncher.log"): 
            with open("noxlauncher.log", "w") as file: file.write("")
    
        with open("noxlauncher.log", "a") as file: file.write(message + "\n")

def info(message: str) -> None: 

    print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [INFO] {message}")
    Logging.add_log(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [INFO] {message}")
    
def log(message: str) -> None: 

    print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [LOG] {message}")
    Logging.add_log(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [LOG] {message}")

def error(message: str) -> None:

    print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [ERROR] {message}")
    Logging.add_log(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [ERROR] {message}")

def warn(message: str) -> None: 
    
    print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [WARN] {message}")
    Logging.add_log(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [WARN] {message}")

