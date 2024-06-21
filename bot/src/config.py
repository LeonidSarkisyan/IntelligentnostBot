import os

from dotenv import load_dotenv

load_dotenv()

DEBUG = bool(int(os.environ.get("DEBUG")))
BOT_TOKEN = os.environ.get("BOT_TOKEN")

if DEBUG:
    MODERATOR_ID = int(os.environ.get("MODERATOR_ID_DEBUG"))
else:
    MODERATOR_ID = int(os.environ.get("MODERATOR_ID"))

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_NAME = os.environ.get("DB_NAME")

LEGIT_PRICE = int(os.environ.get("LEGIT_PRICE"))
FIND_PRICE = int(os.environ.get("FIND_PRICE"))

COUNT_START_BONUS_MONEY = 150

SITE_NAME = "https://intelligent-store.ru"