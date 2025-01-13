"""
This script contains essential functions for interacting with the Telegram Bot API using raw HTTP requests. 
Functions include sending messages, setting webhooks, getting updates, etc.

Main contributor: Muhammad Derakhshan
"""

import requests
import json
import os
from dotenv import load_dotenv


load_dotenv()
botToken = os.getenv("BOT_TOKEN")
if not botToken:
    raise ValueError("No bot token found. Please check your .env file.")
baseUrl = f'https://api.telegram.org/bot{botToken}/'

def getMe():
    """
    A simple method for testing your bot's authentication token.
    Requires no parameters.
    Returns basic information about the bot in form of a User object.
    """
    requestUrl = f'{baseUrl}getMe'
    response = requests.get(requestUrl)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None
    return response.json()

def sendMessage(chatId, text):
    """
    Use this method to send text messages. On success, the sent Message is returned.
    """
    requestUrl = f'{baseUrl}sendMessage'
    payload = {'chat_id': chatId, 'text': text, "parse_mode": "MarkdownV2"}
    response = requests.post(requestUrl, json=payload)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.json())
        return None
    return response.json()

def editMessageText(chatId, messageId, text):
    """
    Use this method to edit text and game messages.
    On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returned.
    Note that business messages that were not sent by the bot and do not contain an inline keyboard can only be edited within 48 hours from the time they were sent.
    """
    requestUrl = f'{baseUrl}editMessageText'
    payload = {'chat_id': chatId, 'message_id': messageId, 'text': text}
    response = requests.post(requestUrl, json=payload)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None
    return response.json()

def forwardMessage(chatId, fromchatId, messageId):
    """
    Use this method to forward messages of any kind.
    Service messages and messages with protected content can't be forwarded.
    On success, the sent Message is returned.
    """
    requestUrl = f'{baseUrl}forwardMessage'
    payload = {'chat_id': chatId, 'from_chat_id': fromchatId, 'message_id': messageId}
    response = requests.post(requestUrl, json=payload)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None
    return response.json()

def getChat(chatId):
    """
    Use this method to get up-to-date information about the chat.
    Returns a ChatFullInfo object on success.
    """
    requestUrl = f'{baseUrl}getChat'
    payload = {'chat_id': chatId}
    response = requests.get(requestUrl, params=payload)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None
    return response.json()

def getChatMemberCount(chatId):
    """
    Use this method to get the number of members in a chat. Returns Int on success.
    """
    requestUrl = f'{baseUrl}getChatMemberCount'
    payload = {'chat_id': chatId}
    response = requests.get(requestUrl, params=payload)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None
    return response.json()

def getChatMember(chatId, userId):
    """
    Use this method to get information about a member of a chat.
    The method is only guaranteed to work for other users if the bot is an administrator in the chat.
    Returns a ChatMember object on success.
    """
    requestUrl = f'{baseUrl}getChatMember'
    payload = {'chat_id': chatId, 'user_id': userId}
    response = requests.get(requestUrl, params=payload)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None
    return response.json()

def setMyCommands(commands, scope=None, languageCode=None):
    """
    Use this method to change the list of the bot's commands.
    See this manual for more details about bot commands.
    Returns True on success.
    
    core.telegram.org/bots/features#commands
    """
    requestURL = f'{baseUrl}setMyCommands'
    payload = {'commands': json.dumps(commands)}
    if scope is not None:
        payload['scope'] = json.dumps(scope)
    if languageCode:
        payload['language_code'] = languageCode
    response = requests.post(requestURL, json=payload)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None
    return response.json()

def setChatMenuButton(chatId=None, menuButton=None):
    """
    Use this method to change the bot's menu button in a private chat, or the default menu button.
    Returns True on success.
    """
    requestURL = f'{baseUrl}setChatMenuButton'
    payload = {}
    if chatId:
        payload['chat_id'] = chatId
    if menuButton:
        payload['menu_button'] = json.dumps(menuButton)
    response = requests.post(requestURL, json=payload)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None
    return response.json()

def setMyDefaultAdministratorRights(rights=None, for_channels=False):
    """
    Use this method to change the default administrator rights requested by the bot when it's added as an administrator to groups or channels.
    These rights will be suggested to users, but they are free to modify the list before adding the bot.
    Returns True on success.
    """
    requestURL = f'{baseUrl}setMyDefaultAdministratorRights'
    payload = {}
    if rights:
        payload['rights'] = json.dumps(rights)
    if for_channels:
        payload['for_channels'] = True
    response = requests.post(requestURL, json=payload)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None
    return response.json()
