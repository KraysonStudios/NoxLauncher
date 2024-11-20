import webbrowser
import requests

def has_internet() -> bool:

    try:
        return requests.get("https://google.com", timeout= 20).ok
    except:
        return False

def open_github() -> None: webbrowser.open("https://github.com/KraysonStudios/NoxLauncher")
def open_discord() -> None: webbrowser.open("https://discord.com/invite/DWfuQRsxwb")
def open_kofi() -> None: webbrowser.open("https://ko-fi.com/kraysonstudios")