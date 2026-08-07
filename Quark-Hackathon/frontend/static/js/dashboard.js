// ===============================
// AI Guardian Dashboard
// ===============================

// ---------- LIVE CLOCK ----------

function updateClock() {

    const now = new Date();

    document.getElementById("clock").innerText =
        now.toLocaleTimeString();

}

setInterval(updateClock, 1000);
updateClock();


// ---------- AGE DETECTION ----------

async function updateAge() {

    try {

        const response = await fetch("http://127.0.0.1:5000/detect-age");

        const data = await response.json();

        console.log("Age:", data);

        if (data.status === "success") {

            document.getElementById("camera").innerText = "🟢 Connected";

            document.getElementById("age").innerText = data.age;

            document.getElementById("person").innerText = data.person;

            document.getElementById("confidence").innerText =
                (data.confidence * 100).toFixed(1) + "%";

            // Protection Status
            if (data.protection) {

                document.getElementById("protection").innerHTML =
                    "🟢 Enabled";

            } else {

                document.getElementById("protection").innerHTML =
                    "⚪ Disabled";

            }

        } else {

            document.getElementById("camera").innerText =
                "🔴 Camera Error";

        }

    }

    catch (error) {

        console.log(error);

        document.getElementById("camera").innerText =
            "🔴 Backend Offline";

    }

}

// First scan
updateAge();

// Scan every 5 minutes
setInterval(updateAge, 5 * 60 * 1000);


// ---------- WEBSITE ----------

async function updateWebsite() {

    try {

        const response =
            await fetch("http://127.0.0.1:5000/website-status");

        const data = await response.json();

        document.getElementById("website").innerText =
            data.website;

        document.getElementById("websiteStatus").innerHTML =
            data.status;

    }

    catch (error) {

        console.log(error);

    }

}

updateWebsite();

setInterval(updateWebsite, 2000);


// ---------- ACTIVITY ----------

async function updateActivity() {

    try {

        const response =
            await fetch("http://127.0.0.1:5000/activity-log");

        const data = await response.json();

        const tbody =
            document.querySelector("#activityTable tbody");

        tbody.innerHTML = "";

        data.forEach(item => {

            let website;

            try {

                website =
                    new URL(item.website).hostname;

            }

            catch {

                website = item.website;

            }

            tbody.innerHTML += `

            <tr>

                <td>${item.time}</td>

                <td title="${item.website}">
                    ${website}
                </td>

                <td>${item.status}</td>

            </tr>

            `;

        });

    }

    catch (error) {

        console.log(error);

    }

}

updateActivity();

setInterval(updateActivity, 2000);