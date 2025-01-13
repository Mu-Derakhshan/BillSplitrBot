from api import get_user_id
from client import get_client
import asyncio


def add_bill_handler(data):
    # get people in the bill
    user_ids = []
    for entity in data["message"]["entities"]:
        if entity["type"] == "mention":
            username = data["message"]["text"][entity["offset"]:entity["offset"]+entity["length"]]

            client = get_client()
            with client:
                client.loop.run_until_complete(get_user_id(username))
            user_ids.append(user_id)
        elif entity["type"] == "text_mention":
            user_id = entity["user"]["id"]
            user_ids.append(user_id)
    return user_ids
