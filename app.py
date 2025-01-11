from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import requests
import bot

load_dotenv()

app = Flask(__name__)

webhookUrl = os.getenv("WEBHOOK_URL")
if not webhookUrl:
    raise ValueError("No webhook URL found. Please check your .env file.")

botToken = os.getenv("BOT_TOKEN")
baseUrl = f'https://api.telegram.org/bot{botToken}/'

# TO DO
def processUpdate(update):
    """
    This function processes the incoming updates from Telegram.
    You can handle messages, commands, etc., inside here.
    """

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    This is the route that Telegram sends updates to.
    We will process the incoming update here.
    """
    update = request.get_json()
    if update:
        processUpdate(update)
    return jsonify({"status": "ok"}), 200

def setWebhook(url=None):
    """
    Set the webhook for your bot. 
    The URL should be your server's endpoint where the bot will receive incoming updates.
    If no URL is provided, it will default to the one in the .env file.
    """
    if url is None:
        url = os.getenv("WEBHOOK_URL")
        if not url:
            raise ValueError("No webhook URL found. Please check your .env file.")
    
    requestUrl = f'{baseUrl}setWebhook'
    payload = {'url': url}
    response = requests.post(requestUrl, json=payload)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None
    return response.json()

if __name__ == '__main__':
    setWebhook(webhookUrl)
    app.run(debug=True, host="0.0.0.0", port=5000)