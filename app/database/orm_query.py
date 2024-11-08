import datetime

from sqlalchemy import distinct, select
from sqlalchemy.orm import Query
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Subcategory, Category, Good


async def orm_get_all_categories(session: AsyncSession):
    result = await session.execute(select(Category))
    return result.scalars().all()


async def orm_get_all_subcategories(session: AsyncSession, category: str):
    result = await session.execute(select(Subcategory).where(
        Subcategory.category_id == select(Category.id).where(Category.name == category).scalar_subquery()
        )
    )
    return result.scalars().all()


async def orm_get_all_goods(session: AsyncSession, subcategory: str):
    result = await session.execute(select(Good).where(
        Good.subcategory_id == select(Subcategory.id).where(Subcategory.name == subcategory).scalar_subquery()
        )
    )
    return result.scalars().all()



