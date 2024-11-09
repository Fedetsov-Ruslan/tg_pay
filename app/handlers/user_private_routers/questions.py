from aiogram import Router, F
from aiogram.types import  CallbackQuery, InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4

from kbds.inline import get_inline_mode_button

router = Router()


answers_db = {
    "python": "Python — это высокоуровневый язык программирования.",
    "aiogram": "Aiogram — это асинхронная библиотека для разработки Telegram-ботов.",
    "telegram": "Telegram — это мессенджер, ориентированный на безопасность и скорость."
}
@router.callback_query(F.data.startswith("faq"))
async def faq(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    await callback.message.answer(text="Здесь вы может найти ответы на ваши вопросы", reply_markup=get_inline_mode_button())
    

"""Подключение сайта"""
# @router.inline_query()
# async def inline_query_handler(query: InlineQuery):
#     text = query.query or "echo" 
#     link = 'https://ru.wikipedia.org/wiki/' + text
#     result_id: str = hashlib.md5(text.encode('utf-8')).hexdigest()
    
#     articles = [InlineQueryResultArticle(
#         id=result_id,
#         title='Wikipedia',
#         url=link,
#         input_message_content=InputTextMessageContent(message_text=link),
#    )]
    
#     await query.answer(articles, cache_time=1, is_personal=True)

# @router.callback_query(F.data.startswith("faq"))


@router.inline_query()
async def inline_query_handler(query: InlineQuery):
    """ПОдключения БД. В данном случае БД - словарь."""
    query_text = query.query.strip().lower()
    if not query_text:
        return
    results = []
    for keyword, answer in answers_db.items():
        if keyword in query_text:
            results.append(
                InlineQueryResultArticle(
                    id=str(uuid4()),
                    title=f"Ответ на '{keyword}'",
                    input_message_content=InputTextMessageContent(message_text=answer)
                )
            )
    if results:
        await query.answer(results, cache_time=1)
    else:

        results.append(
            InlineQueryResultArticle(
                id=str(uuid4()),
                title="Ответ не найден",
                input_message_content=InputTextMessageContent(message_text="Извините, ответ на ваш вопрос не найден.")
            )
        )
        await query.answer(results, cache_time=1)

