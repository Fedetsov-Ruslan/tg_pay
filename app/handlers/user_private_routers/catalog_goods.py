from aiogram import Router, F
from aiogram.types import  CallbackQuery
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_get_all_categories, orm_get_all_subcategories
from handlers.fsm.states import CatalogActions
from kbds.inline import get_start_menu_kbds, get_paginator_keyboard

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
    print(callback.data)
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
    await state.update_data(subcategory_goods=callback.data)
 
    await state.set_state(CatalogActions.all_product)


@router.callback_query(CatalogActions.all_product)
async def add_to_cart(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.update_data(product=callback.data)
    
    await state.set_state(CatalogActions.add_cart)
    
    
@router.callback_query(CatalogActions.add_cart)
async def count(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.update_data(add_cart=callback.data)
    
    await state.set_state(CatalogActions.count)
    
    
@router.callback_query(CatalogActions.count)
async def confirm(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.update_data(count=callback.data)
    
    await state.set_state(CatalogActions.confirm)
