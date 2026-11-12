import requests
from requests import RequestException


SERVICE_URL = "http://127.0.0.1:5000"

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

def get_characters():
    return send_request("GET", "/characters")


def get_character(character_id):
    return send_request("GET", f"/characters/{character_id}")


def create_character(character):
    return send_request("POST", "/characters", character)


def update_character(character_id, character):
    return send_request("PUT", f"/characters/{character_id}", character)