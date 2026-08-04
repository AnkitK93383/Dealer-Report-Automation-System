import uuid
import os


def create_session_folder():

    session_id = str(uuid.uuid4())

    folder = os.path.join(
        "temp",
        session_id
    )

    os.makedirs(
        folder,
        exist_ok=True
    )

    return folder