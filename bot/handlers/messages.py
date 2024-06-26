from aiogram import types, F
from aiogram.fsm.context import FSMContext
from loguru import logger

from bot.utils import states as st
from bot.utils.keyboards import create_keyboard
from bot.utils.texts import create_text
from bot.loader import router, BOT_PASS

# This handler will be called when user sends 'hello' message to the bot
@router.message(F.text == BOT_PASS)
async def start(message: types.Message):
    # Log that user sends hello to the bot
    logger.info(f"User {message.from_user.id} sends hello to the bot")
    # create_text('hello') will return text from texts.json file
    # create_keyboard('hello') will return keyboard from keyboards.json file
    await message.answer(
        await create_text('tmp'),
    )

@router.message()
async def com_not_found(message: types.Message):
    await message.answer(
        await create_text('com_not_found'), reply_markup=create_keyboard('start')
    )