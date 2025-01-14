from api import sendMessage
from flask import request


def handle_internal_error(error):
    data = request.json
    chat_id = data["message"]["chat"]["id"]
    sendMessage(chat_id, "Error happened double check your command!")
    return "OK", 200