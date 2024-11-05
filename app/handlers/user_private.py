from aiogram import Router, F
from aiogram.types import  CallbackQuery
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext

from app.handlers.user_private_routers.cart_goods import router as cart_goods_router
from app.handlers.user_private_routers.catalog_goods import router as catalog_goods_router
from app.handlers.user_private_routers.questions import router as questions_router


router = Router()

router.include_router(cart_goods_router)
router.include_router(catalog_goods_router)
router.include_router(questions_router)