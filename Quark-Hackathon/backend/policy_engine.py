from urllib.parse import urlparse, parse_qs

# Add the search terms that your parental-control policy should block.
BLOCKED_KEYWORDS = [
    # Populate this list with the terms appropriate for your project.
]


def policy_check(url):

    url = url.lower()

    parsed = urlparse(url)

    query = parse_qs(parsed.query)

    search = ""

    if "q" in query:
        search = query["q"][0].lower()

    # Check search keywords
    for word in BLOCKED_KEYWORDS:

        if word in search:

            return {
                "blocked": True,
                "reason": "Blocked Search",
                "category": "Restricted Search"
            }

    # If nothing matched
    return {
        "blocked": False,
        "reason": "",
        "category": ""
    }