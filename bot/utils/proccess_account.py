from bot.api.account_info import account_info
from aiogram import types
from bot.utils.get_data import get_data
from bot.messages.message_parser import stringify_notallow_message, stringify_message
from bot.api.account_link import account_link
from bot.api.mark_bad import mark_bad
import bot.keyboards as keyboards


"""Обработать изменение аккаунта (CHECK/REFRESH)."""


async def process_account(callback_query: types.CallbackQuery, update_link=False):
    db_id = callback_query.data.split(":")[1]
    message = callback_query.message
    chat_id = message.chat.id

    try:
        account = account_info(db_id)
        get_data(chat_id)["accounts"][db_id]["account"] = account
        status = account["state"][0]["status"]

        if status != "ALLOW" and status != "FAILED_AND_CAN_RETRY":
            await message.edit_text(
                stringify_notallow_message(account),
            )
            return

        link = (
            account_link(db_id)
            if update_link
            else get_data(chat_id)["accounts"][db_id]["link"]
        )
        if update_link:
            get_data(chat_id)["accounts"][db_id]["link"] = link
            await callback_query.answer("Link updated")

        await message.edit_text(
            stringify_message(account, link),
            reply_markup=keyboards.create_link_keyboard(db_id),
        )
    except Exception:
        await message.edit_text(
            "Error while fetching accounts. Contact your employer.",
            reply_markup=keyboards.main_menu_keyboard,
        )


""" Обработать BAD """


async def proccess_bad(callback_query: types.CallbackQuery):
    db_id = callback_query.data.split(":")[1]
    message = callback_query.message
    chat_id = message.chat.id
    account = get_data(chat_id)["accounts"][db_id]["account"]

    account["state"][0]["status"] = "BAD"
    mark_bad(db_id, chat_id=chat_id)  # Сохраняем

    await message.edit_text(
        stringify_notallow_message(account),
    )
