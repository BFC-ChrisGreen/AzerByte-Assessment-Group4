import sqlite3
from pathlib import Path
from flask import Flask, jsonify, request

app = Flask(__name__)
DATABASE_PATH = Path(__file__).resolve().parents[1] / "database" / "azerbyte.db"
ALLOWED_CLASSES = {"Warrior", "Mage", "Rogue", "Priest", "Ranger"}
ALLOWED_REALMS = {"Emberfall", "Ironhollow", "Moonspire", "Stormwatch"}
REQUIRED_FIELDS = ("name", "character_class", "level", "realm")

def get_database_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection
def validate_character(data):
    if not isinstance(data, dict):
        return "The request body must contain JSON."

    missing_fields = [field for field in REQUIRED_FIELDS if field not in data]
    if missing_fields:
        return f"Missing fields: {', '.join(missing_fields)}"

    if not isinstance(data["name"], str) or not 2 <= len(data["name"].strip()) <= 30:
        return "Name must contain between 2 and 30 characters."

    if data["character_class"] not in ALLOWED_CLASSES:
        return "Character class is not allowed."

    if type(data["level"]) is not int or not 1 <= data["level"] <= 60:
        return "Level must be a whole number between 1 and 60."

    if data["realm"] not in ALLOWED_REALMS:
        return "Realm is not allowed."

    return None


@app.get("/health")
def health():
    return jsonify({"service": "azerbyte", "status": "online"}), 200
@app.get("/characters")
def get_characters():
    with get_database_connection() as connection:
        rows = connection.execute(
            """
            SELECT character_id, name, character_class, level, realm
            FROM characters
            ORDER BY character_id
            """
        ).fetchall()

    return jsonify([dict(row) for row in rows]), 200
@app.get("/characters/<int:character_id>")
def get_character(character_id):
    with get_database_connection() as connection:
        row = connection.execute(
            """
            SELECT character_id, name, character_class, level, realm
            FROM characters
            WHERE character_id = ?
            """,
            (character_id,),
        ).fetchone()

    if row is None:
        return jsonify({"error": "Character not found"}), 404

    return jsonify(dict(row)), 200

    return jsonify({"error": "Character not found"}), 404

@app.post("/characters")
def create_character():
    data = request.get_json(silent=True)
    validation_error = validate_character(data)

    if validation_error:
        return jsonify({"error": validation_error}), 400

    with get_database_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO characters (name, character_class, level, realm)
            VALUES (?, ?, ?, ?)
            """,
            (
                data["name"].strip(),
                data["character_class"],
                data["level"],
                data["realm"],
            ),
        )
        new_id = cursor.lastrowid
        row = connection.execute(
            """
            SELECT character_id, name, character_class, level, realm
            FROM characters
            WHERE character_id = ?
            """,
            (new_id,),
        ).fetchone()

    return jsonify(dict(row)), 201

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
