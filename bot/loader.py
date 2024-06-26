from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from loguru import logger

import os

load_dotenv() # Load environment variables from .env file

# Parse all environment variables
TOKEN = os.environ.get('BOT_TOKEN')
MONGO_URI = os.environ.get('MONGO_URI')
MONGO_DB = os.environ.get('MONGO_DB')
MONGO_USER = os.environ.get('MONGO_USER')
MONGO_PASS = os.environ.get('MONGO_PASS')
BOT_PASS = os.environ.get('BOT_PASS')
TIME_FORMAT = "%Y/%m/%d %H:%M:%S"

# Check if token is provided
if not TOKEN:
    logger.error('Token not provided')
    exit(-1)

# Set up bot and dispatcher
bot = Bot(token=TOKEN,defaults=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
router = Router()
dp.include_router(router)