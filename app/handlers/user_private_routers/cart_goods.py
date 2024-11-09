from aiogram import Router, F
from aiogram.types import  CallbackQuery, InputMediaPhoto, Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from kbds.inline import (
    get_paginated_for_carts,
    get_payment_keyboard,
    pay_url_kbds
)
from database.orm_query import (
    orm_get_carts,
    orm_delete_product_in_cart
)
from handlers.fsm.states import CartActions
from yookassa_payment import yookassa_payment


router = Router()


@router.callback_query(F.data.startswith("cart"))
async def view_cart(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.set_state(CartActions.viewing_cart)
    cart = await orm_get_carts(session=session, telegram_id=callback.from_user.id)
    cart_list = [i for i in cart]
    await state.update_data(view_cart=cart_list)
    
    await callback.message.answer_photo(
        photo=cart_list[0].photo_url,
        caption="Товары в корзине: " + cart_list[0].name + "\n" + str(cart_list[0].quantity),
        reply_markup=get_paginated_for_carts(
            carts=cart_list))
    
    
@router.callback_query(F.data.startswith("page_"), CartActions.viewing_cart)
async def paginator_view_cart(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    page = int(callback.data.split('_')[1])
    data = await state.get_data()
    cart_list = data.get('view_cart', [])
    media = InputMediaPhoto(
        media=cart_list[page].photo_url,
        caption="Товары в корзине: " + cart_list[page].name + "\n" + str(cart_list[page].quantity)        
    )
    paginator_kbds = get_paginated_for_carts(carts=cart_list, page=page)
    await callback.message.edit_media(media=media, reply_markup=paginator_kbds)
    

@router.callback_query(F.data.startswith("delete_cart_"), CartActions.viewing_cart)
async def delete_cart(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    await orm_delete_product_in_cart(
        session=session,
        cart_id=int(callback.data.split('_')[-1])
    )
    cart = await orm_get_carts(session=session, telegram_id=callback.from_user.id)
    cart_list = [i for i in cart]
    await state.update_data(view_cart=cart_list)
    await callback.message.answer_photo(
        photo=cart_list[0].photo_url,
        caption="Товары в корзине: " + cart_list[0].name + "\n" + str(cart_list[0].quantity),
        reply_markup=get_paginated_for_carts(
            carts=cart_list)
        )
    
    
@router.callback_query(F.data.startswith("order"), CartActions.viewing_cart)
async def inter_city(callback: CallbackQuery, state: FSMContext):
    await state.set_state(CartActions.city)
    
    await callback.message.answer("Введите город")
    
    
@router.message(CartActions.city)
async def inter_address(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await state.set_state(CartActions.address)
    
    await message.answer("Введите улицу")
    
    
@router.message(CartActions.address)
async def inter_house(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    await state.set_state(CartActions.house)
    
    await message.answer("Введите дом")
    
    
@router.message(CartActions.house)
async def inter_flat(message: Message, state: FSMContext):
    await state.update_data(house=message.text)
    await state.set_state(CartActions.flatt)
    
    await message.answer("Введите квартиру")
    

@router.message(CartActions.flatt)
async def inter_payment(message: Message, state: FSMContext):
    await state.update_data(flatt=message.text)
    await state.set_state(CartActions.payment)
    
    await message.answer(
        "Оплатить товары?",
        reply_markup=get_payment_keyboard()
        )
    
    
@router.callback_query(F.data.startswith("payment"), CartActions.payment)
async def payment(callback: CallbackQuery):
    
    try:
        payment_url = await yookassa_payment(
            payment_id=str(callback.from_user.id),
            amount=10000,
            description="Оплата покупок"
        )
        await callback.message.reply(
            "Для оплаты нажмите на кнопку ниже",
            reply_markup=pay_url_kbds(payment_url)
            )
    except:
        await callback.message.reply("Произошла ошибка, попробуйте позже")
        
   
    