import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).with_name("azerbyte.db")

def setup_database():
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS characters (
                character_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL CHECK(length(name) BETWEEN 2 AND 30),
                character_class TEXT NOT NULL
                    CHECK(character_class IN ('Warrior', 'Mage', 'Rogue', 'Priest', 'Ranger')),
                level INTEGER NOT NULL CHECK(level BETWEEN 1 AND 60),
                realm TEXT NOT NULL
                    CHECK(realm IN ('Emberfall', 'Ironhollow', 'Moonspire', 'Stormwatch'))
            )
            """
        )

        connection.executemany(
            """
            INSERT OR IGNORE INTO characters
                (character_id, name, character_class, level, realm)
            VALUES (?, ?, ?, ?, ?)
            """,
            [
                (1, "Aelwyn", "Mage", 24, "Emberfall"),
                (2, "Bromm", "Warrior", 18, "Ironhollow"),
            ],
        )

    print(f"Database ready: {DATABASE_PATH}")

if __name__ == "__main__":
    setup_database()