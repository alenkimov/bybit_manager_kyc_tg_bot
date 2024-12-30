from aiogram import types
import bot.keyboards as keyboards


async def send_start_message(msg: types.Message):
    await msg.answer(
        "I will assist you with your kyc tasks. Select an option.",
        reply_markup=keyboards.links_keyboard,
    )
