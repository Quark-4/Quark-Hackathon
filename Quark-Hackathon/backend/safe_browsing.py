import os
import requests
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Read API Key
API_KEY = os.getenv("SAFE_BROWSING_API_KEY")
print("Loaded API Key:", API_KEY)


def check_url(url):

    # Ignore Chrome internal pages
    if url.startswith("chrome://"):
        return {
            "safe": True,
            "message": "Chrome Internal Page"
        }

    endpoint = (
        f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={API_KEY}"
    )

    payload = {
        "client": {
            "clientId": "ai-guardian",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": [
                "MALWARE",
                "SOCIAL_ENGINEERING",
                "UNWANTED_SOFTWARE",
                "POTENTIALLY_HARMFUL_APPLICATION"
            ],
            "platformTypes": [
                "ANY_PLATFORM"
            ],
            "threatEntryTypes": [
                "URL"
            ],
            "threatEntries": [
                {
                    "url": url
                }
            ]
        }
    }

    response = requests.post(endpoint, json=payload)

    # Google API Error
    if response.status_code != 200:
        print("Status Code:", response.status_code)
        print("Response:", response.text)

        return {
            "safe": False,
            "message": "Google API Error"
        }

    data = response.json()

    print("Google Response:", data)

    # Website is unsafe
    if data.get("matches"):
        return {
            "safe": False,
            "message": "Unsafe Website"
        }

    # Website is safe
    return {
        "safe": True,
        "message": "Safe Website"
    }