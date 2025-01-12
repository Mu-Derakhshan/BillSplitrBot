from api import getChat


def add_bill_handler(data):
    # get people in the bill
    user_ids = []
    for entity in data["message"]["entities"]:
        if entity["type"] == "mention":
            username = data["message"]["text"][entity["offset"]:entity["offset"]+entity["length"]]
            print(getChat(username))
            user_id = getChat(username)["id"]
            user_ids.append(user_id)
        elif entity["type"] == "text_mention":
            user_id = entity["user"]["id"]
            user_ids.append(user_id)
    return user_ids
