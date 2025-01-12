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

    if (new_members := data.get("message", {}).get("new_chat_members", [])):
        for member in new_members:
            if member["id"] == 7559634418:
                sendMessage(data["message"]["chat"]["id"], "Hello I'm added to your group")

    if (membership_update := update.get("my_chat_member", {})):
        if (
            membership_update["old_chat_member"]["status"] == ["administrator", "member"] and 
            membership_update["new_chat_member"]["status"] == ["left", "kicked"]
        ):
            print(f"Removed from chat {membership_update['chat']['id']}")
        elif (
            membership_update["new_chat_member"]["status"] == ["administrator", "member"] and 
            membership_update["old_chat_member"]["status"] == ["left", "kicked"] 
        ):
            print(f"added to chat {membership_update['chat']['id']}")
    
    return "OK", 200

    """# Insert the data into the MongoDB collection
    collection = mongo.db.your_collection_name
    result = collection.insert_one(data)

    # Return a response with the inserted document ID
    response = {"message": "Webhook received", "data": data, "id": str(result.inserted_id)}
    return jsonify(response)"""

