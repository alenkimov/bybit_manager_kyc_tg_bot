from bot.api.account_info import account_info
from aiogram import types
from bot.utils.get_data import get_data
from bot.messages.message_parser import stringify_message
from bot.api.account_link import account_sumsub_url
from bot.api.mark_bad import mark_bad
import bot.keyboards as keyboards
from aiogram.exceptions import TelegramBadRequest
from api_client.dto.sumsub_url_dto import SumsubUrlDto
from bot.model.chat_data import ChatDataEntry


def get_link(
    chat_data: ChatDataEntry, db_id: str, update_link: bool
) -> SumsubUrlDto | None:
    if update_link:
        link = account_sumsub_url(int(db_id))
        chat_data["accounts"][db_id]["link"] = link
    else:
        link = chat_data["accounts"][db_id]["link"]
    return link


async def process_account(callback_query: types.CallbackQuery, update_link=False):
    """Обработать изменение аккаунта (CHECK/REFRESH)."""
    message = callback_query.message
    if not message or not callback_query.data or type(message) != types.Message:
        await callback_query.answer("Some error occured")
        return

    db_id = callback_query.data.split(":")[1]
    chat_id = message.chat.id
    chat_data = get_data(str(chat_id))

    try:
        account = account_info(int(db_id))
        status = account.get_status()

        if status not in {"ALLOW", "FAILED_AND_CAN_RETRY"}:
            await message.edit_text(
                stringify_message(account),
            )
            return

        link = get_link(chat_data, db_id, update_link)
        if not link:
            await callback_query.answer("Some error occured")
            return

        if update_link:
            await callback_query.answer("Link updated")

        await message.edit_text(
            stringify_message(account, link),
            reply_markup=keyboards.create_link_keyboard(db_id),
        )

    except TelegramBadRequest as e:
        # Обработка случаев, когда сообщение не может быть отредактировано
        await callback_query.answer(f"Error: {str(e)}")

    except Exception:
        await message.answer(
            "Some error occured. Contact your employer.",
        )


async def proccess_bad(callback_query: types.CallbackQuery):
    """Обработать BAD"""
    message = callback_query.message
    if not message or not callback_query.data or type(message) != types.Message:
        await callback_query.answer("Some error occured")
        return
    db_id = callback_query.data.split(":")[1]
    chat_id = message.chat.id
    chat_data = get_data(str(chat_id))
    account = chat_data["accounts"][db_id]["account"]

    account.set_status("BAD")
    mark_bad(db_id, chat_id=chat_id)  # Сохраняем

    await message.edit_text(
        stringify_message(account),
    )
