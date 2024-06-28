from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.loader import router, dp, bot, LOCAL_TIME, scheduler
from loguru import logger

from bot.utils.keyboards import create_keyboard
from bot.utils.models import Word, UserWord, UserTests, Users
from bot.utils.scheduler import scheduler_send
from bot.utils.system import start_test
from bot.utils.texts import rnd_w_list, create_text
import time


#
class User_state(StatesGroup):
    answering_emphasis_words = State()
    answering_emphasis_test = State()
    chose_length_test = State()
    change_glob_time = State()
    add_scheduler_time = State()
    add_scheduler_nums = State()

    # change_scheduler = State()
    # add_scheduler_USE_number = State()
    # add_scheduler_test_length = State()
    # chill = State()


@router.message(User_state.answering_emphasis_words, F.text)
async def emphasis_answer(message: types.Message, state: FSMContext) -> None:
    if not await Word.find_one(Word.send_word == message.text.lower()):
        await bot.send_message(chat_id=message.chat.id, text='напиши нормально. я не понимаю')  # TODO: text
        return

    await state.clear()
    if not await Word.find_one(Word.right_word == message.text):
        await bot.send_message(chat_id=message.chat.id, text='ты лох, не так надо')  # TODO: text
        success = False
    else:
        await bot.send_message(chat_id=message.chat.id, text='всё круто')  # TODO: text
        success = True
    right_w = (await Word.find_one(Word.send_word == message.text.lower())).right_word
    await bot.send_message(chat_id=message.chat.id, text=(await rnd_w_list(k=1))[0].send_word)
    data = UserWord(user_id=message.from_user.id, success=success, time=time.time(),
                    word=Word(send_word=message.text, right_word=right_w))  # TODO change time()
    await UserWord.insert(data)


@router.message(User_state.chose_length_test, F.text)
async def manage_start_test(message: types.Message, state: FSMContext):
    await state.set_state(User_state.answering_emphasis_test)
    if not message.text.isdigit() or int(message.text) < 2:
        await bot.send_message(chat_id=message.chat.id, text='всё плохо')  # TODO: text
        return
    await start_test(int(message.text), message.chat.id, message.from_user.id)
    print(await state.get_state())


@router.message(User_state.answering_emphasis_test, F.text)
async def test_answer(message: types.Message, state: FSMContext):
    data = await UserTests.find_one(UserTests.user_id == int(message.from_user.id), UserTests.stage >= 0)
    if data is None:
        print(message.from_user.id)
        print(data)
        await bot.send_message(chat_id=message.chat.id, text='no test')  # TODO: text
        return

    if data.stage < 0 or data.stage == len(data.words) or data.words[data.stage].word.send_word != message.text.lower():
        await bot.send_message(chat_id=message.chat.id, text='напиши нормально. я не понимаю')  # TODO: text
        print(data.words[data.stage].word.send_word, message.text.lower())
        return

    if data.words[data.stage].word.right_word != message.text:
        await bot.send_message(chat_id=message.chat.id, text='ты лох, не так надо')  # TODO: remove
        data.words[data.stage].success = False
        data.words[data.stage].word.send_word = message.text
        data.words[data.stage].time = time.time()  # TODO change time()
    else:
        await bot.send_message(chat_id=message.chat.id, text='всё круто')  # TODO: remove
        data.words[data.stage].success = True
        data.words[data.stage].time = time.time()  # TODO change time()
    data.stage += 1
    if data.stage < len(data.words):  # это не было последнее слово в тесте
        await bot.send_message(chat_id=message.chat.id, text=data.words[data.stage].word.send_word)
        print(data)
        await UserTests.save(data)
        return

    # это было последнее слово в тесте, пишет результаты теста
    await state.clear()
    data.stage = -1
    data.time_end = time.time()
    await UserTests.save(data)

    await bot.send_message(chat_id=message.chat.id, text=create_text('finish_test'),
                           reply_markup=create_keyboard('start'))


@router.message(User_state.change_glob_time, F.text)
async def change_glob_time(message: types.Message, state: FSMContext) -> None:
    if not message.text.isdigit() or int(message.text) > 24 or int(message.text) < -24:
        await bot.send_message(chat_id=message.chat.id, text='baaad')  # TODO: text
        return
    await state.clear()
    data = await Users.find_one(Users.user_id == message.chat.id)
    data.time_offset = int(message.text) - LOCAL_TIME
    await UserTests.save(data)
    await bot.send_message(chat_id=message.chat.id, text=await create_text('time_was_set'))


@router.message(User_state.add_scheduler_time, F.text)
async def add_scheduler(message: types.Message, state: FSMContext) -> None:
    if not ':' in message.text:
        await bot.send_message(message.from_user.id, create_text('chose_scheduler_time_error'))
        return

    hour, minute = message.text.split(':')
    if (not hour) or (not minute) or (not hour.isdigit()) or (not minute.isdigit()) or (
            int(hour) >= 24 or int(hour) <= -1) or (int(minute) >= 60 or int(minute) <= -1):
        await bot.send_message(message.from_user.id, create_text('chose_scheduler_time_error'))
        return
    await state.update_data(time_hour=int(hour), time_minute=int(minute))
    await bot.send_message(message.chat.id, text=await create_text('chose_scheduler_type'),
                           reply_markup=create_keyboard('chose_scheduler_type'))


@router.message(User_state.add_scheduler_nums, F.text)
async def add_scheduler(message: types.Message, state: FSMContext) -> None:
    if not message.text.isdigit() or int(message.text) < 1:
        await bot.send_message(message.chat.id, text='fuck', )  # TODO text
        return
    data = await state.get_data()
    if (not 'time_hour' in data.keys()) or (not 'time_minute' in data.keys()) or (not 'scheduler_type' in data.keys()):
        await state.clear()
        await bot.send_message(message.chat.id, text='fuck')  # TODO text
        return
    scheduler.add_job(func=scheduler_send, name='job_tmp_name', trigger="cron", hour=data['time_hour'],
                      minute=data['time_minute'],
                      args=[message.chat.id, data['scheduler_type'], int(message.text)])
    await bot.send_message(chat_id=message.chat.id, text='schedule was set')  # TODO text
    await state.clear()
    # scheduler.add_job(func=scheduler_send, trigger="interval", seconds=3, name='main_scheduler_job')
    #         # scheduler.add_job(scheduler_send, "cron", hour=18, minute=22)
    # print(await state.get_state())
    # print(await state.get_data())
    # await state.clear()
    # print(await state.get_data())
