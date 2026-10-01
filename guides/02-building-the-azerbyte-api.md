# Guide 2: Building the Azerbyte API

In Topic 2, the Launch Night program was separated into Python modules. Those modules still ran together as one local program. Azerbyte now needs two independently running components that communicate over a network.

In this guide, your group will build:

```text
Python client → HTTP request → Flask API
Python client ← JSON response ← Flask API
```

The first endpoint is deliberately small. The aim is to understand the communication before adding character data, a user interface or a database.

## 1. Prepare the Repository

Before changing anything, every member runs:

```bash
git status
git pull
```

The working tree should be clean.

Agree who will complete each role for this stage:

- Server build
- Client build
- Testing and evidence
- Review and documentation, where there is a fourth member

These roles are only for this stage. They should change during later work so that everyone contributes to different parts of the project.

## 2. Create the Python Environment

Each member creates a local virtual environment from the repository's main folder:

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

The `.venv` folder is local to your computer and is excluded from Git.

### Checkpoint

Run:

```bash
python -m pip show Flask
python -m pip show requests
```

Both packages should be listed.

## 3. Build the Smallest Flask Server

The member responsible for the server creates:

```text
server/server.py
```

Add the following first:

```python
from flask import Flask, jsonify

app = Flask(__name__)
```

This imports Flask and creates the application that will receive requests.

Next, add the first route:

```python
@app.get("/health")
def health():
    return jsonify({"service": "azerbyte", "status": "online"}), 200
```

The route connects a `GET` request for `/health` to the `health` function. `jsonify` turns the Python dictionary into a JSON response. `200` is the HTTP status code for a successful request.

Finally, add:

```python
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
```

Save the file and run:

```bash
python server/server.py
```

Keep this terminal open. The server must continue running while it receives requests.

## 4. Test the Endpoint Directly

Open a web browser and visit:

```text
http://127.0.0.1:5000/health
```

Expected response:

```json
{
  "service": "azerbyte",
  "status": "online"
}
```

### Checkpoint

Explain these points within the group before continuing:

- What does `/health` identify?
- Why is the response JSON rather than normal Python output?
- What does status code `200` tell the client?

The server builder now commits and pushes the working endpoint. Everyone else pulls it before continuing.

Suggested commit message:

```text
Add Azerbyte health endpoint
```

## 5. Build the Separate Client

The member responsible for the client creates:

```text
client/client.py
```

Add:

```python
import requests

SERVICE_URL = "http://127.0.0.1:5000"
```

The `requests` library allows this separate program to send HTTP requests to the Flask API.

Next, add:

```python
def check_service():
    response = requests.get(f"{SERVICE_URL}/health", timeout=5)
    response.raise_for_status()
    data = response.json()
    print(f"Azerbyte service status: {data['status']}")
```

Finally, add:

```python
if __name__ == "__main__":
    check_service()
```

Open a second terminal, activate the virtual environment and run:

```bash
python client/client.py
```

Expected output:

```text
Azerbyte service status: online
```

### Checkpoint

Stop the Flask server using **Ctrl+C**, then run the client again.

The request should now fail because the client and server are genuinely separate. Restart the server before continuing.

## 6. Handle a Failed Connection

The current client stops with a long error if the service cannot be reached. Improve it by importing the exception type:

```python
from requests import RequestException
```

Then update `check_service`:

```python
def check_service():
    try:
        response = requests.get(f"{SERVICE_URL}/health", timeout=5)
        response.raise_for_status()
        data = response.json()
        print(f"Azerbyte service status: {data['status']}")
    except RequestException:
        print("The Azerbyte service could not be reached.")
```

Test the client once with the server running and once with it stopped.

The client builder now commits and pushes the completed client. Everyone else pulls it.

Suggested commit message:

```text
Connect Python client to Azerbyte API
```

## 7. Record the First Tests

Open:

```text
evidence/test-record.md
```

Record both results:

- The client receives `online` while the API is running.
- The client displays a clear message while the API is stopped.

The member responsible for testing commits and pushes the updated test record.

Suggested commit message:

```text
Record API connection tests
```

## 8. Explain What You Built

Add a short entry to `docs/technical-decisions.md` explaining why the prototype uses HTTP and JSON between the client and server.

Keep this brief. At this stage, the group is recording the decision, not writing the individual evaluation.

## Final Check

- `server/server.py` runs separately and provides `/health`.
- The endpoint returns JSON and status code `200`.
- `client/client.py` requests the endpoint successfully.
- The client handles the server being unavailable.
- The test record contains both results.
- The repository contains separate contributions from the group.
- Everyone has pulled the completed version.

You now have the first working part of a distributed system. The next guide will replace the simple health response with shared Azerbyte character data.

## Common Problems

### `ModuleNotFoundError`

Activate `.venv` and run:

```bash
python -m pip install -r requirements.txt
```

### Address already in use

Another Flask server may still be running. Find its terminal and stop it using **Ctrl+C** before starting the server again.

### The browser or client cannot connect

Check that:

- `server.py` is still running.
- The address is exactly `http://127.0.0.1:5000`.
- The endpoint includes `/health`.
- The client and server use the same port.

### Git rejects a push

Do not force push. Check that your work is committed, then run:

```bash
git pull --no-rebase
```

Resolve any reported conflict, test the final version and push again.
