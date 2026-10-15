from flask import Flask, jsonify

app = Flask(__name__)

characters = [
    {
        "character_id": 1,
        "name": "ProfGreen",
        "character_class": "Warrior",
        "level": 1,
        "realm": "Stormwatch",
    },
    {
        "character_id": 2,
        "name": "BigBoyBailey",
        "character_class": "Mage",
        "level": 60,
        "realm": "Orgrimmar",
    },
    {
        "character_id": 3,
        "name": "Willson",
        "character_class": "Ranger",
        "level": 60,
        "realm": "Winterspring",
    },
    {
        "character_id": 4,
        "name": "SneakyOday",
        "character_class": "Rogue",
        "level": 60,
        "realm": "Hinterlands",
    },
    {
        "character_id": 5,
        "name": "KeithTheConspirator",
        "character_class": "Priest",
        "level": 47,
        "realm": "Stormwatch",
    },
]
@app.get("/health")
def health():
    return jsonify({"service": "azerbyte", "status": "online"}), 200
@app.get("/characters")
def get_characters():
    return jsonify(characters), 200
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

