from aiogram import types, F
from aiogram.fsm.context import FSMContext
from loguru import logger

from bot.utils import states as st
from bot.utils.keyboards import create_keyboard
from bot.utils.texts import create_text
from bot.loader import router, BOT_PASS, ADMINS


@router.message(F.text == BOT_PASS)
async def start(message: types.Message):
    if not str(message.from_user.id) in list(ADMINS.replace(' ', '').split(',')):
        logger.info('try admin')
        return
    logger.info('admin logged in')
    await message.answer(
        await create_text('admin'), reply_markup=create_keyboard('admin'),
    )


@router.message()
async def com_not_found(message: types.Message):
    await message.answer(
        await create_text('com_not_found'), reply_markup=create_keyboard('start')
    )
