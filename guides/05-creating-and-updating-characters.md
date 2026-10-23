# Guide 5: Creating and Updating Characters

Azerbyte can now read persistent character data from SQLite. This guide adds the remaining actions needed for the basic version: creating a character, updating a character and rejecting data that does not follow the agreed rules.

By the end of this guide:

- the API will accept `POST` and `PUT` requests;
- validation will protect the database from unsuitable data;
- reusable client functions will handle all HTTP communication;
- the command-line client will provide a simple menu; and
- created and updated records will remain after the server restarts.

Completing this guide gives the group the basic technical version of the Azerbyte prototype. It is the starting point for testing, improvement and extension, not the finished assessment.

## 1. Check the Starting Point

Every member runs:

```bash
git status
git pull
.venv\Scripts\activate
python database/setup_database.py
```

Open two terminals and activate the virtual environment in both.

Start the server in the first terminal:

```bash
python server/server.py
```

Run the client in the second terminal:

```bash
python client/client.py
```

Do not continue until the Guide 4 client can read both starter characters from SQLite.

### Rotate the Group Roles

Agree who will take the lead on:

- server validation and endpoints;
- reusable client communication;
- command-line client;
- testing and documentation, where there is a fourth member.

Each member updates the **Proposed Project Role** section in their own file inside:

```text
team-practice/members
```

## 2. Understand the New Requests

The prototype already uses:

| Method and endpoint | Purpose | Successful status |
|---|---|---:|
| `GET /characters` | Return every character | `200` |
| `GET /characters/<character_id>` | Return one character | `200` |

This guide adds:

| Method and endpoint | Purpose | Successful status |
|---|---|---:|
| `POST /characters` | Create a character | `201` |
| `PUT /characters/<character_id>` | Replace an existing character's editable data | `200` |

Both new requests will send JSON using the existing field names:

```json
{
  "name": "Cinder",
  "character_class": "Rogue",
  "level": 12,
  "realm": "Moonspire"
}
```

The client does not send `character_id` when creating a record. SQLite generates it.

## 3. Add Server-Side Validation

Open:

```text
server/server.py
```

Update the Flask import so it includes `request`:

```python
from flask import Flask, jsonify, request
```

Directly below `DATABASE_PATH`, add:

```python
ALLOWED_CLASSES = {"Warrior", "Mage", "Rogue", "Priest", "Ranger"}
ALLOWED_REALMS = {"Emberfall", "Ironhollow", "Moonspire", "Stormwatch"}
REQUIRED_FIELDS = ("name", "character_class", "level", "realm")
```

Below `get_database_connection()`, add:

```python
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
```

The server must validate every request. A different client could bypass checks placed only in the command-line program.

### Checkpoint

Explain within the group:

- why validation belongs on the server;
- why the allowed values match `docs/data-rules.md`; and
- why returning an error is safer than trying to guess what invalid data meant.

## 4. Create a Character

Add this route above the final `if __name__ == "__main__":` block:

```python
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
```

A successful create returns the stored record, including the ID generated by SQLite.

## 5. Update a Character

Below the create route, add:

```python
@app.put("/characters/<int:character_id>")
def update_character(character_id):
    data = request.get_json(silent=True)
    validation_error = validate_character(data)

    if validation_error:
        return jsonify({"error": validation_error}), 400

    with get_database_connection() as connection:
        existing = connection.execute(
            "SELECT character_id FROM characters WHERE character_id = ?",
            (character_id,),
        ).fetchone()

        if existing is None:
            return jsonify({"error": "Character not found"}), 404

        connection.execute(
            """
            UPDATE characters
            SET name = ?, character_class = ?, level = ?, realm = ?
            WHERE character_id = ?
            """,
            (
                data["name"].strip(),
                data["character_class"],
                data["level"],
                data["realm"],
                character_id,
            ),
        )
        row = connection.execute(
            """
            SELECT character_id, name, character_class, level, realm
            FROM characters
            WHERE character_id = ?
            """,
            (character_id,),
        ).fetchone()

    return jsonify(dict(row)), 200
```

The endpoint first checks that the character exists. It then updates the editable values and returns the stored record.

### Checkpoint

The server builder checks the file for indentation and syntax errors, starts Flask and confirms that the existing `GET` endpoints still work.

The server builder then commits and pushes. Everyone else pulls before changing the client.

Suggested commit message:

```text
Add character create and update endpoints
```

## 6. Separate the Client Communication

The current `client.py` sends requests and displays the results. Separating these responsibilities will allow the command-line client and a later Tkinter client to reuse the same HTTP functions.

Create:

```text
client/api_client.py
```

Add:

```python
import requests
from requests import RequestException


SERVICE_URL = "http://127.0.0.1:5000"
```

Next, add:

```python
def send_request(method, endpoint, data=None):
    try:
        response = requests.request(
            method,
            f"{SERVICE_URL}{endpoint}",
            json=data,
            timeout=5,
        )

        try:
            response_data = response.json()
        except ValueError:
            response_data = {}

        if not response.ok:
            error = response_data.get(
                "error",
                f"Request failed with status {response.status_code}.",
            )
            return None, error

        return response_data, None
    except RequestException:
        return None, "The Azerbyte service could not be reached."
```

This function returns two values:

```text
successful request → data, None
unsuccessful request → None, error message
```

Finally, add:

```python
def get_characters():
    return send_request("GET", "/characters")


def get_character(character_id):
    return send_request("GET", f"/characters/{character_id}")


def create_character(character):
    return send_request("POST", "/characters", character)


def update_character(character_id, character):
    return send_request("PUT", f"/characters/{character_id}", character)
```

### Explain Back

Before continuing, each member should be able to explain:

- what `method`, `endpoint` and `data` represent;
- why all requests use the same `SERVICE_URL`; and
- why returning an error message is more useful than allowing the program to crash.

## 7. Build the Basic Command-Line Client

Open:

```text
client/client.py
```

Replace its current contents with the following. The HTTP code has moved into `api_client.py`; this file now handles input and output.

```python
from api_client import (
    create_character,
    get_character,
    get_characters,
    update_character,
)


def display_character(character):
    print(
        f"{character['character_id']}: {character['name']} - "
        f"Level {character['level']} {character['character_class']} "
        f"on {character['realm']}"
    )


def read_character_details():
    name = input("Name: ").strip()
    character_class = input(
        "Class (Warrior, Mage, Rogue, Priest or Ranger): "
    ).strip()
    realm = input(
        "Realm (Emberfall, Ironhollow, Moonspire or Stormwatch): "
    ).strip()

    try:
        level = int(input("Level: "))
    except ValueError:
        print("Level must be a whole number.")
        return None

    return {
        "name": name,
        "character_class": character_class,
        "level": level,
        "realm": realm,
    }


def show_all_characters():
    characters, error = get_characters()
    if error:
        print(error)
        return

    for character in characters:
        display_character(character)


def show_one_character():
    try:
        character_id = int(input("Character ID: "))
    except ValueError:
        print("Character ID must be a whole number.")
        return

    character, error = get_character(character_id)
    if error:
        print(error)
        return

    display_character(character)


def add_character():
    character_data = read_character_details()
    if character_data is None:
        return

    character, error = create_character(character_data)
    if error:
        print(error)
        return

    print("Character created:")
    display_character(character)


def change_character():
    try:
        character_id = int(input("Character ID to update: "))
    except ValueError:
        print("Character ID must be a whole number.")
        return

    character_data = read_character_details()
    if character_data is None:
        return

    character, error = update_character(character_id, character_data)
    if error:
        print(error)
        return

    print("Character updated:")
    display_character(character)


def main():
    while True:
        print("\nAzerbyte Character Manager")
        print("1. View all characters")
        print("2. Find a character")
        print("3. Create a character")
        print("4. Update a character")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            show_all_characters()
        elif choice == "2":
            show_one_character()
        elif choice == "3":
            add_character()
        elif choice == "4":
            change_character()
        elif choice == "5":
            print("Goodbye.")
            break
        else:
            print("Choose an option from 1 to 5.")


if __name__ == "__main__":
    main()
```

Save the file.

### Checkpoint

The client builder commits and pushes `api_client.py` and the new `client.py`. Everyone else pulls and runs the menu.

Suggested commit message:

```text
Add Azerbyte character management client
```

## 8. Complete the Required Tests

Keep Flask running in the first terminal:

```bash
python server/server.py
```

Run the client in the second terminal:

```bash
python client/client.py
```

Complete these tests in order.

### Test 1: View and Find

1. Select option `1` and check that Aelwyn and Bromm appear.
2. Select option `2` and find character ID `1`.
3. Select option `2` again and request ID `999`.

The final request should display `Character not found` without crashing.

### Test 2: Create a Valid Character

Select option `3` and enter:

```text
Name: Cinder
Class: Rogue
Realm: Moonspire
Level: 12
```

The client should display `Character created` and the new database ID.

### Test 3: Reject Invalid Data

Select option `3` again. Use the same values but enter level `99`.

The API should reject it with:

```text
Level must be a whole number between 1 and 60.
```

### Test 4: Update the Created Character

Select option `4`. Use Cinder's new ID and enter the same details with level `13`.

The client should display the updated record.

### Test 5: Update a Missing Character

Select option `4` again and use ID `999` with otherwise valid data.

The client should display:

```text
Character not found
```

### Test 6: Confirm Persistence

1. Exit the client.
2. Stop Flask using **Ctrl+C**.
3. Restart Flask.
4. Run the client again.
5. Find Cinder using the ID returned earlier.

Cinder should still exist at level `13`.

## 9. Record the Test Evidence

Open:

```text
evidence/test-record.md
```

Record the actual results:

| Test | Expected result |
|---|---|
| View all characters | Every stored character is displayed |
| Find existing character | Status `200` and the correct character |
| Find missing character | Status `404` and a clear error |
| Create valid character | Status `201` and a generated ID |
| Create level `99` | Status `400` and a validation error |
| Update existing character | Status `200` and the changed record |
| Update ID `999` | Status `404` and a clear error |
| Restart Flask and find the new character | Created and updated values remain |
| Stop Flask and run the client | A clear unavailable-service message |

Record failures and retests rather than changing the evidence to what should have happened.

## 10. Update the Documentation

Open:

```text
docs/technical-decisions.md
```

Add short entries explaining:

- why validation is completed by the API;
- why the client communication was moved into `api_client.py`; and
- why the API uses different status codes for created, invalid and missing resources.

Check that:

```text
docs/data-rules.md
```

still matches the classes, realms, name length and level range used by the API.

### Update the Running Instructions

Add a short **Running the Prototype** section to the repository's main `README.md`. It should tell another person to:

1. Create and activate `.venv` if needed.
2. Install `requirements.txt`.
3. Run `python database/setup_database.py`.
4. Run `python server/server.py` in one terminal.
5. Run `python client/client.py` in another terminal.

One member commits and pushes the test evidence and documentation. Everyone else pulls it.

Suggested commit message:

```text
Document and test the Azerbyte basic version
```

## Final Check: Basic Version Complete

The group has reached the basic version when:

- the Python client and Flask API run separately;
- the components communicate through HTTP and JSON;
- SQLite stores the character data;
- users can view all characters;
- users can find one character;
- users can create a character;
- users can update a character;
- missing and invalid requests receive useful responses;
- created and updated data remains after a restart;
- the database can be recreated from committed setup code;
- another group member can follow the README and run the system;
- the test record contains successful and unsuccessful requests;
- every member has made meaningful Git contributions; and
- every member has pulled and run the completed version.

This is a reliable starting point for the assessment. Higher attainment will come from improving the quality, testing and explanation of the prototype, then selecting suitable extensions. Do not add several new features before this version works consistently.

## Common Problems

### `ImportError` or `ModuleNotFoundError: api_client`

Check that both files are inside the same folder:

```text
client/
├── api_client.py
└── client.py
```

Run the client from the repository's main folder using:

```bash
python client/client.py
```

### `405 Method Not Allowed`

Check that the create route uses `@app.post` and the update route uses `@app.put`. Restart Flask after changing the server.

### `400 Bad Request`

Read the returned error. Check the field names, capitalisation of the class and realm, and the level range.

### A valid request causes an SQLite constraint error

Compare the values in `validate_character()` with the rules used by `database/setup_database.py`. They must match exactly.

### The created character disappears

Check that the API is connected to `database/azerbyte.db` and that the create route uses an SQL `INSERT`. Do not restore the old Python list.

### The menu appears but every request fails

Make sure Flask is still running on `127.0.0.1:5000` in the other terminal.

### A push is rejected

Do not force push. Commit completed work if needed, run `git pull` and read the message carefully. Speak to the group before discarding or replacing any file.
