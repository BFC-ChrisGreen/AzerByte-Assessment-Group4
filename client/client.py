import requests
from requests import RequestException

SERVICE_URL = "http://127.0.0.1:5000"

def check_service():
    try:
        response = requests.get(f"{SERVICE_URL}/health", timeout=5)
        response.raise_for_status()
        data = response.json()
        print(f"Azerbyte service status: {data['status']}")
    except RequestException:
        print("The Azerbyte service could not be reached.")
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
if __name__ == "__main__":
    check_service()
    print()
    display_all_characters()
    print()
    display_character(1)
    print()
    display_character(999)
