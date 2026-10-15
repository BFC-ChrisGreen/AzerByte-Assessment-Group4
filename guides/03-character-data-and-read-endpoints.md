# Guide 3: Character Data and Read Endpoints

Your client and API can already communicate through the `/health` endpoint. The next job is to move beyond that test response and exchange useful Azerbyte character data.

By the end of this guide, the client will be able to:

- request all characters;
- request one character using its ID; and
- handle a character that does not exist.

The character data will be held in a Python list for now. This keeps the focus on requests, responses and agreed data rules. The next guide will move the same data into SQLite so that it is not lost when the server stops.

## 1. Get the Group Ready

Before anyone changes a file, every member runs:

```bash
git status
git pull
```

The working tree should be clean before the group continues. If `git status` lists changes you do not recognise, stop and speak to the group before deleting or replacing anything.

Open two terminals in Visual Studio Code.

In the first terminal, activate the virtual environment and start the server:

```bash
.venv\Scripts\activate
python server/server.py
```

Keep the server running. In the second terminal, activate the virtual environment and run the client:

```bash
.venv\Scripts\activate
python client/client.py
```

The client should report:

```text
Azerbyte service status: online
```

Do not begin the new work until the Guide 2 client and server still work.

Agree who will take the lead on each part of this guide:

- character data and rules;
- server endpoints;
- client changes; and
- testing and documentation.

If your group has three members, combine the testing and documentation role with one of the others. Change the roles from the previous guide where possible.

Each member updates the **Proposed Project Role** section in their own file inside:

```text
team-practice/members
```

Use the role you are completing in this guide. Update this again when the group rotates roles in a later guide.

## 2. Agree the Character Data

Open:

```text
docs/data-rules.md
```

Record the rules below in the document. Use these starter values so that every component begins with the same rules.

| Field | Data type | Rule |
|---|---|---|
| `character_id` | Integer | Unique and greater than zero |
| `name` | String | Between 2 and 30 characters |
| `character_class` | String | `Warrior`, `Mage`, `Rogue`, `Priest` or `Ranger` |
| `level` | Integer | Between 1 and 60 |
| `realm` | String | `Emberfall`, `Ironhollow`, `Moonspire` or `Stormwatch` |

For this guide, use at least two fictional characters. Groups may add more allowed classes or realms later, but the updated values must be recorded in `docs/data-rules.md` and used consistently by the client, API and database. Do not use real personal data.

### Checkpoint

Before writing the endpoints, each member should be able to answer:

- Why must the client and server use the same field names?
- What might happen if one component stores `level` as text and another expects an integer?
- Why does each character need a unique ID?

The member responsible for the data rules commits and pushes the completed document. Everyone else pulls before continuing.

Suggested commit message:

```text
Agree Azerbyte character data rules
```

## 3. Add Temporary Character Data

Open:

```text
server/server.py
```

Keep the existing Flask imports, app and `/health` route. Below `app = Flask(__name__)`, add:

```python
characters = [
    {
        "character_id": 1,
        "name": "Aelwyn",
        "character_class": "Mage",
        "level": 24,
        "realm": "Emberfall",
    },
    {
        "character_id": 2,
        "name": "Bromm",
        "character_class": "Warrior",
        "level": 18,
        "realm": "Ironhollow",
    },
]
```

This is temporary in-memory data. It will be available while the server is running, but changes would be lost when the program stops. SQLite will replace it in the next guide.

Check that every dictionary uses the field names recorded in `docs/data-rules.md`.

## 4. Return All Characters

Add this route above the final `if __name__ == "__main__":` block:

```python
@app.get("/characters")
def get_characters():
    return jsonify(characters), 200
```

Run the server and visit:

```text
http://127.0.0.1:5000/characters
```

The browser should display a JSON list containing both characters.

### Checkpoint

The server builder now commits and pushes the working endpoint. Everyone else pulls the change and tests it before the group continues.

Suggested commit message:

```text
Add character list endpoint
```

## 5. Return One Character

A client should not need to download every character when it only wants one. Add a second route:

```python
@app.get("/characters/<int:character_id>")
def get_character(character_id):
    for character in characters:
        if character["character_id"] == character_id:
            return jsonify(character), 200

    return jsonify({"error": "Character not found"}), 404
```

Test an ID that exists:

```text
http://127.0.0.1:5000/characters/1
```

Then test an ID that does not exist:

```text
http://127.0.0.1:5000/characters/999
```

The first request should return one character with status code `200`. The second should return a short JSON error with status code `404`.

### Checkpoint

Explain within the group:

- what the value after `/characters/` represents;
- why the route uses `<int:character_id>`; and
- why a missing character should return `404` rather than `200`.

Do not continue until all three requests work: all characters, one existing character and one missing character.

## 6. Request Character Data from the Client

Open:

```text
client/client.py
```

Keep the existing imports, `SERVICE_URL` and `check_service()` function. Add the following function below `check_service()`:

```python
def request_json(endpoint):
    try:
        response = requests.get(f"{SERVICE_URL}{endpoint}", timeout=5)

        if response.status_code == 404:
            print(response.json()["error"])
            return None

        response.raise_for_status()
        return response.json()
    except RequestException:
        print("The Azerbyte service could not be reached.")
        return None
```

This function keeps the request and error handling in one place. Other client functions can use it without repeating the same code.

Next, add:

```python
def display_all_characters():
    characters = request_json("/characters")

    if characters is None:
        return

    print("Azerbyte characters")
    for character in characters:
        print(
            f"{character['character_id']}: {character['name']} - "
            f"Level {character['level']} {character['character_class']} "
            f"on {character['realm']}"
        )


def display_character(character_id):
    character = request_json(f"/characters/{character_id}")

    if character is None:
        return

    print(
        f"{character['name']} is a level {character['level']} "
        f"{character['character_class']} on {character['realm']}."
    )
```

Replace the existing final block with:

```python
if __name__ == "__main__":
    check_service()
    print()
    display_all_characters()
    print()
    display_character(1)
    print()
    display_character(999)
```

Make sure the server is running in the first terminal:

```bash
python server/server.py
```

Run the client in the second terminal:

```bash
python client/client.py
```

The output should look like this:

```text
Azerbyte service status: online

Azerbyte characters
1: Aelwyn - Level 24 Mage on Emberfall
2: Bromm - Level 18 Warrior on Ironhollow

Aelwyn is a level 24 Mage on Emberfall.

Character not found
```

Small spacing differences are fine. The important part is that all four results appear without the client crashing.

The client builder commits and pushes the completed change. Everyone else pulls and runs it.

Suggested commit message:

```text
Display character data in the client
```

## 7. Record the Tests

Open:

```text
evidence/test-record.md
```

Record the actual result of each test:

| Test | Expected result |
|---|---|
| Request `/characters` | Status `200` and a JSON list |
| Request an existing character ID | Status `200` and one character |
| Request character ID `999` | Status `404` and a clear JSON error |
| Run the client with the server stopped | A clear connection message rather than a crash |

Record failures as well as successful results. If a test fails, fix the problem and record the retest.

The member responsible for testing commits and pushes the completed evidence.

Suggested commit message:

```text
Record character endpoint tests
```

## 8. Record the Storage Decision

Open:

```text
docs/technical-decisions.md
```

Add a short entry explaining that character data is temporarily stored in a Python list so that the group can build and test the read endpoints first. Record that SQLite will replace this list in the next stage to provide persistent storage.

Keep this to a few clear sentences.

## Final Check

Before the group finishes this guide, make sure that:

- the original `/health` endpoint still works;
- `/characters` returns every character;
- `/characters/1` returns one character;
- `/characters/999` returns a JSON error and status `404`;
- the client displays the full list and an individual character;
- the field names and data types match `docs/data-rules.md`;
- the test record includes successful and unsuccessful requests;
- the technical decision has been recorded;
- every member has pulled the finished version; and
- the repository shows contributions from different group members.

At this point, your group has a working read-only version of Azerbyte. The next guide will replace the temporary Python list with SQLite so that character data remains available after the server restarts.

## Common Problems

### Check these first

Before changing or deleting any code, check the following:

1. Both Visual Studio Code terminals are open in the group's Azerbyte repository.
2. The virtual environment is active in both terminals.
3. The Flask server is still running in one terminal.
4. The server is using `127.0.0.1` and port `5000`.
5. The client uses the same address and port.
6. `git pull` has been completed and the latest group changes are visible.

Keep the original error message visible while checking these points.

### The new route returns `404 Not Found`

Check the spelling of the URL and make sure the route appears above:

```python
if __name__ == "__main__":
```

Restart the server after changing the file.

### `NameError: characters is not defined`

Make sure the `characters` list is in `server/server.py` and appears before the route functions.

### `KeyError` in the client

Check that every dictionary uses exactly the same field names as the client. For example, `character_class` and `class` are different keys.

### The client reports that the service cannot be reached

Make sure the Flask server is still running in its own terminal and is using port `5000`.

### Git rejects a push

Do not force push. Commit your work if needed, run `git pull` and read the message carefully. Ask for help before discarding any change.
