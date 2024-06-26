from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandStart
from loguru import logger
from bot.loader import bot, dp, BOT_PASS, router
from bot.utils.keyboards import create_keyboard
from bot.utils.models import UserTests, Users
from bot.utils.states import User_state
from bot.utils.texts import create_text
from aiogram import F
from beanie.operators import In


# This handler will be called when user sends '/start' command to the bot
# @dp.message(CommandStart())
# async def com_start(message: types.Message):
#         c1 = types.BotCommand(command='test', description='Пройти тест')
#         c2 = types.BotCommand(command='repeat_wrong_words',
#                               description='Повторить слова в которых вы неверно поставили ударение')
#         c3 = types.BotCommand(command='stop_test', description='Остановить тест или повторение слов')
#         c4 = types.BotCommand(command='my_answers', description='Мои ответы')
#         # c5 = types.BotCommand(command='my_tests', description='Посмотреть результаты моих тестов')
#         c6 = types.BotCommand(command='help', description='Помощь по боту')
#
#         await bot.set_my_commands([c1, c2, c3, c4, c6])
#         await bot.set_chat_menu_button(message.chat.id, types.MenuButtonCommands('commands'))

@router.message(CommandStart())
@router.message(Command('help'))
@router.message(F.text == 'help')
async def com_help(message: types.Message):
    data = await Users.find_one(Users.user_id == message.from_user.id)
    if not data:
        data = Users(user_id=int(message.from_user.id), user_name=message.from_user.username, first_name=message.from_user.first_name, last_name=message.from_user.last_name, time_offset=0)
        await Users.insert(data)
    await message.answer(
        await create_text('start'), reply_markup=create_keyboard('start')
    )


@dp.message(Command('stop'), User_state.answering_emphasis_test)
@dp.message(Command('stop'), User_state.chose_length_test)
async def com_stop_test(message: types.Message, state: FSMContext):
    await UserTests.find_many(UserTests.user_id == message.from_user.id and UserTests.stage != -1).delete()
    await state.set_state(User_state.chill)
    await bot.send_message(chat_id=message.chat.id, text=await create_text('stop_test'), reply_markup='start')


@dp.message(Command('stop'), User_state.answering_emphasis_words)
async def com_stop_emphasis(message: types.Message, state: FSMContext):
    await state.set_state(User_state.chill)
    await bot.send_message(chat_id=message.chat.id, text=await create_text('stop'), reply_markup=create_keyboard('start'))
