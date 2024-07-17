import requests
from functools import cache

@cache
def check_internet() -> bool:
    try:
        requests.get("https://google.com", timeout= 30)
        return True
    except:
        return False
