from api import setMyCommands
from app import create_app

app = create_app()

if __name__ == "__main__":
    setMyCommands(
        [
            {
                "command": "register",
                "description": "register yourself in this group",
                "scope": {"type": "all_group_chats"},
            },
            {
                "command": "add_bill",
                "description": "add your bill",
                "scope": {"type": "all_group_chats"},
            },
            {
                "command": "pay",
                "description": "use this to pay your debts",
                "scope": {"type": "all_group_chats"},
            },
            {
                "command": "summary",
                "description": "summary of all bills in the group",
                "scope": {"type": "all_group_chats"},
            },
            {
                "command": "my_debts",
                "description": "see the summary of your bills only",
                "scope": {"type": "all_group_chats"},
            },
            {
                "command": "reset",
                "description": "reset and delete the history of all expenses and bills history",
                "scope": {"type": "all_chat_administrators"},
            }
        ]
    )
    app.run(
        host="0.0.0.0",
        port=443,
        ssl_context=(
            "/etc/letsencrypt/live/bot.joinet.buzz/fullchain.pem",
            "/etc/letsencrypt/live/bot.joinet.buzz/privkey.pem",
        ),
    )
