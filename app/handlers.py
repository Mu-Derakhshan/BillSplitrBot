from api import get_user_id
from client import get_client
import asyncio


def add_bill_handler(data):
    # get people in the bill
    user_ids = []
    for entity in data["message"]["entities"]:
        if entity["type"] == "mention":
            username = data["message"]["text"][entity["offset"]:entity["offset"]+entity["length"]]

            """loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            client = get_client()
            with client:
                user_id = client.loop.run_until_complete(get_user_id(username))
                user_ids.append(user_id)"""

            user_id = asyncio.run(get_user_id(username))

        elif entity["type"] == "text_mention":
            user_id = entity["user"]["id"]
            user_ids.append(user_id)
    return user_ids
