from bot.utils.texts import create_text
from loguru import logger
from bot.loader import bot, scheduler, router


async def scheduler_send(chat_id, scheduler_type, nums):
    """Привет, ты готов пройти свой ежедневный тест?"""
    await bot.send_message(chat_id=chat_id, text=scheduler_type + ' ' + str(nums))

# def scheduler_send() -> None:
#     # await bot.send_message(808952280, text='test')
#     print('aasdasfdasfa')
#     logger.info('test test test test test test test')


# @router.callback_query(F.data == 'change_scheduler')
# async def change_scheduler(call: types.CallbackQuery, state: FSMContext) -> None:
#     jobs = scheduler.get_jobs()
#     if len(jobs) > 1:
#         logger.error("Too many jobs scheduled")
#         exit(-1)
#     if jobs:
#         scheduler.remove_job(job_id=jobs[0].id, jobstore=None)
#         await bot.send_message(call.message.chat.id, text='job removed')
#     elif not jobs:
#         scheduler.add_job(func=scheduler_send, trigger="interval", seconds=3, name='main_scheduler_job')
#         # scheduler.add_job(scheduler_send, "cron", hour=18, minute=22)
#         await bot.send_message(call.message.chat.id, text='job added')
