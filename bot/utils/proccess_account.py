from bot.api.account_info import account_info
from aiogram import types
from bot.messages.message_parser import stringify_notallow_message, stringify_message
from bot.api.account_link import account_link
import bot.keyboards as keyboards


"""Обработать изменение аккаунта (CHECK/REFRESH)."""


async def process_account(
    callback_query: types.CallbackQuery, chat_data, update_link=False
):
    dbId = callback_query.data.split(":")[1]
    message = callback_query.message
    chat_id = message.chat.id

    try:
        account = account_info(dbId)
        chat_data[chat_id]["accounts"][dbId]["account"] = account
        status = account["kyc"]["state"][0]["status"]

        if status != "ALLOW":
            await message.edit_text(
                stringify_notallow_message(account),
            )
            return

        link = (
            account_link(dbId)
            if update_link
            else chat_data[chat_id]["accounts"][dbId]["link"]
        )
        if update_link:
            chat_data[chat_id]["accounts"][dbId]["link"] = link
            await callback_query.answer("Link updated")

        await message.edit_text(
            stringify_message(account, link),
            reply_markup=keyboards.create_link_keyboard(dbId),
        )
    except Exception:
        await message.edit_text(
            "Error while fetching accounts. Contact your employer.",
            reply_markup=keyboards.main_menu_keyboard,
        )


""" Обработать BAD """


async def proccess_bad(callback_query: types.CallbackQuery, chat_data):
    dbId = callback_query.data.split(":")[1]
    message = callback_query.message
    account = chat_data[message.chat.id]["accounts"][dbId]["account"]
    account["kyc"]["state"][0]["status"] = "BAD"
    await message.edit_text(
        stringify_notallow_message(account),
    )
