import flet
import requests
import datetime
import time

from fs import check_noxlauncher_filesystem, get_home
from gui.utils import has_internet
from typing import Dict, Any, List

class ModrinthAPI:

    def __init__(self, page: flet.Page, loader: str) -> None:

        self.page: flet.Page = page
        self.loader: str = loader
        self.rate_limiter_data: Dict[str, Any] = {"count": 0, "time": datetime.datetime.now(), "blocked": False}
        self.base_api_url: str = "https://api.modrinth.com/v2"
        self.headers: Dict[str, str] = {"User-Agent": "https://github.com/KraysonStudios/NoxLauncher"}
        self.container: flet.Container = flet.Container(expand= True, expand_loose= True, alignment= flet.alignment.center)

    def search_projects(self, query: str) -> None:

        if self.rate_limiter(): 

            self.container.content = flet.Text("Please wait a few seconds before searching again.", size= 20, font_family= "NoxLauncher")
            self.container.update()
            return

        if not has_internet(): return

        params: Dict[str, Any] = {
            "query": query,
            "limit": 20,
            "index": "downloads",
        }

        response: requests.Response = requests.get(f"{self.base_api_url}/search", params= params, headers= self.headers, timeout= 10)

        if response.status_code != 200:

            self.container.content = flet.Text("Something went wrong. Please try again later.", size= 20, font_family= "NoxLauncher")
            self.container.update()
            return
        
        elif response.json()["total_hits"] == 0:
            self.container.content = flet.Text("No results found!", size= 20, font_family= "NoxLauncher")
            self.container.update()
            return
        
        self.container.content = flet.Column(
            controls= [],
            expand_loose= True,
            expand= True,
            scroll= flet.ScrollMode.ADAPTIVE
        )
        
        for project in [project for project in response.json()["hits"] if self.loader in project["categories"]]:
            project: Dict[str, Any] = self.idiomatic_project(project)

            self.container.content.controls.append(
                flet.Container(
                    content= flet.Column(
                        controls= [
                            flet.Container(
                                content= flet.Image(src= project["icon"], width= 50, height= 50, filter_quality= flet.FilterQuality.HIGH, error_content= flet.Container(width= 50, height= 50, alignment= flet.alignment.center, content= flet.Text("?", size= 20, font_family= "NoxLauncher"))),
                                alignment= flet.alignment.center,
                                expand_loose= True,
                                border_radius= 20,
                                padding= flet.padding.only(bottom= 30)
                            ),
                            flet.Container(
                                content= flet.Text(project["name"], size= 28, font_family= "NoxLauncher"),
                                alignment= flet.alignment.center,
                                expand_loose= True
                            ),
                            flet.Container(
                                content= flet.Row(
                                    controls= [
                                        flet.Image(src= "downloads.png", width= 50, height= 50, filter_quality= flet.FilterQuality.HIGH),
                                        flet.Text(project["downloads"], size= 18, font_family= "NoxLauncher")
                                    ],
                                    expand_loose= True,
                                    spacing= 20
                                ),
                                alignment= flet.alignment.center_left,
                                expand_loose= True,
                                padding= flet.padding.only(top= 10, bottom= 10)
                            ),
                            flet.Container(
                                content= flet.Row(
                                    controls= [
                                        flet.Image(src= "mods.png", width= 50, height= 50, filter_quality= flet.FilterQuality.HIGH),
                                        flet.Text(", ".join(project["versions"]), size= 16, font_family= "NoxLauncher")
                                    ],
                                    expand_loose= True,
                                    spacing= 20,
                                    scroll= flet.ScrollMode.AUTO,
                                    alignment= flet.MainAxisAlignment.START
                                ),
                                alignment= flet.alignment.center_left,
                                expand_loose= True,
                                padding= flet.padding.only(top= 10, bottom= 10)
                            ),
                            flet.Container(
                                content= flet.Text(project["description"], size= 16, font_family= "NoxLauncher"),
                                alignment= flet.alignment.center_left,
                                expand_loose= True
                            ),
                            flet.Container(
                                content= flet.Dropdown(hint_text= "Install the mod!", options= [flet.dropdown.Option(version, text_style= flet.TextStyle(size= 14, font_family= "NoxLauncher")) for version in project["versions"]], border_color= "#717171", border_radius= 10, border_width= 2, hint_style= flet.TextStyle(size= 14, font_family= "NoxLauncher"), on_change= self.install_mod, data= {"slug": project["id"], "icon": project["icon"]}),
                                expand_loose= True,
                                alignment= flet.alignment.center,
                                padding= 5
                            )
                        ],
                        horizontal_alignment= flet.CrossAxisAlignment.CENTER,
                        expand_loose= True,
                        expand= True
                    ),
                    height= 500,
                    expand_loose= True,
                    padding= 20
                )
            )

        self.container.update()

    def idiomatic_project(self, project: Dict[str, Any]) -> Dict[str, Any]:

        description: str = project["description"].replace("\n", " ")
        icon_url: str = project["icon_url"]

        if len(description) > 100: description = description[:100] + "..."
        if len(icon_url) == 0: icon_url = "icon.png"

        return {
            "id": project["slug"],
            "name": project["title"],
            "description": description,
            "icon" : icon_url,
            "downloads": project["downloads"],
            "versions": project["versions"]
        }


    def rate_limiter(self) -> bool: 

        if self.rate_limiter_data["count"] >= 5 and not self.rate_limiter_data["blocked"]:

            self.rate_limiter_data["time"] =  datetime.datetime.now() + datetime.timedelta(seconds= 15)
            self.rate_limiter_data["blocked"] = True
            return True

        elif self.rate_limiter_data["time"] <= datetime.datetime.now() and self.rate_limiter_data["blocked"]: 

            self.rate_limiter_data["count"] = 0
            self.rate_limiter_data["time"] = datetime.datetime.now()
            self.rate_limiter_data["blocked"] = False
            return False
        
        elif self.rate_limiter_data["count"] >= 5: return True

        self.rate_limiter_data["count"] += 1
        
        return False
    
    def install_mod(self, event: flet.ControlEvent) -> None: 

        if not has_internet(): return

        response: requests.Response = requests.get(f"https://api.modrinth.com/v2/project/{event.control.data['slug']}/version", headers= self.headers, timeout= 10)

        if response.status_code != 200: 

            event.control.parent.content = flet.Row(
                controls= [
                    flet.Container(height= 60, width= 10, bgcolor= "#eb3434"),
                    flet.Text("Something went wrong. Please try again later.", size= 15, font_family= "NoxLauncher")
                ],
                spacing= 20,
                run_spacing= 20,
                expand_loose= True
            )

            event.control.parent.update()

            time.sleep(3)
            
            return

        matching_versions: List[Dict[str, Any]] = [
            version for version in response.json()
            if event.control.value in version["game_versions"] and self.loader in version["loaders"]
        ]

        matching_versions.sort(key= lambda date: date["date_published"], reverse= True)

        file: requests.Response = requests.get(matching_versions[0]["files"][0]["url"], headers= self.headers, timeout= 60*2)

        if file.status_code != 200: 

            event.control.parent.content = flet.Row(
                controls= [
                    flet.Container(height= 60, width= 10, bgcolor= "#eb3434"),
                    flet.Text("Something went wrong attempting to download the mod. Please try again later.", size= 15, font_family= "NoxLauncher")
                ],
                spacing= 20,
                run_spacing= 20,
                expand_loose= True
            )

            event.control.parent.update()

            time.sleep(3)
            
            return

        check_noxlauncher_filesystem()

        with open(f"{get_home()}/mods/{matching_versions[0]["files"][0]["filename"]}", "wb") as jar: jar.write(file.content)

        successful_install: flet.AlertDialog = flet.AlertDialog(
            icon= flet.Image(src= event.control.data["icon"], width= 60, height= 60, filter_quality= flet.FilterQuality.HIGH),
            title= flet.Container(
                content= flet.Text(event.control.data["slug"].capitalize(), size= 18, font_family= "NoxLauncher", color= "#FFFFFF"),
                alignment= flet.alignment.center,
                expand_loose= True
            ),
            bgcolor= "#272727",
            content= flet.Column(
                [
                    flet.Text(value= matching_versions[0]["files"][0]["filename"], size= 18, font_family= "NoxLauncher", color= "#717171"),
                    flet.Text(value= "Has been installed!", size= 16, font_family= "NoxLauncher", color= "#FFFFFF")
                ],
                alignment= flet.MainAxisAlignment.CENTER,
                horizontal_alignment= flet.CrossAxisAlignment.CENTER,
                height= 130,
                expand_loose= True
            ),
            on_dismiss= lambda _: self.page.close(successful_install)
            
        )

        self.page.open(successful_install)
