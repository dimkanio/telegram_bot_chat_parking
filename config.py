import os

TOKEN = os.environ['TOKEN']
PARKING_CHAT_ID = os.environ['PARKING_CHAT_ID']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DBPATH = os.path.join(BASE_DIR, "parkingdb")
