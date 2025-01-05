from typing import Callable, Awaitable

from aiogram import types


async def send_loading_message(
    text: str, msg: types.Message
) -> Callable[[], Awaitable[None]]:
    loading_messaage = await msg.answer(text, reply_markup=types.ReplyKeyboardRemove())

    async def delete_loading_message():
        if loading_messaage:
            await loading_messaage.delete()

    return delete_loading_message
