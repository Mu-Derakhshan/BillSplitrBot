import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
host = os.getenv("MONGO_HOST")
port = os.getenv("MONGO_PORT", 27017)
database_name = os.getenv("MONGO_DATABASE")

escaped_username = quote_plus(username)
escaped_password = quote_plus(password)

class Config:
    DEBUG = True
    SECRET_KEY = "your_secret_key"
    MONGO_URI = f"mongodb://{escaped_username}:{escaped_password}@{host}:{port}/{database_name}?authSource=admin"
