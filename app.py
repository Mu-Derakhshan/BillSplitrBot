from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = "7559634418:AAEAaD4OCOTnHWfmY8Zz6sJWQEZQzewLcYQ"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

@app.route('/webhook', methods=['POST'])
def telegram_webhook():
    data = request.get_json()
    
    # Extract chat ID and message text
    chat_id = data['message']['chat']['id']
    message_text = data['message'].get('text', '')

    # Respond to the /start command
    if message_text == '/start':
        send_message(chat_id, "Sent using webhook: HI!")
    
    return "OK", 200

def send_message(chat_id, text):
    """Send a message to a Telegram user."""
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
    }
    requests.post(url, json=payload)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, ssl_context=(
        '/etc/letsencrypt/live/bot.joinet.buzz/fullchain.pem',
        '/etc/letsencrypt/live/bot.joinet.buzz/privkey.pem'
    ))
