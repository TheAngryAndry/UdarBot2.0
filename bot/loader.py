from datetime import timedelta, datetime

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from loguru import logger
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler

load_dotenv()  # Load environment variables from .env file

# Parse all environment variables
TOKEN = os.environ.get('BOT_TOKEN')
MONGO_URI = os.environ.get('MONGO_URI')
MONGO_DB = os.environ.get('MONGO_DB')
MONGO_USER = os.environ.get('MONGO_USER')
MONGO_PASS = os.environ.get('MONGO_PASS')
BOT_PASS = os.environ.get('BOT_PASS')
ADMINS = os.environ.get('ADMINS')
TIME_FORMAT = "%Y/%m/%d %H:%M:%S"
LOCAL_TIME = +3


def alarm(time):
    print('Alarm! This alarm was scheduled at %s.' % time)


# Check if token is provided
if not TOKEN:
    logger.error('Token not provided')
    exit(-1)

# Set up bot and dispatcher
bot = Bot(token=TOKEN, defaults=DefaultBotProperties(parse_mode=ParseMode.HTML))
scheduler = AsyncIOScheduler()
dp = Dispatcher()
router = Router()
dp.include_router(router)

# scheduler = AsyncIOScheduler()
# scheduler.add_executor('processpool')
# scheduler.add_jobstore('mongodb', collection='jobs')
#
# alarm_time = datetime.now() + timedelta(seconds=10)  # TODO: remove
#
# scheduler.add_job(alarm, 'date', run_date=alarm_time, args=[datetime.now()])
#
# scheduler.start()
