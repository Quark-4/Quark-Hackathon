chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {

    if (changeInfo.status !== "complete" || !tab.url) {
        return;
    }
// Ignore Chrome internal pages and extension pages
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

        console.log("Backend Response:", JSON.stringify(data));

        // If website is unsafe, redirect to blocked page
        if (!data.safe) {

            chrome.tabs.update(tabId, {
                url: chrome.runtime.getURL("blocked.html")
            });

        }

    } catch (error) {
        console.error(error);
    }

});