import json


def authenticate(username, password):

    with open("users.json", "r") as f:
        users = json.load(f)

    for user in users:

        if (
            user["username"] == username
            and user["password"] == password
        ):
            return user

    return None