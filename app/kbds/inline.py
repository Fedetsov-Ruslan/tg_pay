from aiogram.types import InlineKeyboardButton, InputMediaPhoto, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import  CallbackQuery



def get_start_menu_kbds():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="📚 Каталог", callback_data="catalog"))
    keyboard.add(InlineKeyboardButton(text="🛒 Корзина", callback_data="cart"))
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
    keyboard.add(InlineKeyboardButton(text="Добавить в корзину", callback_data=f"select_product_{products[page].id}"))
    if page < len(products)-1:
        keyboard.add(InlineKeyboardButton(text="Next →", callback_data=f"page_{page + 1}"))

    return keyboard.adjust(1,1,1).as_markup()


def get_paginated_for_carts(carts: list, page: int = 0):
    keyboard = InlineKeyboardBuilder()
    if page > 0:
        keyboard.add(InlineKeyboardButton(text="← Previous", callback_data=f"page_{page - 1}"))
    if page < len(carts)-1:
        keyboard.add(InlineKeyboardButton(text="Next →", callback_data=f"page_{page + 1}"))
    keyboard.add(InlineKeyboardButton(text="Удалить", callback_data=f"delete_cart_{carts[page].id}"))
    keyboard.add(InlineKeyboardButton(text="Оформить заказ", callback_data="order"))
    return keyboard.adjust(1,1,1,1).as_markup()


def get_confirm_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Подтвердить", callback_data="confirm"))
    keyboard.add(InlineKeyboardButton(text="Отмена", callback_data="cancel"))
    return keyboard.adjust(1,1).as_markup()