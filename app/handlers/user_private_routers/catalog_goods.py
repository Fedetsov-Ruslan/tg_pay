from aiogram import Router, F
from aiogram.types import  CallbackQuery, InputMediaPhoto, Message
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import (
    orm_create_cart,
    orm_get_all_categories,
    orm_get_all_subcategories,
    orm_get_all_goods,
    orm_get_product_name_for_id,
    )
from handlers.fsm.states import CatalogActions
from kbds.inline import (
    get_confirm_keyboard,
    get_start_menu_kbds,
    get_paginator_keyboard,
    get_paginated_for_products,
    )

router = Router()


@router.callback_query(F.data.startswith("catalog"))
async def get_category(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.set_state(CatalogActions.all_category_goods)
    categories = await orm_get_all_categories(session=session)
    await state.update_data(all_category_goods=categories)
    await callback.message.edit_reply_markup(reply_markup=get_paginator_keyboard(data=categories))
    await state.set_state(CatalogActions.select_category_goods)
    

@router.callback_query(F.data.startswith("page_"), CatalogActions.select_category_goods)
async def search_category(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    page = int(callback.data.split('_')[1])
    data = await state.get_data()
    categories = data.get('all_category_goods', [])
    await callback.message.edit_reply_markup(reply_markup=get_paginator_keyboard(page=page, data=categories)) 



@router.callback_query(CatalogActions.select_category_goods)
async def get_subcategory(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.update_data(select_category_goods=callback.data)
    subcategories = await orm_get_all_subcategories(session=session, category=callback.data)
    await state.set_state(CatalogActions.all_subcategory_goods) 
    await state.update_data(all_subcategory_goods=subcategories)
    await callback.message.edit_reply_markup(reply_markup=get_paginator_keyboard(data=subcategories))
    await state.set_state(CatalogActions.select_subcategory_goods)
    

@router.callback_query(F.data.startswith("page_"), CatalogActions.select_subcategory_goods)
async def search_category(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    page = int(callback.data.split('_')[1])
    data = await state.get_data()
    categories = data.get('all_subcategory_goods', [])
    await callback.message.edit_reply_markup(reply_markup=get_paginator_keyboard(page=page, data=categories)) 
    

@router.callback_query(CatalogActions.select_subcategory_goods)
async def get_product(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.update_data(select_subcategory_goods=callback.data)
    products = await orm_get_all_goods(session=session, subcategory=callback.data)
    await state.set_state(CatalogActions.all_product)
    await state.update_data(all_product=products)
    product = products[0]
    await callback.message.answer_photo(
        photo=product.photo_url,
        caption=product.name,
        reply_markup=get_paginated_for_products(
            products=products))
    await state.set_state(CatalogActions.select_product)


@router.callback_query(F.data.startswith("page_"), CatalogActions.select_product)
async def search_category(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    page = int(callback.data.split('_')[1])
    data = await state.get_data()
    products = data.get('all_product', [])
    media = InputMediaPhoto(
        media=products[page].photo_url,
        caption=products[page].name)
    paginator_kbds = get_paginated_for_products(products=products, page=page)
    await callback.message.edit_media(media=media, reply_markup=paginator_kbds)
                                      

@router.callback_query(F.data.startswith("select_product"), CatalogActions.select_product)
async def select_count(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    product = int(callback.data.split('_')[-1])
    await state.update_data(select_product=product)
    await callback.message.answer("Введите количество")
    await state.set_state(CatalogActions.count)
    
      
    
@router.message(CatalogActions.count)
async def confirm(message: Message, state: FSMContext, session: AsyncSession):
    print(123)
    try:
        count = int(message.text)
        await state.update_data(count=count)
        data = await state.get_data()
        product_name = await orm_get_product_name_for_id(session=session, id=data['select_product'])
        await message.answer(f"Товар: {product_name}\nКоличество: {count}", reply_markup=get_confirm_keyboard())
        await state.set_state(CatalogActions.confirm)
        await state.update_data(confirm=product_name)
    except:
        await message.answer("Количество должно быть целым числом")
        

@router.callback_query(CatalogActions.confirm)
async def confirm(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    cart = await orm_create_cart(session=session, user_id=callback.from_user.id, product_id=data['select_product'], count=data['count'])
    print(cart.id)
    await callback.message.answer(f"Товар: {data['confirm']} добавлен в корзину в количество {data['count']}", reply_markup=get_start_menu_kbds())
    await state.clear()

    
    
