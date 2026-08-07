chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {

    // Wait until page is fully loaded
    if (changeInfo.status !== "complete" || !tab.url) {
        return;
    }

    // Ignore Chrome internal pages
    if (
        tab.url.startsWith("chrome://") ||
        tab.url.startsWith("chrome-extension://")
    ) {
        return;
    }

    console.log("Website:", tab.url);

    try {

        const response = await fetch("http://127.0.0.1:5000/check-url", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                url: tab.url
            })
        });


        const data = await response.json();


        console.log(
            "Backend Response:",
            JSON.stringify(data)
        );


        // Block if:
        // 1. Website is unsafe
        // OR
        // 2. Child is watching NSFW content

        if (
            !data.safe ||
            (
                data.ai &&
                data.ai.person === "child" &&
                data.ai.nsfw === true
            )
        ) {

            console.log("BLOCKING CONTENT");

            chrome.tabs.update(tabId, {

                url: chrome.runtime.getURL("blocked.html")

            });

        }


    } catch (error) {

        console.error(
            "Backend connection error:",
            error
        );

    }

});