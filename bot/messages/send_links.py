from itertools import islice
import time

from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.utils.check_account import filter_accounts
from bot.utils.get_data import get_data
from bot.model.state import UserState
from bot.model.state import UserState
from bot.api.account_info import account_info
from bot.api.account_link import account_sumsub_url
from .start_message import send_start_message
from .message_parser import stringify_message
from .loading_message import send_loading_message
import bot.keyboards as keyboards


async def send_links(msg: types.Message, state: FSMContext):
    if not msg.text:  # Пустой ввод
        return
    text = msg.text
    if text == keyboards.TEXTS["menu"]:  # Выход из состояния
        await state.clear()
        await send_start_message(msg)

    elif not text.isdigit() or int(text) < 1:  # Некорректный ввод
        await state.set_state(UserState.count)
        await msg.answer(
            "Please, enter a number greater than 0",
            reply_markup=keyboards.main_menu_keyboard,
        )

    else:
        chat_id = str(msg.chat.id)
        chat_data = get_data(chat_id)
        ready_accounts = filter_accounts(
            chat_data,
            list(account["account"] for account in chat_data["accounts"].values()),
        )
        delete_loading_message = await send_loading_message("Preparing links...", msg)

        try:
            for account in islice(ready_accounts, int(text)):

                updated_account = account_info(account.get_id())

                if updated_account.is_kyc_allowed():
                    sumsub_url = account_sumsub_url(account.get_id())
                    chat_data["accounts"][str(account.get_id())]["link"] = sumsub_url
                    chat_data["delayed"][str(account.get_id())] = time.time()

                await msg.answer(
                    stringify_message(account, sumsub_url),
                    reply_markup=(
                        keyboards.create_link_keyboard(account.get_id())
                        if updated_account.is_kyc_allowed()
                        else None
                    ),
                )

        # except Exception as e:
        #     await msg.answer(
        #         f"Error while generating links. Contact your admin or try again.\n\n Detailed Error: {e}",
        #     )
        #     await send_start_message(msg)

        finally:
            await delete_loading_message()
            await state.clear()
