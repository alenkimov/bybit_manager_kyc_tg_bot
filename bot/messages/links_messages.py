from typing import Sequence

from aiogram import types
from aiogram.fsm.context import FSMContext

from api_client.dto.account_dto import AccountDto

from bot.utils.get_accounts_by_provider import get_accounts_by_provider
from bot.utils.get_data import get_data
from bot.utils.check_account import filter_accounts
from bot.model.chat_data import ChatDataEntry
from bot.model.state import UserState
from .start_message import send_start_message
from .loading_message import send_loading_message
import bot.keyboards as keyboards


async def handle_no_accounts(msg: types.Message):
    await msg.answer("Sorry, currently no accounts available. Try again later.")
    await send_start_message(msg)


def update_accounts_data(chat_data: ChatDataEntry, accounts: Sequence[AccountDto]):
    # chat_data["accounts"] = {}  # Очищение памяти
    for account in accounts:
        db_id = str(account.get_id())
        chat_data["accounts"][db_id] = {"account": account, "link": None}


async def query_count(msg: types.Message, state: FSMContext):
    try:
        if not msg.from_user:
            return

        delete_loading_message = await send_loading_message("Fetching accounts...", msg)

        accounts = get_accounts_by_provider(msg.from_user.username or "")
        chat_data = get_data(str(msg.chat.id))

        filtered_accounts = filter_accounts(chat_data, accounts)
        if not filtered_accounts:
            await handle_no_accounts(msg)
            return

        update_accounts_data(chat_data, filtered_accounts)

        await msg.answer(
            f"Count of currently available accounts: {len(filtered_accounts)}."
        )
        await state.set_state(UserState.count)
        await msg.answer(
            "Specify how many accounts you want to process",
            reply_markup=keyboards.main_menu_keyboard,
        )

    except Exception as e:
        await msg.answer(
            f"Error while retrieving accounts. Try again or contact an admin.\n\nDetailed Error: {e}",
        )
        await send_start_message(msg)

    finally:
        await delete_loading_message()
