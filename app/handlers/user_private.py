from aiogram import Router, F, types
from aiogram.types import  CallbackQuery, ChatMemberStatus
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext

from app.config import CHANNEL_ID
from app.handlers.user_private_routers.cart_goods import router as cart_goods_router
from app.handlers.user_private_routers.catalog_goods import router as catalog_goods_router
from app.handlers.user_private_routers.questions import router as questions_router
from app.kbds.inline import get_start_menu_kbds


router = Router()

router.include_router(cart_goods_router)
router.include_router(catalog_goods_router)
router.include_router(questions_router)


async def check_subscription(user_id: int, bot:types.Bot) -> bool:
    try:
        chat_member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return chat_member.status in ["member", "administrator", "creator"]
    except Exception as e:
        print(e)
        return False


@router.message(CommandStart())
async def start(callback: CallbackQuery, state: FSMContext):
    user = callback.message.from_user.id
    bot_instanse = callback.bot()
    if await check_subscription(user, bot_instanse):
        await callback.answer('Добро пожаловать за покупками', reply_markup=get_start_menu_kbds())

    