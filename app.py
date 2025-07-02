from flask import Flask, jsonify, request
import json

def localize_field(field_dict, lang):
    return field_dict.get(lang) or field_dict.get("en")  # fallback to English

app = Flask(__name__)

# Load JSON data
with open("wilayas.json", encoding="utf-8") as f:
    wilayas = json.load(f)

with open("teams.json", encoding="utf-8") as f:
    teams = json.load(f)

with open("meals.json", encoding="utf-8") as f:
    meals = json.load(f)

@app.route("/")
def home():
    return "Welcome to the Fenek API"

@app.route("/meals", methods=["GET"])
def get_meals():
    lang = request.args.get("lang", "en")
    localized_meals = []

    for meal in meals:
        localized_meals.append({
            "id": meal["id"],
            "name": localize_field(meal["name"], lang),
            "region": meal["region"],
            "description": localize_field(meal["description"], lang),
            "ingredients": meal["ingredients"]
        })

    return jsonify(localized_meals)

@app.route("/meals/<int:meal_id>", methods=["GET"])
def get_meal_by_id(meal_id):
    lang = request.args.get("lang", "en")
    meal = next((m for m in meals if m["id"] == meal_id), None)

    if not meal:
        return jsonify({"error": "Meal not found"}), 404

    localized_meal = {
        "id": meal["id"],
        "name": localize_field(meal["name"], lang),
        "region": meal["region"],
        "description": localize_field(meal["description"], lang),
        "ingredients": meal["ingredients"]
    }

    return jsonify(localized_meal)

@app.route("/wilayas", methods=["GET"])
def get_wilayas():
    lang = request.args.get("lang", "en")
    localized = []
    for w in wilayas:
        localized.append({
            "code": w["code"],
            "name": localize_field(w["name"], lang),
            "capital": localize_field(w["capital"], lang)
        })
    return jsonify(localized)

@app.route("/wilayas/<int:code>", methods=["GET"])
def get_wilaya_by_code(code):
    lang = request.args.get("lang", "en")
    w = next((w for w in wilayas if w["code"] == code), None)
    if not w:
        return jsonify({"error": "Wilaya not found"}), 404
    return jsonify({
        "code": w["code"],
        "name": localize_field(w["name"], lang),
        "capital": localize_field(w["capital"], lang)
    })

@app.route("/teams", methods=["GET"])
def get_teams():
    lang = request.args.get("lang", "en")
    localized = []
    for t in teams:
        localized.append({
            "id": t["id"],
            "name": localize_field(t["name"], lang),
            "city": localize_field(t["city"], lang),
            "stadium": localize_field(t["stadium"], lang)
        })
    return jsonify(localized)

@app.route("/teams/<int:team_id>", methods=["GET"])
def get_team_by_id(team_id):
    lang = request.args.get("lang", "en")
    t = next((t for t in teams if t["id"] == team_id), None)
    if not t:
        return jsonify({"error": "Team not found"}), 404
    return jsonify({
        "id": t["id"],
        "name": localize_field(t["name"], lang),
        "city": localize_field(t["city"], lang),
        "stadium": localize_field(t["stadium"], lang)
    })


if __name__ == "__main__":
    app.run(debug=True)