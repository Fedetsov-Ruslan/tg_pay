from aiogram import Router, F
from aiogram.types import  CallbackQuery
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.handlers.fsm.states import CatalogActions

router = Router()


@router.callback_query(F.data.startswith == "catalog")
async def get_category(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    
    await state.set_state(CatalogActions.category_goods)


@router.callback_query(CatalogActions.category_goods)
async def get_subcategory(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.update_data(category_goods=callback.data)
        
    await state.set_state(CatalogActions.subcategory_goods) 
    

@router.callback_query(CatalogActions.subcategory_goods)
async def get_product(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.update_data(subcategory_goods=callback.data)
    
    await state.set_state(CatalogActions.product)


@router.callback_query(CatalogActions.product)
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
