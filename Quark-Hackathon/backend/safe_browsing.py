import requests

API_KEY = ""

def check_url(url):

    if API_KEY == "":
        return {
            "safe": True,
            "message": "API Key not added"
        }