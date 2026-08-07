from flask import jsonify, request
from ai_service import detect_age
from safe_browsing import check_url
from datetime import datetime


latest_status = {
    "website": "Waiting...",
    "status": "Waiting..."
}

activity_log = []

# Always ON for demo
protection_enabled = True


def register_routes(app):

    # -----------------------------
    # AI Age Detection + Screen Monitoring
    # -----------------------------
    @app.route("/detect-age", methods=["GET"])
    def age_detection():

        result = detect_age()

        if result["status"] == "success":
            result["protection"] = protection_enabled

            # NEW: Child + NSFW detected
            if result.get("person") == "child" and result.get("nsfw"):

                result["blocked"] = True
                result["message"] = "Adult content blocked for minor"

            else:
                result["blocked"] = False

        return jsonify(result)


    # -----------------------------
    # Safe Browsing + AI Protection
    # -----------------------------
    @app.route("/check-url", methods=["POST"])
    def check_url_route():

        global latest_status
        global activity_log

        data = request.get_json()

        url = data["url"]

        print("\nWebsite:", url)

        # URL checking
        result = check_url(url)


        # Check current viewer
        ai_result = detect_age()


        # NEW: Combine URL + AI decision
        if (
            ai_result.get("status") == "success"
            and ai_result.get("person") == "child"
            and ai_result.get("nsfw") == True
        ):
            result["safe"] = False
            result["reason"] = "Adult content detected while minor is watching"


        latest_status["website"] = url


        if result["safe"]:
            latest_status["status"] = "🟢 Safe"
        else:
            latest_status["status"] = "🚫 Blocked"


        activity_log.insert(0, {
            "time": datetime.now().strftime("%H:%M:%S"),
            "website": url,
            "status": latest_status["status"]
        })

        activity_log = activity_log[:10]


        result["ai"] = ai_result

        return jsonify(result)


    # -----------------------------
    # Website Status
    # -----------------------------
    @app.route("/website-status", methods=["GET"])
    def website_status():

        return jsonify(latest_status)


    # -----------------------------
    # Activity Log
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