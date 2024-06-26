from aiogram import types, F
from aiogram.fsm.context import FSMContext
from beanie.operators import In
from bson import ObjectId
from loguru import logger
import time

from bot.loader import bot, dp, router
from bot.utils.keyboards import create_keyboard
from bot.utils.models import UserWord, UserTests, Users
from bot.utils.states import User_state
from bot.utils.system import start_test, calculate_time
from bot.utils.texts import create_text, rnd_w_list


@router.callback_query(F.data == 'one_emphasis')
async def emphasis_start(call: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(User_state.answering_emphasis_words)
    await call.message.answer((await rnd_w_list(k=1))[0].send_word)
    await call.answer()


@router.callback_query(F.data == 'do_test')
async def test_question(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer(text=await create_text('test_question'), reply_markup=create_keyboard('test_question'))
    await state.set_state(User_state.chose_length_test)
    await call.answer()


@router.callback_query(F.data == 'do_test5')
async def test_start(call: types.CallbackQuery, state: FSMContext) -> None:
    print(call.message.text, call.message.from_user.id, call.message.chat.id)
    await state.set_state(User_state.answering_emphasis_test)
    await start_test(5, call.message.chat.id, call.message.chat.id)
    await call.answer()


@router.callback_query(F.data == 'do_test10')
async def test_start(call: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(User_state.answering_emphasis_test)
    await start_test(10, call.message.chat.id, call.message.chat.id)
    await call.answer()


@router.callback_query(F.data == 'do_test25')
async def test_start(call: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(User_state.answering_emphasis_test)
    await start_test(25, call.message.chat.id, call.message.chat.id)
    await call.answer()


@router.callback_query(F.data == 'see_progress')
async def see_progress(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text=await create_text('see_progress'), reply_markup=create_keyboard('see_progress'))
    await call.answer()


@router.callback_query(F.data == 'progress_wrong_words')
async def progress_wrong_words(call: types.CallbackQuery, state: FSMContext) -> None:
    data = await UserWord.find_many(UserWord.user_id == call.message.chat.id, UserWord.success == False).to_list()
    if not data:
        await call.message.answer(text=await create_text('no_progress'))
        return
    st = '(правильное) (неправильное) (время)'
    for i in data:
        if not i.success:
            st += '\n' + str(i.word.right_word) + ' ' + str(i.word.send_word) + ' ' + await calculate_time(i.time,
                                                                                                           call.message.chat.id)
    await call.message.answer(text=st)
    await call.answer()


@router.callback_query(F.data == 'progress_right_words')
async def progress_right_words(call: types.CallbackQuery, state: FSMContext) -> None:
    data = await UserWord.find_many(UserWord.user_id == call.message.chat.id, UserWord.success == True).to_list()
    if not data:
        await call.message.answer(text=await create_text('no_progress'))
        return
    st = '\n\n(слово) (время)'
    for i in data:
        if i.success:
            st += '\n' + str(i.word.send_word) + ' ' + str(i.word.send_word) + ' ' + await calculate_time(i.time,
                                                                                                          call.message.chat.id)
    await call.message.answer(text=st)
    await call.answer()


# @router.callback_query(F.data == 'progress_tests')
# async def progress_tests(call: types.CallbackQuery, state: FSMContext) -> None:
#     print('tteteee')
#     data = await UserTests.find_many(
#         UserTests.user_id == call.message.chat.id and UserTests.stage == -1).to_list()
#     print(data)
#     if not data:
#         call.message.answer(text=await create_text('no_progress'))
#         return
#     st = '\n\n(процент верных слов) (сколько всего слов) (время) (сколько секунд длился тест)'
#     for i in range(len(data)):
#         count_right, count_wrong = 0, 0
#         for j in data[i].words:
#             if j.success:
#                 count_right += 1
#             else:
#                 count_wrong += 1
#         st += '\n' + str(i + 1) + ': ' + str(round(count_right * 100 / (count_wrong + count_right))) + '% ' + str(
#             count_right + count_wrong) + ' ' + await calculate_time(data[i].time_start,
#                                                                     call.message.chat.id) + " " + str(round(
#             data[i].time_end - data[i].time_start))
#
#     await call.message.answer(text=st)
#     await call.answer()

@router.callback_query(F.data == 'chose_test')
async def chose_test(call: types.CallbackQuery, state: FSMContext) -> None:
    number_tests = await UserTests.find_many(
        UserTests.user_id == call.message.chat.id and UserTests.stage == -1).to_list()
    # NUMS_IN_LINE = 4
    # keyboard = []
    # for i in range(number_tests // NUMS_IN_LINE):
    #     lst = []
    #     for j in range(NUMS_IN_LINE):
    #         n = i*NUMS_IN_LINE + j + 1
    #         lst.append(types.InlineKeyboardButton(text=str(n), callback_data='progress_numtest_{}'.format(n)))
    #     keyboard.append(lst)
    # lst = []
    # for i in range(number_tests % NUMS_IN_LINE):
    #     n = number_tests - number_tests % NUMS_IN_LINE + i + 1
    #     lst.append(types.InlineKeyboardButton(text=str(n), callback_data='progress_numtest_{}'.format(n)))
    # keyboard.append(lst)
    keyboard = []
    for i in range(len(number_tests)):
        t = str(i + 1) + ': ' + await calculate_time(number_tests[i].time_start, call.message.chat.id)
        keyboard.append(
            [types.InlineKeyboardButton(text=t, callback_data='progress_numtest_{}'.format(number_tests[i].id))])
    print(keyboard)
    await call.message.answer(text=await create_text('chose_test'),
                              reply_markup=types.InlineKeyboardMarkup(inline_keyboard=keyboard))


@router.callback_query(F.data.startswith('progress_numtest'))
async def progress_test(call: types.CallbackQuery, state: FSMContext) -> None:
    data = await UserTests.find_one(UserTests.id == ObjectId(call.data[17:]))
    if not data:
        await call.message.answer(text=await create_text('no_progress'))
        return

    st = ''
    if any(not i.success for i in data.words):
        st += '(правильное) (неправильное) (время)'
        for i in data.words:
            if not i.success:
                st += '\n' + str(i.word.right_word) + ' ' + str(i.word.send_word) + ' ' + await calculate_time(i.time,
                                                                                                               call.message.chat.id)

    if any(i.success for i in data.words):
        st += '\n\n(слово) (время)'
        for i in data.words:
            if i.success:
                st += '\n' + str(i.word.send_word) + ' ' + str(i.word.send_word) + ' ' + await calculate_time(i.time,
                                                                                                              call.message.chat.id)
    count_right, count_wrong = 0, 0
    for j in data.words:
        if j.success:
            count_right += 1
        else:
            count_wrong += 1
    st += '\n\nСтатистика по тесту: процент верных слов' + str(
        round(count_right * 100 / (count_wrong + count_right))) + '% ' + "Всего слов: " + str(
        count_right + count_wrong) + 'Время: ' + await calculate_time(data.time_start,
                                                                      call.message.chat.id) + ", тест решён за " + str(
        round(data.time_end - data.time_start)) + " секунд"
    await call.message.answer(text=st)
    await call.answer()


@router.callback_query(F.data == 'see_all_progress')
async def see_all_progress(call: types.CallbackQuery, state: FSMContext) -> None:
    data_words_wrong = await UserWord.find_many(UserWord.user_id == call.message.chat.id,
                                                UserWord.success == False).to_list()
    st = ''
    if data_words_wrong:
        st += '(правильное) (неправильное) (время)'
        for i in data_words_wrong:
            if not i.success:
                st += '\n' + str(i.word.right_word) + ' ' + str(i.word.send_word) + ' ' + await calculate_time(i.time,
                                                                                                               call.message.chat.id)

    data_words_right = await UserWord.find_many(UserWord.user_id == call.message.chat.id,
                                                UserWord.success == True).to_list()
    if data_words_right:
        st += '\n\n(слово) (время)'
        for i in data_words_right:
            if i.success:
                st += '\n' + str(i.word.send_word) + ' ' + str(i.word.send_word) + ' ' + await calculate_time(i.time,
                                                                                                              call.message.chat.id)
    data_tests = await UserTests.find_many(
        UserTests.user_id == call.message.chat.id and UserTests.stage == -1).to_list()
    if data_tests:
        st += '\n\n(процент верных слов) (сколько всего слов) (время) (сколько секунд длился тест)'
        for i in range(len(data_tests)):
            count_right, count_wrong = 0, 0
            for j in data_tests[i].words:
                if j.success:
                    count_right += 1
                else:
                    count_wrong += 1
            st += '\n' + str(i + 1) + ': ' + str(round(count_right * 100 / (count_wrong + count_right))) + '% ' + str(
                count_right + count_wrong) + ' ' + await calculate_time(data_tests[i].time_start,
                                                                        call.message.chat.id) + " " + str(round(
                data_tests[i].time_end - data_tests[i].time_start))
    if not st:
        st = await create_text('no_progress')
    await call.message.answer(text=st)
    await call.answer()
