from aiogram.fsm.state import State, StatesGroup


class CatalogActions(StatesGroup):
    all_category_goods = State()
    select_category_goods = State()
    all_subcategory_goods = State()
    select_subcategory_goods = State()
    all_product = State()
    select_product = State()
    add_cart = State()
    count = State()
    confirm = State()
