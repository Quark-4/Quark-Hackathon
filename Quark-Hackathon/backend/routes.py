from flask import jsonify, request
from ai_service import detect_age
from safe_browsing import check_url
from datetime import datetime

# Latest website status
latest_status = {
    "website": "Waiting...",
    "status": "Waiting..."
}

# Recent activity
activity_log = []

# AI Protection Status
protection_enabled = True


def register_routes(app):

    # -----------------------------
    # AI Age Detection
    # -----------------------------
    @app.route("/detect-age", methods=["GET"])
    def age_detection():

        global protection_enabled

        result = detect_age()

        if result["status"] == "success":

            if result["age"] < 18:
                protection_enabled = True
            else:
                protection_enabled = False

            result["protection"] = protection_enabled

        return jsonify(result)

    # -----------------------------
    # Safe Browsing
    # -----------------------------
    @app.route("/check-url", methods=["POST"])
    def check_url_route():

        global latest_status
        global activity_log
        global protection_enabled

        data = request.get_json()

        url = data["url"]

        print("\nWebsite:", url)

        # If protection is OFF, don't block websites
        if protection_enabled:

            result = check_url(url)

        else:

            result = {
                "safe": True,
                "message": "Protection Disabled (Adult)"
            }

        # Update latest website
        latest_status["website"] = url

        if result["safe"]:
            latest_status["status"] = "🟢 Safe"
        else:
            latest_status["status"] = "🚫 Blocked"

        # Save activity
        activity_log.insert(0, {
            "time": datetime.now().strftime("%H:%M:%S"),
            "website": url,
            "status": latest_status["status"]
        })

        # Keep last 10 websites
        activity_log = activity_log[:10]

        return jsonify(result)

    # -----------------------------
    # Current Website Status
    # -----------------------------
    @app.route("/website-status", methods=["GET"])
    def website_status():

        return jsonify(latest_status)

    # -----------------------------
    # Activity History
    # -----------------------------
    @app.route("/activity-log", methods=["GET"])
    def get_activity_log():

        return jsonify(activity_log)

    # -----------------------------
    # Protection Status
    # -----------------------------
    @app.route("/protection-status", methods=["GET"])
    def protection_status():

        return jsonify({
            "enabled": protection_enabled
        })