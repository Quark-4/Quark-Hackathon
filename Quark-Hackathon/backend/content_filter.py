from urllib.parse import urlparse


def analyze_content(url):
    """
    AI Guardian Content Filter

    Returns:
        blocked
        reason
        category
        threat
    """

    parsed = urlparse(url)

    hostname = parsed.hostname or ""

    hostname = hostname.lower()

    # Browser pages
    if hostname == "":
        return {
            "blocked": False,
            "reason": "",
            "category": "Internal",
            "threat": "None"
        }

    # Default (allow)
    return {
        "blocked": False,
        "reason": "",
        "category": "General",
        "threat": "Low"
    }