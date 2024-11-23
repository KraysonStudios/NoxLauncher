import json
import uuid
import requests

from typing import Dict, Any
from fs import *

class Account:

    @staticmethod
    def get_selected() -> tuple[Dict[str, Any], str] | None:

        check_noxlauncher_filesystem()

        with open(get_home() + "/accounts.json", "r") as file:

            freeaccs = json.load(file)

            if "nopremium" not in freeaccs or "premium" not in freeaccs: return None

            for acc in freeaccs["nopremium"]:
                if acc["selected"] and "token" in acc:
                    return (acc, "nopremium")
                elif acc["selected"] and "token" not in acc:
                    return (acc, "offline")
                
            for acc in freeaccs["premium"]:
                if acc["selected"]:
                    return (acc, "premium")

            return None

class NoPremium:

    def __init__(self) -> None:

        self.elyby_auth_api_url: str = "https://authserver.ely.by"
        self.headers: Dict[str, str] = {"User-Agent": "https://github.com/KraysonStudios/NoxLauncher"}

    @staticmethod 
    def new_offline(name: str) -> None:

        check_noxlauncher_filesystem()

        with open(get_home() + "/accounts.json", "r") as file:

            offaccs = json.load(file)

            if "nopremium" not in offaccs: offaccs["nopremium"] = []

            offaccs["nopremium"].append({
                "name": name,
                "selected": False
            })

        with open(get_home() + "/accounts.json", "w") as file: json.dump(offaccs, file, indent= 4)
        
    @staticmethod
    def get_accounts() -> List[Dict[str, Any]]:

        check_noxlauncher_filesystem()

        with open(get_home() + "/accounts.json", "r") as file: 

            freeaccs = json.load(file)

            if "nopremium" not in freeaccs: return []

            return freeaccs["nopremium"]
        
    def new(self, email: str, password: str) -> str | None:

        check_noxlauncher_filesystem()

        with open(get_home() + "/accounts.json", "r") as file:

            nopremiumaccs = json.load(file)

            if "nopremium" not in nopremiumaccs: 
                
                nopremiumaccs["nopremium"] = [] 

            ACCOUNT_CREDEANTIALS: Dict[str, Any] = {
                "username": email.strip(),
                "password": password.strip(),
                "clientToken": str(uuid.uuid4()),
                "requestUser": True
            }

            account: requests.Response = requests.post(f"{self.elyby_auth_api_url}/auth/authenticate", data= ACCOUNT_CREDEANTIALS, headers= self.headers)

            if account.status_code != 200: return None

            nopremiumaccs["nopremium"].append({
                "name": account.json()["user"]["username"],
                "uuid": account.json()["user"]["id"],
                "token": account.json()["accessToken"],
                "selected": False
            })
            
        with open(get_home() + "/accounts.json", "w") as file: json.dump(nopremiumaccs, file, indent= 4)

        return account.json()["user"]["username"]

    @staticmethod
    def delete(name: str) -> None:

        check_noxlauncher_filesystem()

        with open(get_home() + "/accounts.json", "r") as file:

            nopremiumaccs = json.load(file)

            if "nopremium" not in nopremiumaccs: return

            for acc in nopremiumaccs["nopremium"]:
                if acc["name"] == name:
                    nopremiumaccs["nopremium"].remove(acc)
                    break

        with open(get_home() + "/accounts.json", "w") as file: json.dump(nopremiumaccs, file, indent= 4)

    @staticmethod
    def select(name: str) -> None:

        check_noxlauncher_filesystem()

        with open(get_home() + "/accounts.json", "r") as file:

            nopremiumaccs = json.load(file)

            if "nopremium" not in nopremiumaccs: return

            for acc in nopremiumaccs["nopremium"]:
                if acc["name"] == name:
                    acc["selected"] = True
                    break

        with open(get_home() + "/accounts.json", "w") as file: json.dump(nopremiumaccs, file, indent= 4)