import flet
import platform
import requests
import subprocess
import sys
import time
import os

from logs import info
from typing import List, Dict, Any
from constants import DEPLOYMENT_TYPE, VERSION

class NoxLauncherUpdater:

    def __init__(self, page: flet.Page) -> None:

        self.github_releases: str = "https://api.github.com/repos/KraysonStudios/NoxLauncher/releases" 
        self.headers: Dict[str, str] = {"User-Agent": "https://github.com/KraysonStudios/NoxLauncher"}
        self.page: flet.Page = page
        self.updater_text: flet.Text = flet.Text(value= "Checking for updates...", size= 20, font_family= "NoxLauncher", color= "#717171")

        self.updater_dialog: flet.AlertDialog = flet.AlertDialog(
            modal= True,
            icon= flet.Image(src= "assets/icon.png", width= 200, height= 170, filter_quality= flet.FilterQuality.HIGH),
            title= flet.Container(flet.Text("NoxLauncher", size= 40, font_family= "NoxLauncher"), alignment= flet.alignment.center),
            content= flet.Column(
                controls= [
                    self.updater_text,
                    flet.ProgressBar(width= 150, color= "#148b47")
                ],
                horizontal_alignment= flet.CrossAxisAlignment.CENTER,
                height= 70
            ),
            bgcolor= "#272727",
            on_dismiss= lambda _: None,
            content_padding= flet.padding.only(left= 20, right= 20)
        )

    def check_for_updates(self) -> None:

        info("Checking for updates...")
        
        self.page.open(self.updater_dialog)

        if not self.has_internet(): 
            
            self.page.close(self.updater_dialog)
            return
        
        latest_beta_url: List[str] | None = self._get_latest_beta()

        if latest_beta_url is None: return
        if not self.is_major(latest_beta_url[1]): 

            info("NoxLauncher is up to date.")

            self.updater_text.value = "NoxLauncher is up to date."
            self.updater_text.update()

            time.sleep(2)

            self.page.close(self.updater_dialog)

            return
        
        info(f"Downloading new version: {latest_beta_url[1]}")

        self.updater_text.value = f"Installing {latest_beta_url[1]}"
        self.updater_text.update()

        if not os.path.exists(f"{os.getcwd()}/{latest_beta_url[1]}"): 
            try:
                beta: requests.Response = requests.get(latest_beta_url[0], headers= self.headers, timeout= 10)
            except: return
            
            if beta.status_code != 200: return

            with open(f"{os.getcwd()}/{latest_beta_url[1]}", "wb") as file: file.write(beta.content)

        info(f"New version installed. Pls restart NoxLauncher.")

        self.updater_text.value = f"New version installed. Pls restart NoxLauncher."
        self.updater_text.update()

        subprocess.Popen(f"nohup \"{os.getcwd().replace('\\', '/')}/updater\" \"{os.getcwd().replace('\\', '/')}/{latest_beta_url[1]}\" \"{os.getcwd().replace('\\', '/')}\"", shell= True, stdout= subprocess.PIPE, stderr= subprocess.PIPE, stdin= subprocess.PIPE, text= True) if platform.system() == "Linux" else subprocess.Popen(f"start updater.exe \"{os.getcwd().replace('\\', '/')}/{latest_beta_url[1]}\" \"{os.getcwd().replace('\\', '/')}\"", shell= True, stdout= subprocess.PIPE, stderr= subprocess.PIPE, stdin= subprocess.PIPE, text= True, creationflags= 134217728)
        
        time.sleep(2)

        self.page.close(self.updater_dialog)
        self.page.window.destroy()

        return
        
    def _get_latest_beta(self) -> List[str]:

        try:
            all_releases: requests.Response = requests.get(self.github_releases, headers= self.headers, timeout= 10)
        except: return

        if all_releases.status_code != 200: return

        return [self._get_url(version["assets"]) for version in all_releases.json() if version["tag_name"] == "Betas"][0]
    
    def _get_url(self, assets: List[Dict[str, Any]]) -> List[str]:

        for version in assets:
            if version["name"].find(platform.system()) != -1:
                return [version["browser_download_url"], version["name"]]
            
    def is_major(self, version: str) -> bool:

        return sum([int(z) for z in version.split(".") if z.isdigit()]) > sum([int(z) for z in VERSION.split(".") if z.isdigit()])

    def has_internet(self) -> bool:

        try:
            return requests.get("https://google.com", timeout= 20).ok
        except:
            return False
            
        