from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from config import CHANNEL_ID
from handlers.user_private_routers.cart_goods import router as cart_goods_router
from handlers.user_private_routers.catalog_goods import router as catalog_goods_router
from handlers.user_private_routers.questions import router as questions_router
from kbds.inline import get_start_menu_kbds
from database.orm_query import orm_create_user



router = Router()

router.include_router(cart_goods_router)
router.include_router(catalog_goods_router)
router.include_router(questions_router)


@router.message(CommandStart())
async def start(message: Message, session: AsyncSession):
    user = message.from_user.id
    try:
        if message.text.split()[-1] == "payment_success":
            await message.answer("Оплата успешно завершена! Спасибо за покупку.")
            await message.answer(
                'Добро пожаловать за покупками',
                reply_markup=get_start_menu_kbds()
                )
        else:
            await message.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user)
            await orm_create_user(session=session, user_id=user, name=message.from_user.full_name)
            await message.answer(
                'Добро пожаловать за покупками',
                reply_markup=get_start_menu_kbds()
                )
    except:
        await message.answer('Подпишитесь на наш канал чтобы пользоваться ботом')

    