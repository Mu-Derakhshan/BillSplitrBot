from flask import Flask
from flask_pymongo import PyMongo

def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object('config.Config')

    # Initialize Flask-PyMongo
    mongo = PyMongo(app)

    # Register the webhook route
    from webhook import webhook as webhook_blueprint
    app.register_blueprint(webhook_blueprint)

    return app

