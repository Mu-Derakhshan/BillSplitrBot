from api import setMyCommands
from app import create_app

app = create_app()

if __name__ == "__main__":
    setMyCommands(
        [
            {"command": "help", "description": "help"},
            {"command": "register", "description": "register yourself in this group"},
            {"command": "add_bill", "description": "add your bill"},
            {"command": "pay", "description": "use this to pay your debts"},
            {"command": "summary", "description": "summary of all bills in the group"},
            {
                "command": "my_debts",
                "description": "see the summary of your bills only",
            },
            {"command": "reset", "description": "remove all expenses and bills paid and unpaid use carefully"},
        ],
        scope={"type": "all_group_chats"}
    )
    app.run(
        host="0.0.0.0",
        port=443,
        ssl_context=(
            "/etc/letsencrypt/live/bot.joinet.buzz/fullchain.pem",
            "/etc/letsencrypt/live/bot.joinet.buzz/privkey.pem",
        ),
    )
