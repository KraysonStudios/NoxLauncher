import json

from typing import Dict, Any
from fs import *

class Account:

    @staticmethod
    def get_selected() -> tuple[Dict[str, Any], str] | None:

        check_noxlauncher_filesystem()

        with open(get_home() + "/accounts.json", "r") as file:

            freeaccs = json.load(file)

            if "free" not in freeaccs or "premium" not in freeaccs: return None

            for acc in freeaccs["free"]:
                if acc["selected"]:
                    return (acc, "free")
                
            for acc in freeaccs["premium"]:
                if acc["selected"]:
                    return (acc, "premium")

            return None

class FreeACC:

    @staticmethod
    def get_accounts() -> List[Dict[str, Any]]:

        check_noxlauncher_filesystem()

        with open(get_home() + "/accounts.json", "r") as file: 

            freeaccs = json.load(file)

            if "free" not in freeaccs: return []

            return freeaccs["free"]
        
    @staticmethod
    def new(name: str, selected: bool = False) -> None:

        check_noxlauncher_filesystem()

        with open(get_home() + "/accounts.json", "r") as file:

            freeaccs = json.load(file)

            if "free" not in freeaccs: freeaccs["free"] = [] 

            freeaccs["free"].append({
                "name": name,
                "selected": selected
            })

        with open(get_home() + "/accounts.json", "w") as file: json.dump(freeaccs, file, indent= 4)

    @staticmethod
    def delete(name: str) -> None:

        check_noxlauncher_filesystem()

        with open(get_home() + "/accounts.json", "r") as file:

            freeaccs = json.load(file)

            if "free" not in freeaccs: return

            for acc in freeaccs["free"]:
                if acc["name"] == name:
                    freeaccs["free"].remove(acc)
                    break

        with open(get_home() + "/accounts.json", "w") as file: json.dump(freeaccs, file, indent= 4)

    @staticmethod
    def select(name: str) -> None:

        check_noxlauncher_filesystem()

        with open(get_home() + "/accounts.json", "r") as file:

            freeaccs = json.load(file)

            if "free" not in freeaccs: return

            for acc in freeaccs["free"]:
                if acc["name"] == name:
                    acc["selected"] = True
                    break

        with open(get_home() + "/accounts.json", "w") as file: json.dump(freeaccs, file, indent= 4)
    