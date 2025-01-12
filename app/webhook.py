from flask import Blueprint, request, jsonify
from api import sendMessage
from db import get_db

webhook = Blueprint('webhook', __name__)

@webhook.route('/webhook', methods=['POST'])
def handle_webhook():
    # Access the Flask-PyMongo instance
    db = get_db()

    # Extract the JSON data from the request
    data = request.json

    if data.get("message", {}).get("text", "") == "/start":
        sendMessage(data["message"]["chat"]["id"], "Hello I got your message")

    if (membership_update := data.get("my_chat_member", {})):
        if (
            membership_update["old_chat_member"]["status"] in ["administrator", "member"] and 
            membership_update["new_chat_member"]["status"] in ["left", "kicked"]
        ):
            print(f"Removed from chat {membership_update['chat']['id']}")
        elif (
            membership_update["new_chat_member"]["status"] in ["administrator", "member"] and 
            membership_update["old_chat_member"]["status"] in ["left", "kicked"] 
        ):
            sendMessage(membership_update['chat']['id'], "Hello I'm added to your group")
            print(f"added to chat {membership_update['chat']['id']}")

    ### Handling the commands ###
    if (msg := data.get("message", {})):
        if msg["chat"]["type"] in ["group", "supergroup"]:
            if (entities := msg.get(entities, None))
                print(entities)
    
    return "OK", 200

    """# Insert the data into the MongoDB collection
    collection = mongo.db.your_collection_name
    result = collection.insert_one(data)

    # Return a response with the inserted document ID
    response = {"message": "Webhook received", "data": data, "id": str(result.inserted_id)}
    return jsonify(response)"""

