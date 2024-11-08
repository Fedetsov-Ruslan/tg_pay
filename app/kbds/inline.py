from aiogram.types import InlineKeyboardButton, InputMediaPhoto, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import  CallbackQuery



def get_start_menu_kbds():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="📚 Каталог", callback_data="catalog"))
    keyboard.add(InlineKeyboardButton(text="🛒 Корзина", callback_data="cars"))
    keyboard.add(InlineKeyboardButton(text="📊 Ответы на вопросы", callback_data="faq"))
    return keyboard.as_markup()


def get_paginator_keyboard(*, 
                           page: int = 0, 
                           items_per_page: int=10,
                           data: list[str] = [],
                           sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()
    start = page * items_per_page
    end = start + items_per_page
    for row in data[start:end]:
        if row in data:
            keyboard.add(InlineKeyboardButton(text=row.name, callback_data=row.name))
        else:
            keyboard.add(InlineKeyboardButton(text=row.name, callback_data=row.name))

    navigation_buttons = []
    if start > 0:
        navigation_buttons.append(InlineKeyboardButton(text="Предыдущая страница", callback_data=f"page_{page - 1}"))
    if end < len(data):
        navigation_buttons.append(InlineKeyboardButton(text="Следующая страница", callback_data=f"page_{page + 1}"))
    keyboard.add(*navigation_buttons)
    return keyboard.adjust(*sizes).as_markup()


def get_paginated_for_products(products: list, page: int = 0):
    keyboard = InlineKeyboardBuilder()
    if page > 0:
        keyboard.add(InlineKeyboardButton(text="← Previous", callback_data=f"page_{page - 1}"))
    keyboard.add(InlineKeyboardButton(text="Выбрать товар", callback_data="select_product"))
    if page < len(products):
        keyboard.add(InlineKeyboardButton(text="Next →", callback_data=f"page_{page + 1}"))

    return keyboard.adjust(3,).as_markup()