import requests
from requests import RequestException

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