from aiogram.fsm.state import State, StatesGroup


class CatalogActions(StatesGroup):
    category_goods = State()
    subcategory_goods = State()
    product = State()
    add_cart = State()
    count = State()
    confirm = State()
