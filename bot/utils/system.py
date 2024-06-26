from bot.loader import bot, TIME_FORMAT
from loguru import logger
from bot.utils.models import UserTests, UserWord, Users
from bot.utils.texts import rnd_w_list
import time


async def start_test(test_length: int = 10, chat_id: int | None = None, user_id: int | None = None):
    if chat_id is None or user_id is None:
        logger.error('no chat id')
        exit(-1)
    words_list = [UserWord(user_id=user_id, success=None, time=None, word=i) for i in
                  await rnd_w_list(k=test_length)]  # TODO change time()
    data = UserTests(user_id=user_id, stage=0, words=words_list, time_start=time.time(),
                     time_end=None)  # TODO change time()
    await UserTests.insert(data)
    await bot.send_message(chat_id=chat_id, text=words_list[0].word.send_word)


async def calculate_time(t: float, user_id: int) -> str:
    offset = (await Users.find_one(Users.user_id == user_id)).time_offset
    if offset is None:
        offset = 0
    return time.strftime(TIME_FORMAT, time.localtime(t + 3600 * offset))
