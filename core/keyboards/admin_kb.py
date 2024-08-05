from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton, InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from aiogram_widgets.pagination import KeyboardPaginator


from config import NEW_ADMINS
from core.db.db import select_all_places, select_all_quizes_, select_all_quizes___


def admin_kb() -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(text='Меню добавления', callback_data='menu_add'),
            InlineKeyboardButton(text='Меню изменения', callback_data='menu_edit')
        ],
        [
            InlineKeyboardButton(text='Меню удаления', callback_data='menu_delete')
        ],
        [
            InlineKeyboardButton(text='В бота', callback_data='start')
        ]
    ]
    kb_ = InlineKeyboardMarkup(inline_keyboard=kb)
    return kb_


def menu_add_kb(telegram_id) -> InlineKeyboardMarkup:
    kb_for_general_admin = [
        [
            InlineKeyboardButton(text='Спарсить квизы', callback_data='admin_add:parse')
        ],
        [
            InlineKeyboardButton(text='Добавить локацию', callback_data='admin_add:location'),
            #InlineKeyboardButton(text='Добавить категорию', callback_data='admin_add:category')
        ],
        [
            InlineKeyboardButton(text='Добавить название квиза', callback_data='admin_add:quiz')
        ],
        [
            InlineKeyboardButton(text='Просмотреть локации', callback_data='admin_show:locations'),
            #InlineKeyboardButton(text='Просмотреть категории', callback_data='admin_show:categories')
        ],
        [
            InlineKeyboardButton(text='Просмотреть квизы', callback_data='admin_show:quizes')
        ],
        # [
        #     InlineKeyboardButton(text='Добавить квиз', callback_data='admin_add:quiz_add')
        # ],
        [
            InlineKeyboardButton(text='Назад', callback_data='admin')
        ]
    ]

    kb_for_not_general_admins = [
        [
            InlineKeyboardButton(text='Просмотреть локации', callback_data='admin_show:locations'),
            InlineKeyboardButton(text='Просмотреть категории', callback_data='admin_show:categories')
        ],
        [
            InlineKeyboardButton(text='Просмотреть квизы', callback_data='admin_show:quizes')
        ],
        [
            InlineKeyboardButton(text='Добавить название квиза', callback_data='admin_add:quiz_add')
        ],
        [
            InlineKeyboardButton(text='Назад', callback_data='admin')
        ]
    ]
    if not telegram_id in NEW_ADMINS:
        kb_ = InlineKeyboardMarkup(inline_keyboard=kb_for_general_admin)
    elif telegram_id in NEW_ADMINS:
        kb_ = InlineKeyboardMarkup(inline_keyboard=kb_for_not_general_admins)

    return kb_


def return_to_admin() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='Назад', callback_data='admin')
    return kb.as_markup()


def return_to_menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='Назад', callback_data='menu_add')
    return kb.as_markup()


async def apaginator(router, type_):
    if type_ == 'locations':
        data = await select_all_places()
        buttons = []
        additional_buttons = [
            [
                InlineKeyboardButton(text="Назад 🔙", callback_data="menu_add"),
            ]
        ]
        for i in data:
            code = i['id']
            name = i['name']
            buttons.append(InlineKeyboardButton(text=name, callback_data=f'alocations_open:{code}'))
        paginator = KeyboardPaginator(data=buttons, per_page=5, per_row=2, router=router, additional_buttons=additional_buttons)

        return paginator.as_markup()

    if type_ == 'quizes':
        data = await select_all_quizes_()
        buttons_q = []
        additional_buttons = [
            [
                InlineKeyboardButton(text="Назад 🔙", callback_data="menu_add"),
            ]
        ]
        for i in data:
            code = i['id']
            name = i['name']
            buttons_q.append(InlineKeyboardButton(text=name, callback_data=f'aquizes_open:{code}'))
        paginator = KeyboardPaginator(data=buttons_q, per_page=5, per_row=2, router=router,
                                      additional_buttons=additional_buttons)

        return paginator.as_markup()


def edit_kb():
    kb = [
        [
            InlineKeyboardButton(text='Изменить Название квиза', callback_data='admin_edit:quiz_name'),
            InlineKeyboardButton(text='Изменить локацию', callback_data='admin_edit:location')
        ],
        # [
            # InlineKeyboardButton(text='Изменить тематику')
        # ]
        [
            InlineKeyboardButton(text='Назад', callback_data='admin')
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


async def a_paginator(router, type_):
    if type_ == 'quizes':
        data = await select_all_quizes_()
        buttons_q = []
        additional_buttons = [
            [
                InlineKeyboardButton(text="Назад 🔙", callback_data="admin"),
            ]
        ]
        for i in data:
            code = i['id']
            name = i['name']
            buttons_q.append(InlineKeyboardButton(text=name, callback_data=f'aquizes_edit:{code}'))
        paginator = KeyboardPaginator(data=buttons_q, per_page=5, per_row=2, router=router,
                                      additional_buttons=additional_buttons)

        return paginator.as_markup()
    elif type_ == 'locations':
        data = await select_all_places()
        buttons_q = []
        additional_buttons = [
            [
                InlineKeyboardButton(text="Назад 🔙", callback_data="admin"),
            ]
        ]
        for i in data:
            code = i['id']
            name = i['name']
            buttons_q.append(InlineKeyboardButton(text=name, callback_data=f'alocations_edit:{code}'))
        paginator = KeyboardPaginator(data=buttons_q, per_page=5, per_row=2, router=router,
                                      additional_buttons=additional_buttons)

        return paginator.as_markup()


def variant_kb(id_, type_):
    kb = [
        [
            InlineKeyboardButton(text='Переписать', callback_data=f'admin_record:{type_}:rewrite:{id_}'),
            InlineKeyboardButton(text='Удалить', callback_data=f'admin_record:{type_}:delete:{id_}')
        ],
        [
            InlineKeyboardButton(text='Назад', callback_data='menu_edit')
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def return_to_vubor(id_, type_):
    kb = []
    if type_ == 'quiz':
            kb.append(
                [InlineKeyboardButton(text='Назад', callback_data=f'aquizes_edit:{id_}')]
            )
    return InlineKeyboardMarkup(inline_keyboard=kb)


async def quiz_paginator(router):
    data = await select_all_quizes___()
    buttons_q = []
    additional_buttons = [
        [
            InlineKeyboardButton(text="Назад 🔙", callback_data="admin"),
        ]
    ]
    for i in data:
        code = i['id']
        quiz_tag = i['tag']
        buttons_q.append(InlineKeyboardButton(text=quiz_tag, callback_data=f'aquizes_delete:{code}'))
    paginator = KeyboardPaginator(data=buttons_q, per_page=15, per_row=2, router=router,
                                  additional_buttons=additional_buttons)

    return paginator.as_markup()


def quiz_delete_kb(quiz_id):
    kb = [
        [
            InlineKeyboardButton(text='Удалить', callback_data=f'quiz_delete:{quiz_id}')
        ],
        [
            InlineKeyboardButton(text='Назад', callback_data='menu_delete')
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)