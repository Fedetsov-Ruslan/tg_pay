import datetime

from sqlalchemy import delete, distinct, select
from sqlalchemy.orm import Query
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import (
    Subcategory,
    Category,
    Good,
    User,
    Cart
)


async def orm_get_all_categories(session: AsyncSession):
    result = await session.execute(select(Category))
    return result.scalars().all()


async def orm_get_all_subcategories(session: AsyncSession, category: str):
    result = await session.execute(select(Subcategory).where(
        Subcategory.category_id == select(Category.id).
        where(Category.name == category).scalar_subquery()
        )
    )
    return result.scalars().all()


async def orm_get_all_goods(session: AsyncSession, subcategory: str):
    result = await session.execute(select(Good).where(
        Good.subcategory_id == select(Subcategory.id).
        where(Subcategory.name == subcategory).
        scalar_subquery()
        )
    )
    return result.scalars().all()


async def orm_get_product_name_for_id(session: AsyncSession, id: int):
    result = await session.execute(select(Good.name).where(Good.id == id))
    return result.scalars().first()


async def orm_create_user(session: AsyncSession, user_id: int, name: str):
    user = select(User.id).where(User.telegram_id == user_id)
    if  user == None:
        user = User(telegram_id=user_id, name=name)
        session.add(user)
        await session.commit()
        await session.refresh(user)
    return user


async def orm_create_cart(session: AsyncSession, user_id: int, product_id:int, count: int):
    cart = Cart(
        user_id=select(User.id).
                where(User.telegram_id == user_id).
                scalar_subquery(),
        good_id=product_id, quantity=count)
    session.add(cart)
    await session.commit()
    await session.refresh(cart)
    return cart


async def orm_get_carts(session: AsyncSession, telegram_id: int):
    result = await session.execute(
        select(Cart.id, Good.name, Good.photo_url, Cart.quantity).join(Good).where(
            Cart.user_id == select(User.id).
            where(User.telegram_id == telegram_id).
            scalar_subquery()
            )
    )
    return result


async def orm_delete_product_in_cart(session: AsyncSession, cart_id: int):
    query = delete(Cart).where(Cart.id == cart_id)
    await session.execute(query)
    await session.commit()

