import sqlite3
from pathlib import Path
from flask import Flask, jsonify

app = Flask(__name__)
DATABASE_PATH = Path(__file__).resolve().parents[1] / "database" / "azerbyte.db"


def get_database_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection



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
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
