from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties


from bot.handlers import router


async def start_bot(token: str):
    bot = Bot(token=token, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()
    dp.include_router(router)

    # Оффаем обработку вне работы бота
    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
