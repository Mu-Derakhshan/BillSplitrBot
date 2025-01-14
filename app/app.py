from flask import Flask

from db import close_db
from middlewares import handle_internal_error


def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object("config.Config")

    # Register the webhook route
    from webhook import webhook as webhook_blueprint

    app.register_blueprint(webhook_blueprint)

    app.teardown_appcontext(close_db)
    app.register_error_handler(500, handle_internal_error)

    return app
