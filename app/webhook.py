from flask import Blueprint, request, jsonify
from flask_pymongo import PyMongo
from api import sendMessage
from db import get_db

webhook = Blueprint('webhook', __name__)

@webhook.route('/webhook', methods=['POST'])
def handle_webhook():
    # Access the Flask-PyMongo instance
    db = get_db()

    # Extract the JSON data from the request
    data = request.json

    if data["message"]["text"] == "/start":
        sendMessage(data["message"]["chat"]["id"], "Hello I got your message")
    
    return "OK", 200

    """# Insert the data into the MongoDB collection
    collection = mongo.db.your_collection_name
    result = collection.insert_one(data)

    # Return a response with the inserted document ID
    response = {"message": "Webhook received", "data": data, "id": str(result.inserted_id)}
    return jsonify(response)"""

