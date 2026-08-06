from flask import jsonify, request
from ai_service import detect_age
from safe_browsing import check_url


def register_routes(app):

    @app.route("/detect-age", methods=["GET"])
    def age_detection():
        result = detect_age()
        return jsonify(result)

    @app.route("/check-url", methods=["POST"])
    def check_url_route():

        data = request.get_json()

        url = data["url"]

        print("\nWebsite:", url)

        result = check_url(url)

        return jsonify(result)