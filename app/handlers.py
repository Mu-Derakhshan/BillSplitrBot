from db import get_db

def add_bill_handler(data):
    db = get_db()
    user_ids = []
    usernames_unknown = []
    for entity in data["message"]["entities"]:
        if entity["type"] == "mention":
            username = data["message"]["text"][entity["offset"]:entity["offset"]+entity["length"]]
            # Search for username in database if not found prompt them /register themselves
            user = db.users.find({"username": username})
            if user:
                user_ids.append(user["user_id"])
            else:
                usernames_unknown.append(username)
        elif entity["type"] == "text_mention":
            user_id = entity["user"]["id"]
            user_ids.append(user_id)
    if usernames_unknown:
        return False, usernames_unknown
    return True, user_ids
