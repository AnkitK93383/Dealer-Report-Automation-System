import json
import bcrypt


def authenticate(username, password):

    with open("users.json", "r") as f:
        users = json.load(f)

    for user in users:

        if (
            user["username"] == username
            and bcrypt.checkpw(
                password.encode("utf-8"),
                user["password"].encode("utf-8")
            )
        ):
            return user

    return None