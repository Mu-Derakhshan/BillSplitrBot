from flask import Blueprint, request, jsonify
from api import sendMessage
from db import get_db
from helpers import extract_user_ids, extract_title, extract_amount
from jinja2 import Template

webhook = Blueprint('webhook', __name__)

@webhook.route('/webhook', methods=['POST'])
def handle_webhook():
    # Access the Flask-PyMongo instance
    db = get_db()

    # Extract the JSON data from the request
    data = request.json

    if data.get("message", {}).get("text", "") == "/start":
        try:
            with open("MessageTemplates/start.txt", "r") as file:
                start_message = file.read()
            sendMessage(data["message"]["chat"]["id"], start_message)
        except FileNotFoundError:
            sendMessage(data["message"]["chat"]["id"], "Welcome! Please add me to your group and grant me admin rights.")

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
            if (entities := msg.get("entities", None)):
                cmd = None
                for entity in entities:
                    if entity["type"] == "bot_command":
                        cmd = msg["text"][entity["offset"]:entity["offset"]+entity["length"]]
                if cmd == "/register@BillSplitrBot":
                    db.users.update_one(
                        {"user_id": msg["from"]["id"]},
                        {"$set": {"username": msg["from"].get("username", ""), "first_name": msg["from"]["first_name"]}},
                        upsert=True
                    )
                    sendMessage(msg["chat"]["id"], "You are registered successfully")
                if cmd == "/add_bill@BillSplitrBot":
                    done, *result = extract_user_ids(data)
                    if not done:
                        usernames_unknown = result[0]
                        text_mentions_unknown = result[1]
                        with open('MessageTemplates/unregistered.txt', 'r') as file:
                            template_string = file.read()
                        template = Template(template_string)
                        context = {"usernames_unknown": usernames_unknown, "text_mentions_unknown": text_mentions_unknown}
                        rendered_string = template.render(context)
                        sendMessage(msg["chat"]["id"], rendered_string)
                        return "OK", 200
                    user_ids = result[0]
                    title = extract_title(data)
                    amount = extract_amount(data)
                    creditor = int(msg["from"]["id"])
                    new_expense = db.expenses.insert_one({
                        "chat_id": msg["chat"]["id"],
                        "title": title,
                        "amount": amount,
                        "creditor": creditor,
                        "debtors": user_ids,
                    })
                    amount_per_person = amount / len(user_ids)
                    db.bills.insert_many([
                        {
                            "expense_id": new_expense.inserted_id,
                            "chat_id": msg["chat"]["id"],
                            "creditor": creditor,
                            "debtor": debtor,
                            "amount": amount_per_person,
                            "is_paid": False
                        }
                        for debtor in user_ids if debtor != creditor
                    ])
                    sendMessage(msg["chat"]["id"], f"added the bill successfully")
                if cmd == "/summary@BillSplitrBot":
                    chat_id = msg["chat"]["id"]
                    expenses = db.expenses.find({"chat_id": chat_id})
                    for expense in expenses:
                        expense["creditor_name"] = db.users.find_one({"user_id": expense["creditor"]})["first_name"]
                        if expense["creditor"] in expense["debtors"]:
                            expense["amount_per_person"] = expense["amount"] / len(expense["debtors"])
                        else:
                            expense["amount_per_person"] = expense["amount"] / (len(expense["debtors"]) - 1)
                        debtor_paid_array = []
                        for debtor in expense["debtors"]:
                            if (bill := db.bills.find_one({"expense_id": expense["_id"], "chat_id": chat_id, "debtor": debtor})):
                                is_paid = bill["is_paid"]
                                debtor_name = db.users.find_one({"user_id": debtor})["first_name"]
                                debtor_paid_array.append((debtor, debtor_name, is_paid))
                        expense["debtors"] = debtor_paid_array
                    with open('MessageTemplates/summary.txt', 'r') as file:
                        template_string = file.read()
                    template = Template(template_string)
                    print(list(expenses))
                    context = {"expenses": list(expenses)}
                    rendered_string = template.render(context)
                    sendMessage(msg["chat"]["id"], rendered_string)
    
    return "OK", 200

    """# Insert the data into the MongoDB collection
    collection = mongo.db.your_collection_name
    result = collection.insert_one(data)

    # Return a response with the inserted document ID
    response = {"message": "Webhook received", "data": data, "id": str(result.inserted_id)}
    return jsonify(response)"""
