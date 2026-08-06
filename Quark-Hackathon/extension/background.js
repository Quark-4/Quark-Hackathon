chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {

    if (changeInfo.status === "complete" && tab.url) {

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

            console.log("Backend:", data);

        }

        catch(error){

            console.log(error);

        }

    }

});