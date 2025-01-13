import re
from db import get_db

def extract_user_ids(data):
    db = get_db()
    user_ids = []
    usernames_unknown = []
    for entity in data["message"]["entities"]:
        if entity["type"] == "mention":
            username = data["message"]["text"][entity["offset"]:entity["offset"]+entity["length"]]
            # Search for username in database if not found prompt them /register themselves
            user = db.users.find_one({"username": username[1:]})
            if user:
                user_ids.append(user["user_id"])
            else:
                usernames_unknown.append(username)
        elif entity["type"] == "text_mention":
            user_id = entity["user"]["id"]
            user_ids.append(user_id)
    if usernames_unknown:
        return False, usernames_unknown
    return True, [int(user_id) for user_id in user_ids]

def extract_title(data):
    for entity in data["message"]["entities"]:
        if entity["type"] == "hashtag":
            return data["message"]["text"][entity["offset"]:entity["offset"]+entity["length"]]


def extract_amount(data):
    text = re.search(r"[\$€£]\d+(\.\d{1,2})?", data["message"]["text"])[0]
    amount = float(text[1:])
    return amount
