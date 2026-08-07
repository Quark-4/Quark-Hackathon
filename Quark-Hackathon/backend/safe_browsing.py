import os
import requests
from dotenv import load_dotenv
from policy_engine import policy_check

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
            "message": "Chrome Internal Page",
            "reason": "",
            "category": "Internal",
            "threat": "None"
        }

    # ----------------------------
    # AI Guardian Policy Engine
    # ----------------------------
    policy = policy_check(url)

    if policy["blocked"]:
        return {
            "safe": False,
            "message": "Blocked by AI Guardian",
            "reason": policy["reason"],
            "category": policy["category"],
            "threat": "Policy Engine"
        }

    # ----------------------------
    # Google Safe Browsing
    # ----------------------------
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

    if response.status_code != 200:

        print("Status Code:", response.status_code)
        print("Response:", response.text)

        return {
            "safe": False,
            "message": "Google API Error",
            "reason": "API Error",
            "category": "Unknown",
            "threat": "Google Safe Browsing"
        }

    data = response.json()

    print("Google Response:", data)

    if data.get("matches"):

        return {
            "safe": False,
            "message": "Unsafe Website",
            "reason": "Google Safe Browsing",
            "category": "Cyber Threat",
            "threat": data["matches"][0]["threatType"]
        }

    return {
        "safe": True,
        "message": "Safe Website",
        "reason": "",
        "category": "General",
        "threat": "None"
    }