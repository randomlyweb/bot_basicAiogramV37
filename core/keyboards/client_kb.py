from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton, InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from aiogram_widgets.pagination import KeyboardPaginator


from core.db.db import select_all_categories, select_all_places, select_all_quizes_


def start_kb() -> InlineKeyboardMarkup:
    kb = [
        [InlineKeyboardButton(text='Расписание', callback_data='timetable'), InlineKeyboardButton(text='Группа', url='t.me/quiz_almaty/')],
        [InlineKeyboardButton(text='Все квизы', callback_data='all:q'), InlineKeyboardButton(text='Чат', url='t.me/quiz_kz_chat')],
        [InlineKeyboardButton(text='Все локации', callback_data='all:l'), InlineKeyboardButton(text='Связаться с нами', url='t.me/paks13')]
    ]

    kb_ = InlineKeyboardMarkup(inline_keyboard=kb)

    return kb_


def filter_kb() -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(text='На сегодня', callback_data='filter:today'),
            #InlineKeyboardButton(text='По тематикам', callback_data='filter:by_categories')
        ],
        [
            InlineKeyboardButton(text='Завтра', callback_data='filter:tomorrow'),
            InlineKeyboardButton(text='По локациям', callback_data='filter:by_locations')
        ],
        [
            InlineKeyboardButton(text='Неделю', callback_data='filter:week'),
            InlineKeyboardButton(text='По квизам', callback_data='filter:by_quizes')
        ],
        # [
        #     InlineKeyboardButton(text='Точная дата', callback_data='filter:input')
        # ],
        [
            InlineKeyboardButton(text='Назад', callback_data='start')
        ]
    ]

    kb_ = InlineKeyboardMarkup(inline_keyboard=kb)
    return kb_


async def generate_thematics() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    themes = await select_all_categories()
    for th in themes:
        kb.button(text=th['name'], callback_data=f'open_th:{th["id"]}')

    kb.button(text='Назад', callback_data='timetable')

    kb.adjust(2)
    return kb.as_markup()


def return_to_choose_th() -> InlineKeyboardMarkup:
    kb = [
        [InlineKeyboardButton(text='Назад', callback_data='filter:by_categories')]
    ]

    kb_ = InlineKeyboardMarkup(inline_keyboard=kb)

    return kb_


def return_to_choose_quizes() -> InlineKeyboardMarkup:
    kb = [
        [InlineKeyboardButton(text='Назад', callback_data='timetable')]
    ]

    kb_ = InlineKeyboardMarkup(inline_keyboard=kb)

    return kb_


def return_to_filter_by_locations():
    kb = InlineKeyboardBuilder()
    kb.button(text='Назад', callback_data='filter:by_locations')
    return kb.as_markup()


def return_to_filter_by_quizes():
    kb = InlineKeyboardBuilder()
    kb.button(text='Назад', callback_data='filter:by_quizes')
    return kb.as_markup()


def return_to_filter_by_categories():
    kb = InlineKeyboardBuilder()
    kb.button(text='Назад', callback_data='filter:by_categories')
    return kb.as_markup()


def return_to_start():
    kb = InlineKeyboardBuilder()
    kb.button(text='Назад', callback_data='start')
    return kb.as_markup()


async def paginator(router, type_):
    if type_ == 'locations':
        data = await select_all_places()
        buttons = []
        additional_buttons = [
            [
                InlineKeyboardButton(text="Назад 🔙", callback_data="start"),
            ]
        ]
        for i in data:
            code = i['id']
            name = i['name']
            buttons.append(InlineKeyboardButton(text=name, callback_data=f'locations_open:{code}'))
        paginator = KeyboardPaginator(data=buttons, per_page=5, per_row=2, router=router, additional_buttons=additional_buttons)

        return paginator.as_markup()

    if type_ == 'quizes':
        data = await select_all_quizes_()
        buttons_q = []
        additional_buttons = [
            [
                InlineKeyboardButton(text="Назад 🔙", callback_data="start"),
            ]
        ]
        for i in data:
            code = i['id']
            name = i['name']
            buttons_q.append(InlineKeyboardButton(text=name, callback_data=f'quizes_open:{code}'))
        paginator = KeyboardPaginator(data=buttons_q, per_page=5, per_row=2, router=router,
                                      additional_buttons=additional_buttons)

        return paginator.as_markup()