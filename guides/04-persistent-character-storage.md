# Guide 4: Persistent Character Storage

Guide 3 gave Azerbyte working character endpoints, but the data is still stored in a Python list. That list is recreated whenever the server starts and cannot store changes permanently.

In this guide, your group will replace the list with SQLite. The existing client and endpoint addresses will stay the same.

By the end of this guide:

- SQLite will store the character records;
- the database can be recreated from setup code;
- the existing read endpoints will use the database; and
- character data will remain available after the Flask server restarts.

## 1. Check the Starting Point

Before anyone changes a file, every member runs:

```bash
git status
git pull
```

The working tree should be clean.

Open two terminals in Visual Studio Code. Activate the virtual environment in both:

```bash
.venv\Scripts\activate
```

Start the server in the first terminal:

```bash
python server/server.py
```

Run the Guide 3 client in the second terminal:

```bash
python client/client.py
```

Check that:

- the service reports `online`;
- both starter characters are displayed;
- character ID `1` is returned; and
- character ID `999` produces `Character not found`.

Stop the server using **Ctrl+C** once these checks pass.

Do not begin the database work until the Guide 3 version still works.

### Rotate the Group Roles

Agree who will take the lead on:

- database setup;
- server changes;
- testing and evidence; and
- review and documentation, where there is a fourth member.

Each member updates the **Proposed Project Role** section in their own file inside:

```text
team-practice/members
```

## 2. Check That Database Files Are Ignored

The database file will be created separately on each computer. It must not be committed because different group members would keep overwriting one another's local data.

Open `.gitignore` in the main repository folder. Make sure it contains:

```text
*.db
*.sqlite
*.sqlite3
```

If these lines are missing, one member adds them, commits and pushes the change. Everyone else then pulls.

Suggested commit message:

```text
Ignore local SQLite database files
```

The Python setup code will be committed. The database file created by that code will remain local.

## 3. Create the Database Setup Script

The database builder creates:

```text
database/setup_database.py
```

Add:

```python
import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).with_name("azerbyte.db")
```

`sqlite3` is included with Python. `Path` creates a reliable path to the database folder, regardless of which group member runs the program.

Next, add:

```python
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
```

This creates the `characters` table and applies the data rules agreed in Guide 3.

Still inside `setup_database()`, directly below `connection.execute(...)`, add:

```python
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
```

`INSERT OR IGNORE` adds the starter records if they are missing. Running the setup again will not duplicate or overwrite them.

Finally, add:

```python
if __name__ == "__main__":
    setup_database()
```

Save the file.

## 4. Create the Local Database

Run:

```bash
python database/setup_database.py
```

The output should begin with:

```text
Database ready:
```

The file below should now appear in Visual Studio Code:

```text
database/azerbyte.db
```

Run the setup command a second time. It should finish without an error.

Now run:

```bash
git status
git check-ignore database/azerbyte.db
```

`git status` should show `setup_database.py`, but it should not list `azerbyte.db`. The second command should print the database path, confirming that Git is ignoring it.

### Checkpoint

The database builder commits and pushes the setup code. Do not add the database file manually.

Suggested commit message:

```text
Add Azerbyte database setup
```

Every other member now:

1. Pulls the commit.
2. Runs `python database/setup_database.py` locally.
3. Confirms that their own `database/azerbyte.db` file appears.

## 5. Connect the Server to SQLite

Open:

```text
server/server.py
```

At the top of the file, add these imports above the Flask import:

```python
import sqlite3
from pathlib import Path
```

Keep the existing Flask import used by Guide 3:

```python
from flask import Flask, jsonify
```

Directly below:

```python
app = Flask(__name__)
```

add:

```python
DATABASE_PATH = Path(__file__).resolve().parents[1] / "database" / "azerbyte.db"


def get_database_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection
```

The row factory allows each database result to be converted into a dictionary before Flask turns it into JSON.

Delete the temporary `characters = [...]` list from Guide 3. The database now owns that data.

Do not change the `/health` endpoint.

## 6. Read All Characters from SQLite

Find the existing `get_characters()` function and replace it with:

```python
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
```

The endpoint address and response format have not changed. Only the source of the data has changed.

## 7. Read One Character from SQLite

Replace the existing `get_character()` function with:

```python
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
```

The `?` is a parameter placeholder. The value is supplied separately rather than being joined into the SQL string.

### Explain Back

Before testing, every member should be able to explain:

- why the client has not needed to change;
- why the SQL uses `?` rather than placing the ID directly into the query; and
- why `dict(row)` is needed before returning the result as JSON.

## 8. Test the Persistent Version

Start the server:

```bash
python server/server.py
```

In the second terminal, run:

```bash
python client/client.py
```

The output should still show Aelwyn, Bromm, character ID `1` and the missing-character response.

Also visit:

```text
http://127.0.0.1:5000/characters
```

Stop the server using **Ctrl+C**, restart it and run the client again.

The same records should still be returned because they are now read from `azerbyte.db`.

### Checkpoint

The server builder commits and pushes the completed database connection. Everyone else pulls, runs their local setup script and tests the server before continuing.

Suggested commit message:

```text
Read character data from SQLite
```

## 9. Record the Evidence

Open:

```text
evidence/test-record.md
```

Record the actual result of each test:

| Test | Expected result |
|---|---|
| Run the database setup twice | Both runs complete and only two starter records exist |
| Request `/characters` | Status `200` and two database records |
| Request `/characters/1` | Status `200` and Aelwyn's record |
| Request `/characters/999` | Status `404` and `Character not found` |
| Restart Flask and request the characters again | The same records are still returned |
| Run setup on another group member's clone | Their local database is created successfully |

If a test fails, record what happened, fix the problem and record the retest.

## 10. Record the Decision

Open:

```text
docs/technical-decisions.md
```

Complete or update the row for persistent storage. Briefly record:

- why the group selected SQLite;
- why the database file is excluded from Git; and
- how the setup script allows each member to create the same structure locally.

The tester or documentation lead commits and pushes the evidence and decision. Everyone else then pulls.

Suggested commit message:

```text
Record SQLite tests and decision
```

## Final Check

Before completing Guide 4, make sure that:

- Guide 3's `/health` and read endpoints still work;
- `server.py` no longer contains the temporary character list;
- the API reads characters from SQLite;
- `database/setup_database.py` can be run more than once;
- `database/azerbyte.db` is ignored by Git;
- every member can create their own local database;
- the test record contains the SQLite results;
- the technical decision is recorded;
- contributions from different members appear in the Git history; and
- every member has pulled the completed version.

The prototype now has persistent read-only data. Guide 5 will add the ability to create and update characters.

## Common Problems

### `no such table: characters`

The database file exists, but the setup script has not created the table. Stop the server and run:

```bash
python database/setup_database.py
```

Then restart the server.

### `unable to open database file`

Check that the repository still contains the `database` folder and that `DATABASE_PATH` is copied exactly.

### The client still shows the old list after changing the database

Check that the temporary `characters = [...]` list has been removed and both `GET` endpoints use `get_database_connection()`.

### The database appears in `git status`

Do not commit it. Check that `.gitignore` contains `*.db`, save the file and run `git status` again.

### A group member pulls the code but has no database

This is expected. Database binaries are not shared. That member must run:

```bash
python database/setup_database.py
```

### `database is locked`

Stop the Flask server and close any program that has opened `azerbyte.db`. Run the setup or test again before restarting Flask.
