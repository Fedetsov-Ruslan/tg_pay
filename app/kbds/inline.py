from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder



def get_start_menu_kbds():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="📚 Каталог", callback_data="catalog"))
    keyboard.add(InlineKeyboardButton(text="🛒 Корзина", callback_data="cars"))
    keyboard.add(InlineKeyboardButton(text="📊 Ответы на вопросы", callback_data="faq"))
    return keyboard.as_markup()