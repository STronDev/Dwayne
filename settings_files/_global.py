import os
import pymongo
# from utils import get_mode

Settings_DIR = os.path.dirname(os.path.abspath(__file__))
Root_DIR = os.path.dirname(Settings_DIR)
Data_DIR = os.path.join(Root_DIR, 'data')

Discord_Token = os.getenv("Discord_Token", False)

Cogs_Folder = "cogs."

# Reddit

Redit_ID = os.getenv("Redit_ID")
Redit_Secret = os.getenv("Redit_Secret")
Redit_Subredits = [
	'memes',
	'dankmemes',
	'terriblefacebookmemes'
]

# Role Settings

MODERATOR = "Moderator"

# Server Stuff

BANNER = ""
PREFIX = ""

# Pymongo

myclient = pymongo.MongoClient("mongodb+srv://STron:kGLRfUyXLis5ztnf@discord.1uuuu.mongodb.net/discord?retryWrites=true&w=majority")
mydb = myclient["discord"]

server_settings = mydb["ServerSettings"]

# Oxfoard

app_id = "44e8e4d5"
app_key = "1839ccf435c00605e29b24969897a1a8"
