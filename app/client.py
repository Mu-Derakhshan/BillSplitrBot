from telethon import TelegramClient
from flask import g


api_id = '29987776'
api_hash = '405ae53edc62eeb2bf37808608e102f3'
phone_number = '14808537840'

def get_client():
    if 'client' not in g:
        g.client = TelegramClient('bill_session', api_id, api_hash)
    return g.client