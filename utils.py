import requests

def has_internet() -> bool:

    try:
        return requests.get("https://google.com", timeout= 20).ok
    except:
        return False