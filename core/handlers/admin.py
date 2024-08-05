import re
from datetime import datetime
from collections import defaultdict

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from asyncpg.exceptions import UniqueViolationError

from core.keyboards.admin_kb import admin_kb, menu_add_kb, return_to_admin, return_to_menu, apaginator, edit_kb, a_paginator, variant_kb, return_to_vubor, quiz_paginator, \
quiz_delete_kb
from core.states.admin_states import LocationState, QuizState, CategoryState, RePeakState, ChoiceState, ReWriteQuizName, ReWriteLocation
from core.db.db import add_location_if_not_exists, add_quiz_if_not_exists, add_category_if_not_exists, \
    select_all_quizes_for_location, select_location_by_id, select_all_quizes_for_quiz, select_quiz_name_by_id, \
    select_quiz_name_by_name, select_location_name_by_name, add_quiz, check_for_quiz, edit_quiz, delete_quiz_name, delete_location, edit_location, select_quiz_by_id, \
    delete_quiz
from config import ADMIN_IDS, NEW_ADMINS
from core.utils.quizes_utils import generate_quizes, generate_quiz_by_
from core.utils.parsing import get_wowquiz, get_club60sec, get_quizium, get_quizplease, get_quizyasha, parse_schedule, clean_input_data

router = Router()


@router.message(Command('admin'))
async def show_admin_panel(message: Message, state: FSMContext):
    await state.clear()
    if (message.from_user.id in ADMIN_IDS) or (message.from_user.id in NEW_ADMINS):
        await message.answer('Здравствуйте! Вы в админ панели',
                             reply_markup=admin_kb())


@router.callback_query(F.data == 'admin')
async def askjdask(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.delete()
    if (call.from_user.id in ADMIN_IDS) or (call.from_user.id in NEW_ADMINS):
        await call.message.answer(text='Здравствуйте! Вы в админ панели',
                                  reply_markup=admin_kb())


@router.callback_query(F.data == 'menu_add')
async def askdka(call: CallbackQuery, state: FSMContext):
    await state.clear()
    if (call.from_user.id in ADMIN_IDS) or (call.from_user.id in NEW_ADMINS):
        await call.message.delete()
        await call.message.answer(text='второй уровень панели',
                                     reply_markup=menu_add_kb(call.from_user.id))


@router.callback_query(F.data.startswith('admin_add'))
async def skadkas(call: CallbackQuery, state: FSMContext):
    if (call.from_user.id in ADMIN_IDS) or (call.from_user.id in NEW_ADMINS):
        type_ = call.data.split(':')[1]
        if type_ == 'location':
            await call.message.edit_text(text='Вы в меню добавления локации\n\n'
                                              '<i>Введите название локации</i>',
                                         reply_markup=return_to_menu())
            await state.set_state(LocationState.name)
            await state.update_data(msg=call.message.message_id)

        elif type_ == 'category':
            await call.message.edit_text(text='Вы в меню добавления тематики\n\n'
                                              '<i>Введите название тематики</i>',
                                         reply_markup=return_to_menu())
            await state.set_state(CategoryState.name)
            await state.update_data(msg=call.message.message_id)

        elif type_ == 'quiz':
            await call.message.edit_text(text='Вы в меню добавления квиза\n\n'
                                              '<i>Введите название квиза</i>',
                                         reply_markup=return_to_menu())
            await state.set_state(QuizState.name)
            await state.update_data(msg=call.message.message_id)

        elif type_ == 'quiz_add':
            await call.message.edit_text(text='здесь пока-что пусто', reply_markup=return_to_menu())

        elif type_ == 'parse':
            await call.message.edit_text(text='Проводим парсинг! Подождите чуть-чуть')

            parsing_data = []

            wowquiz = get_wowquiz()
            for w in wowquiz:
                quiz_name = 'Wow Quiz'
                quiz_date = w['date']
                quiz_title = w['title']
                quiz_place = w['place']
                quiz_time = w['time']

                time_string = f'{quiz_date} {quiz_time}'
                string = f'{quiz_name}:{quiz_title}:{quiz_place}/{time_string}'
                parsing_data.append(string)
            quizplease = get_quizplease()
            for qp in quizplease:
                quiz_name = 'Квиз, Плиз!'
                quiz_date = qp['date']
                quiz_title = qp['title']
                quiz_place = qp['place']
                quiz_time = qp['time']

                time_string = f'{quiz_date} {quiz_time}'
                string = f'{quiz_name}:{quiz_title}:{quiz_place}/{time_string}'
                parsing_data.append(string)
            quizyasha = get_quizyasha()
            for qz in quizyasha:
                quiz_name = 'Квизяша'
                quiz_date = qz['date']
                quiz_title = qz['title']
                quiz_place = qz['place']
                quiz_time = qz['time']

                time_string = f'{quiz_date} {quiz_time}'
                string = f'{quiz_name}:{quiz_title}:{quiz_place}/{time_string}'
                parsing_data.append(string)
            club60sec = get_club60sec()
            for cs in club60sec:
                quiz_name = 'Клуб "60 секунд"'
                quiz_date = cs['date']
                quiz_title = cs['title']
                quiz_place = cs['place']
                quiz_time = cs['time']

                time_string = f'{quiz_date} {quiz_time}'
                string = f'{quiz_name}:{quiz_title}:{quiz_place}/{time_string}'
                parsing_data.append(string)
            quizium = get_quizium()
            for qm in quizium:
                quiz_name = 'Квизиум'
                quiz_date = qm['date']
                quiz_title = qm['title']
                quiz_place = qm['place']
                quiz_time = qm['time']

                time_string = f'{quiz_date} {quiz_time}'
                string = f'{quiz_name}:{quiz_title}:{quiz_place}/{time_string}'
                parsing_data.append(string)

            data = await generate_quiz_by_(parsing_data)
            await call.message.edit_text(text=f'{data}\n\n'
                                              f'Для того, чтобы изменить какой-либо из квизов, скопируйте квиз(просто нажмите). Если всё нормально - напишите "<code>Всё нормально</code>"')
            await state.set_state(ChoiceState.choice)
            await state.update_data(parsing_data=data)


@router.message(ChoiceState.choice)
async def askdka(message: Message, state: FSMContext):
    await state.update_data(choice=message.text)
    data = await state.get_data()

    if str(data['choice']).lower() == str('Всё нормально').lower():
        counter = 0
        await state.clear()
        string_without_b_tags = re.sub(r'<\/?b>', '', data['parsing_data'])
        final_string = re.sub(r'<\/?code>', '', string_without_b_tags)
        cleaned_data = clean_input_data(final_string)
        q = parse_schedule(cleaned_data)
        for date, events in q.items():
            for event_name, event in events.items():
                data_part = str(event).split('/')
                name = str(data_part[0]).split(':')[0]
                categories = str(data_part[0]).split(':')[1]
                place = str(data_part[0]).split(':')[2]
                time = str(data_part[1])

                location_id = await select_location_name_by_name(place)
                quiz_id = await select_quiz_name_by_name(name)

                if location_id == [] or quiz_id == []:
                     print('Данных по локациям и квизам не найдено!')
                else:
                    status = await check_for_quiz(
                        location_id=location_id[0]["id"],
                        quiz_id=quiz_id[0]["id"],
                        year=int(str(date).split('-')[0]),
                        month=int(str(date).split('-')[1]),
                        day=int(str(date).split('-')[2]),
                        hours=int(str(time).split(':')[0]),
                        minutes=int(str(time).split(':')[1]),
                        tag=str(categories)
                    )
                    if status == False:
                        await add_quiz(
                            location_id=location_id[0]["id"],
                            quiz_id=quiz_id[0]["id"],
                            year=int(str(date).split('-')[0]),
                            month=int(str(date).split('-')[1]),
                            day=int(str(date).split('-')[2]),
                            hours=int(str(time).split(':')[0]),
                            minutes=int(str(time).split(':')[1]),
                            tag=str(categories)
                        )
                        counter += 1
                    else:
                        print('Такой квиз уже есть')
        await message.answer(f'Загружено {counter} квизов', reply_markup=return_to_menu())

    else:
        await state.set_state(ChoiceState.new_string)
        await message.reply('Отлично! Теперь, пожалуйста, перепишите этот квиз так, как вы хотели бы его видеть')


@router.message(ChoiceState.new_string)
async def lasdla(message: Message, state: FSMContext):
    await state.update_data(new_string=message.text)
    data = await state.get_data()
    await state.clear()

    quiz_str = data['choice']
    new_t = data['new_string']
    new_string = str(quiz_str).replace(quiz_str, new_t)
    parsing_data = data['parsing_data']
    new_data = str(parsing_data).replace(quiz_str, new_string)

    await message.answer(f'{new_data}\n\n'
                         f'Для того, чтобы изменить какой-либо из квизов, скопируйте квиз(просто нажмите). Если всё нормально - напишите "<code>Всё нормально</code>"')
    await state.set_state(ChoiceState.choice)
    await state.update_data(parsing_data=new_data)


@router.message(LocationState.name)
async def djejad(message: Message, state: FSMContext):
    if (message.from_user.id in ADMIN_IDS) or (message.from_user.id in NEW_ADMINS):
        await state.update_data(name=message.text)
        data = await state.get_data()
        try:
            await message.bot.delete_message(chat_id=message.from_user.id, message_id=data['msg'])
        except:
            pass
        msg = await message.answer('Теперь введите ссылку на локацию')
        await state.set_state(LocationState.link)
        await state.update_data(msg2=msg.message_id)


@router.message(LocationState.link)
async def asdasdadasd(message: Message, state: FSMContext):
    if (message.from_user.id in ADMIN_IDS) or (message.from_user.id in NEW_ADMINS):
        await state.update_data(link=message.text)
        data = await state.get_data()
        try:
            await message.bot.delete_message(chat_id=message.from_user.id, message_id=data['msg2'])
        except:
            pass
        msg = await message.answer('Теперь введите адрес локации')
        await state.set_state(LocationState.address)
        await state.update_data(msg3=msg.message_id)


@router.message(LocationState.address)
async def asdasasd(message: Message, state: FSMContext):
    if (message.from_user.id in ADMIN_IDS) or (message.from_user.id in NEW_ADMINS):
        await state.update_data(address=message.text)
        data = await state.get_data()
        await state.clear()

        try:
            await message.bot.delete_message(chat_id=message.from_user.id, message_id=data['msg3'])
        except:
            pass
        await add_location_if_not_exists(
            data['name'],
            data['link'],
            data['address']
        )
        await message.answer('Локация добавлена!', reply_markup=return_to_menu())


@router.message(QuizState.name)
async def djejaasdd(message: Message, state: FSMContext):
    if (message.from_user.id in ADMIN_IDS) or (message.from_user.id in NEW_ADMINS):
        await state.update_data(name=message.text)
        data = await state.get_data()
        try:
            await message.bot.delete_message(chat_id=message.from_user.id, message_id=data['msg'])
        except:
            pass

        msg = await message.answer('Теперь введите ссылку на квиз')
        await state.set_state(QuizState.link)
        await state.update_data(msg2=msg.message_id)


@router.message(QuizState.link)
async def asdasaasdasd(message: Message, state: FSMContext):
    if (message.from_user.id in ADMIN_IDS) or (message.from_user.id in NEW_ADMINS):
        await state.update_data(link=message.text)
        data = await state.get_data()
        await state.clear()

        try:
            await message.bot.delete_message(chat_id=message.from_user.id, message_id=data['msg2'])
        except:
            pass

        await add_quiz_if_not_exists(
            data['name'],
            data['link']
        )
        await message.answer('Название квиза добавлено!', reply_markup=return_to_menu())


@router.message(CategoryState.name)
async def djeasjaasdd(message: Message, state: FSMContext):
    if (message.from_user.id in ADMIN_IDS) or (message.from_user.id in NEW_ADMINS):
        await state.update_data(name=message.text)
        data = await state.get_data()
        await state.clear()

        try:
            await message.bot.delete_message(chat_id=message.from_user.id, message_id=data['msg'])
        except:
            pass
        try:
            await add_category_if_not_exists(data['name'])
            await message.answer('Тематика добавлена', reply_markup=return_to_menu())
        except UniqueViolationError:
            await message.answer('Тематика уже была создана! Выберите другое название', reply_markup=return_to_admin())


@router.callback_query(F.data.startswith('admin_show'))
async def sasdkadkas(call: CallbackQuery, state: FSMContext):
    if (call.from_user.id in ADMIN_IDS) or (call.from_user.id in NEW_ADMINS):
        type_ = call.data.split(':')[1]
        if type_ == 'locations':
            await call.message.edit_text(text='Вы в меню просмотра локаций\n\n',
                                         reply_markup=await apaginator(router, 'locations'))


        elif type_ == 'categories':
            await call.message.edit_text(text='Вы в меню просмотра тематик\n\n',
                                         reply_markup=await apaginator(router, 'categories'))


        elif type_ == 'quizes':
            await call.message.edit_text(text='Вы в меню просмора квизов\n\n',
                                         reply_markup=await apaginator(router, 'quizes'))


@router.message(Command('q'))
async def kasldkas(message: Message, state: FSMContext):
    await state.set_state(RePeakState.text)
    await message.answer('Перешлите сюда данные с расписанием')


@router.message(RePeakState.text)
async def skdka(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    await state.clear()
    cleaned_data = clean_input_data(data['text'])

    counter = 0

    months = {
        '01': 'января',
        '02': 'февраля',
        '03': 'марта',
        '04': 'апреля',
        '05': 'мая',
        '06': 'июня',
        '07': 'июля',
        '08': 'августа',
        '09': 'сентября',
        '10': 'октября',
        '11': 'ноября',
        '12': 'декабря'
    }

    def parse_event__(event_str):
        match = re.match(r"– (.*?) \[(.*?)\] - (.*?), (.*?)$", event_str.strip())
        if match:
            name, theme, time, location = match.groups()
            return f"{name}:{theme}:{location}/{time}"
        return None

    def convert_date__(date_str):
        day, month_name = date_str.split(' ')
        for month_num, month in months.items():
            if month == month_name:
                return datetime.strptime(f"2024-{month_num}-{day.zfill(2)}", "%Y-%m-%d").date()
        return None

    def parse_schedule__(data):
        schedule = defaultdict(dict)
        current_date = None

        for line in data.strip().split('\n'):
            if re.match(r"^\d+ \w+, ", line):
                date_str = line.split(',')[0]
                current_date = convert_date__(date_str)
            elif current_date:
                event = parse_event__(line)
                if event:
                    if current_date not in schedule:
                        schedule[current_date] = {}
                    schedule[current_date][event.split(':')[0].strip()] = event

        return schedule

    parsed_schedule = parse_schedule__(data['text'])
    for date, events in parsed_schedule.items():
        for event_name, event in events.items():
            data_part = str(event).split('/')
            name = str(data_part[0]).split(':')[0]
            categories = str(data_part[0]).split(':')[1]
            place = str(data_part[0]).split(':')[2]
            time = str(data_part[1])

            location_id = await select_location_name_by_name(place)
            quiz_id = await select_quiz_name_by_name(name)

            if location_id == [] or quiz_id == []:
                print('Данных по локациям и квизам не найдено!')
            else:
                status = await check_for_quiz(
                    location_id=location_id[0]["id"],
                    quiz_id=quiz_id[0]["id"],
                    year=int(str(date).split('-')[0]),
                    month=int(str(date).split('-')[1]),
                    day=int(str(date).split('-')[2]),
                    hours=int(str(time).split(':')[0]),
                    minutes=int(str(time).split(':')[1]),
                    tag=str(categories)
                )
                if status == False:
                    await add_quiz(
                        location_id=location_id[0]["id"],
                        quiz_id=quiz_id[0]["id"],
                        year=int(str(date).split('-')[0]),
                        month=int(str(date).split('-')[1]),
                        day=int(str(date).split('-')[2]),
                        hours=int(str(time).split(':')[0]),
                        minutes=int(str(time).split(':')[1]),
                        tag=str(categories)
                    )
                    counter += 1
                else:
                    print('Такой квиз уже есть')
    await message.answer(f'Загружено {counter} квизов', reply_markup=return_to_menu())


@router.callback_query(F.data.startswith('alocations_open'))
async def asllasd(call: CallbackQuery):
    location_id = int(call.data.split(':')[1])
    location_name = await select_location_by_id(location_id)
    rows = await select_all_quizes_for_location(location_id)
    text = f'Все квизы {location_name[0]["name"]}\n\n'

    if not rows:
        text += f'Пока-что, в выбранной вами локации нету квизов!'
        await call.message.edit_text(text=text, reply_markup=return_to_menu())
    else:
        await call.message.edit_text(text='Ожидайте! Квизы загружаются', reply_markup=return_to_menu())
        txt = await generate_quizes(rows)
        text += txt
        try:
            await call.message.edit_text(text=text, reply_markup=return_to_menu())
        except TelegramBadRequest:
            print('Сообщение было удалено прежде, чем мы его изменили!')


@router.callback_query(F.data.startswith('aquizes_open'))
async def asllasd(call: CallbackQuery):
    quiz_id = int(call.data.split(':')[1])
    quiz_name = await select_quiz_name_by_id(quiz_id)
    rows = await select_all_quizes_for_quiz(quiz_id)
    text = f'Все квизы {quiz_name[0]["name"]}\n\n'

    if not rows:
        text += f'Пока-что, нету квизов!'
        await call.message.edit_text(text=text, reply_markup=return_to_menu())
    else:
        await call.message.edit_text(text='Ожидайте! Квизы загружаются', reply_markup=return_to_menu())
        txt = await generate_quizes(rows)
        text += txt
        try:
            await call.message.edit_text(text=text, reply_markup=return_to_menu())
        except TelegramBadRequest:
            print('Сообщение было удалено прежде, чем мы его изменили!')


# MENU EDIT
@router.callback_query(F.data == 'menu_edit')
async def ldaslasdl(call: CallbackQuery):
    if (call.from_user.id in ADMIN_IDS) or (call.from_user.id in NEW_ADMINS):
        await call.message.delete()
        await call.message.answer('Выберите, что вы хотите изменить',
                                  reply_markup=edit_kb())


@router.callback_query(F.data.startswith('admin_edit'))
async def asldladlad(call: CallbackQuery):
    type_ = call.data.split(':')[1]
    if type_ == 'quiz_name':
        await call.message.edit_text(text='Выберите квиз, который хотите изменить',
                                     reply_markup=await a_paginator(router, 'quizes'))
    elif type_ == 'location':
        await call.message.edit_text(text='Выберите локацию, которую хотите изменить',
                                     reply_markup=await a_paginator(router, 'locations'))


@router.callback_query(F.data.startswith('aquizes_edit'))
async def alsdlada(call: CallbackQuery, state: FSMContext):
    await state.clear()
    quiz_id = int(call.data.split(':')[1])
    quiz_name = await select_quiz_name_by_id(quiz_id)

    text = (f'Квиз: {quiz_name[0]["name"]}\n\n'
            f'Выберите, что вы хотите с ним сделать')

    await call.message.edit_text(
        text=text,
        reply_markup=variant_kb(quiz_id, 'quiz')
    )


@router.callback_query(F.data.startswith('alocations_edit'))
async def alsdlada(call: CallbackQuery, state: FSMContext):
    await state.clear()
    location_id = int(call.data.split(':')[1])
    location_name = await select_location_by_id(location_id)

    text = (f'Локация: {location_name[0]["name"]}\n\n'
            f'Выберите, что вы хотите с ней сделать')

    await call.message.edit_text(
        text=text,
        reply_markup=variant_kb(location_id, 'location')
    )


@router.callback_query(F.data.startswith('admin_record'))
async def askakdaskd(call: CallbackQuery, state: FSMContext):
    type_ = call.data.split(':')[1]

    if type_ == 'quiz':
        action = call.data.split(':')[2]
        quiz_id = int(call.data.split(':')[3])
        if action == 'rewrite':
            await state.set_state(ReWriteQuizName.name)
            await call.message.delete()
            msg = await call.message.answer(text='Напишите <i>новое</i> название квиза',
                                         reply_markup=return_to_vubor(id_=quiz_id, type_='quiz'))
            await state.update_data(q_id=quiz_id)
            await state.update_data(msg=msg.message_id)
        elif action == 'delete':
            await delete_quiz_name(quiz_id)
            await call.message.answer('Квиз удалён!',
                                      reply_markup=return_to_admin())
    elif type_ == 'location':
        action = call.data.split(':')[2]
        location_id = int(call.data.split(':')[3])
        if action == 'rewrite':
            await state.set_state(ReWriteLocation.name)
            await call.message.delete()
            msg = await call.message.answer(text='Напишите <i>новое</i> название локации',
                                            reply_markup=return_to_vubor(id_=location_id, type_='location'))
            await state.update_data(l_id=location_id)
            await state.update_data(msg=msg.message_id)
        elif action == 'delete':
            await delete_location(location_id)
            await call.message.answer('Локация удалёна!',
                                      reply_markup=return_to_admin())


@router.message(ReWriteQuizName.name)
async def kasdkaasfdla(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    try:
        await message.bot.delete_message(chat_id=message.from_user.id, message_id=data['msg'])
    except:
        pass
    await message.delete()
    await state.set_state(ReWriteQuizName.link)
    msg = await message.answer(text='Теперь напишите <i>новую</i> ссылку на квиз')
    await state.update_data(msg2=msg.message_id)


@router.message(ReWriteQuizName.link)
async def aslasddaL(message: Message, state: FSMContext):
    await state.update_data(link=message.text)
    await message.delete()
    data = await state.get_data()
    await state.clear()

    try:
        await message.bot.delete_message(chat_id=message.from_user.id, message_id=data['msg2'])
    except:
        pass

    await edit_quiz(quiz_id=int(data['q_id']), new_quiz_name=data['name'], link=data['link'])

    await message.answer('Название квиза успешно изменено!',
                         reply_markup=return_to_admin())


@router.message(ReWriteLocation.name)
async def kasdsadfaws3kadla(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    try:
        await message.bot.delete_message(chat_id=message.from_user.id, message_id=data['msg'])
    except:
        pass
    await message.delete()
    await state.set_state(ReWriteLocation.link)
    msg = await message.answer(text='Теперь напишите <i>новую</i> ссылку на локацию')
    await state.update_data(msg2=msg.message_id)


@router.message(ReWriteLocation.link)
async def kaagasdkadla(message: Message, state: FSMContext):
    await state.update_data(link=message.text)
    data = await state.get_data()
    try:
        await message.bot.delete_message(chat_id=message.from_user.id, message_id=data['msg2'])
    except:
        pass
    await message.delete()
    await state.set_state(ReWriteLocation.address)
    msg = await message.answer(text='Теперь напишите <i>новый</i> адрес локации')
    await state.update_data(msg3=msg.message_id)


@router.message(ReWriteLocation.address)
async def asldasdfasfL(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.delete()
    data = await state.get_data()
    await state.clear()

    try:
        await message.bot.delete_message(chat_id=message.from_user.id, message_id=data['msg3'])
    except:
        pass

    await edit_location(location_id=data['l_id'], new_location_name=data['name'], link=data['link'], address=data['address'])

    await message.answer('Локация успешно изменена!',
                         reply_markup=return_to_admin())


@router.callback_query(F.data == 'menu_delete')
async def lasdlasdla(call: CallbackQuery):
    if (call.from_user.id in ADMIN_IDS) or (call.from_user.id in NEW_ADMINS):
        await call.message.edit_text(text='Выберите квиз из клавиатуры ниже, чтобы удалить',
                                     reply_markup=await quiz_paginator(router))


@router.callback_query(F.data.startswith('aquizes_delete'))
async def lasdflasflasflas(call: CallbackQuery):
    quiz_id = int(call.data.split(':')[1])
    rows = await select_quiz_by_id(quiz_id)
    general_text = f'Квиз <b>{rows[0]["tag"]}</b>\n\n'

    txt = await generate_quizes(rows)

    general_text += txt

    await call.message.edit_text(text=f'{general_text}\n\n'
                                      f'Для удаления квиза, воспользуйтесь клавиатурой ниже',
                                 reply_markup=quiz_delete_kb(quiz_id))


@router.callback_query(F.data.startswith('quiz_delete'))
async def asldalsda(call: CallbackQuery):
    quiz_id = int(call.data.split(':')[1])

    await delete_quiz(quiz_id)

    await call.message.edit_text(text='Квиз удалён!', reply_markup=return_to_admin())