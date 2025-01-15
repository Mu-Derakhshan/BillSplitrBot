import os
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
host = os.getenv("MONGO_HOST")
port = os.getenv("MONGO_PORT", 27017)
database_name = os.getenv("MONGO_DATABASE")

class Config:
    DEBUG = True
    SECRET_KEY = "your_secret_key"
    MONGO_URI = f"mongodb://{username}:{password}@{host}:{port}/{database_name}?authSource=admin"
