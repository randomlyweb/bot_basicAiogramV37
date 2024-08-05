import datetime

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from core.utils.quizes_utils import (generate_quizes,
                                     generate_date)
from core.keyboards.client_kb import (filter_kb,
                                      return_to_choose_th,
                                      return_to_choose_quizes,
                                      return_to_filter_by_locations,
                                      return_to_filter_by_quizes,
                                      return_to_filter_by_categories,
                                      return_to_start,
                                      paginator)
from core.db.db import (select_all_rows_with_category,
                        select_location_by_id,
                        select_rows_with_need_date,
                        select_rows_for_tomorrow,
                        select_rows_for_week,
                        select_rows_for_need_day,
                        select_all_quizes_for_location,
                        select_all_quizes_for_quiz,
                        select_quiz_name_by_id,

                        select_all_quizes_,
                        select_all_locations,
                        )
from core.states.client_states import TimeState

router = Router()


@router.message(Command('quizes'))
async def show_quizes_f(message: Message):
    pass


@router.callback_query(F.data == 'timetable')
async def shkdfksdf(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.delete()
    await call.message.answer(text='Привет! Добро пожаловать в бота для просмотра актуальных квизов', reply_markup=filter_kb())


@router.callback_query(F.data.startswith('filter'))
async def akdk(call: CallbackQuery, state: FSMContext):
    type_ = call.data.split(':')[1]

    if type_ == 'by_categories':
        await call.message.edit_text(text='Привет! Добро пожаловать в бота для просмотра актуальных квизов', reply_markup=await paginator(router, 'categories'))

    elif type_ == 'by_locations':
        await call.message.edit_text(text='Привет! Добро пожаловать в бота для просмотра актуальных квизов', reply_markup=await paginator(router, 'locations'))

    elif type_ == 'by_quizes':
        await call.message.edit_text(text='Привет! Добро пожаловать в бота для просмотра актуальных квизов', reply_markup=await paginator(router, 'quizes'))

    elif type_ == 'today':

        text = 'Квизы на сегодня\n'
        rows = await select_rows_with_need_date()

        if not rows:
            text += f'Пока что на сегодня нету квизов!'
            await call.message.edit_text(text=text, reply_markup=return_to_choose_quizes())
        else:
            await call.message.edit_text(text='Ожидайте! Квизы загружаются', reply_markup=return_to_choose_quizes())
            txt = await generate_quizes(rows)
            text += txt
            try:
                await call.message.edit_text(text=text, reply_markup=return_to_choose_quizes())
            except TelegramBadRequest:
                print('Сообщение было удалено прежде, чем мы его изменили!')

    elif type_ == 'tomorrow':

        text = 'Квизы на завтра\n'
        rows = await select_rows_for_tomorrow()

        if not rows:
            text += f'Пока что на завтра нету квизов!'
            await call.message.edit_text(text=text, reply_markup=return_to_choose_quizes())
        else:
            await call.message.edit_text(text='Ожидайте! Квизы загружаются', reply_markup=return_to_choose_quizes())
            txt = await generate_quizes(rows)
            text += txt
            try:
                await call.message.edit_text(text=text, reply_markup=return_to_choose_quizes())
            except TelegramBadRequest:
                print('Сообщение было удалено прежде, чем мы его изменили!')

    elif type_ == 'week':

        text = 'Квизы на неделю\n'
        rows = await select_rows_for_week()

        if not rows:
            text += f'Пока что на этой неделе нету квизов!'
            await call.message.edit_text(text=text, reply_markup=return_to_choose_quizes())
        else:
            await call.message.edit_text(text='Ожидайте! Квизы загружаются', reply_markup=return_to_choose_quizes())
            txt = await generate_quizes(rows)
            text += txt
            try:
                await call.message.edit_text(text=text, reply_markup=return_to_choose_quizes())
            except TelegramBadRequest:
                print('Сообщение было удалено прежде, чем мы его изменили!')

    elif type_ == 'input':
        await call.message.edit_text(text='<i>Введите дату в таком формате YYYY-MM-DD</i>\n\n'
                                          '<blockquote>где YYYY - год\n'
                                          'где MM - месяц\n'
                                          'где DD - день</blockquote>', reply_markup=return_to_choose_quizes())
        await state.set_state(TimeState.time)
        await state.update_data(f=call.message.message_id)


@router.message(TimeState.time)
async def ofjsdfjs(message: Message, state: FSMContext):
    await state.update_data(time=message.text)
    data = await state.get_data()
    await state.clear()

    await message.bot.delete_message(chat_id=message.from_user.id, message_id=data['f'])

    yyyy = str(data['time']).split('-')[0]
    mm = str(data['time']).split('-')[1]
    dd = str(data['time']).split('-')[2]

    dt = await generate_date(mm, dd)

    general_text = f'Квизы на {dt}\n'

    rows = await select_rows_for_need_day(yyyy, mm, dd)

    if not rows:
        general_text += f'Пока что на {dt} нету квизов!'

        txt = await generate_quizes(rows)
        general_text += txt

        await message.answer(text=general_text, reply_markup=return_to_choose_quizes())


@router.callback_query(F.data.startswith('all'))
async def aksldkas(call: CallbackQuery):
    type_ = call.data.split(':')[1]

    if type_ == 'q':
        general_text = 'Все квизы\n\n'
        rows = await select_all_quizes_()
        for row in rows:
            general_text += f'- <a href="{row["link"]}">{row["name"]}</a>\n'

        await call.message.edit_text(text=general_text, reply_markup=return_to_start(), disable_web_page_preview=True)

    elif type_ == 'l':
        general_text = 'Все локации\n\n'
        rows = await select_all_locations()
        for row in rows:
            general_text += f'- <a href="{row["link"]}">{row["name"]}</a> ({row["address"]})\n'

        await call.message.edit_text(text=general_text, reply_markup=return_to_start(), disable_web_page_preview=True)


@router.callback_query(F.data.startswith('locations_open'))
async def asllasd(call: CallbackQuery):
    location_id = int(call.data.split(':')[1])
    location_name = await select_location_by_id(location_id)
    rows = await select_all_quizes_for_location(location_id)
    text = f'Все квизы {location_name[0]["name"]}\n\n'

    if not rows:
        text += f'Пока-что, в выбранной вами локации нету квизов!'
        await call.message.edit_text(text=text, reply_markup=return_to_choose_quizes())
    else:
        await call.message.edit_text(text='Ожидайте! Квизы загружаются', reply_markup=return_to_choose_quizes())
        txt = await generate_quizes(rows)
        text += txt
        try:
            await call.message.edit_text(text=text, reply_markup=return_to_choose_quizes())
        except TelegramBadRequest:
            print('Сообщение было удалено прежде, чем мы его изменили!')


@router.callback_query(F.data.startswith('quizes_open'))
async def asllasd(call: CallbackQuery):
    quiz_id = int(call.data.split(':')[1])
    quiz_name = await select_quiz_name_by_id(quiz_id)
    rows = await select_all_quizes_for_quiz(quiz_id)
    text = f'Все квизы {quiz_name[0]["name"]}\n\n'

    if not rows:
        text += f'Пока-что, нету квизов!'
        await call.message.edit_text(text=text, reply_markup=return_to_choose_quizes())
    else:
        await call.message.edit_text(text='Ожидайте! Квизы загружаются', reply_markup=return_to_choose_quizes())
        txt = await generate_quizes(rows)
        text += txt
        try:
            await call.message.edit_text(text=text, reply_markup=return_to_choose_quizes())
        except TelegramBadRequest:
            print('Сообщение было удалено прежде, чем мы его изменили!')