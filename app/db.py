from pymongo import MongoClient
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db_client = MongoClient(current_app.config['MONGO_URI'])
        g.db = g.db_client.get_default_database()
    return g.db

def close_db(e=None):
    db_client = g.pop('db_client', None)
    if db_client is not None:
        db_client.close()
