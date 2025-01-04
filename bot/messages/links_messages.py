import time

from typing import Callable, Awaitable

from aiogram import types
from aiogram.fsm.context import FSMContext

import bot.keyboards as keyboards
from bot.utils.get_accounts_by_provider import get_accounts_by_provider
from bot.utils.get_data import get_data
from bot.model.state import UserState
from bot.messages.message_parser import stringify_message
from APIClient.dto.account_dto import AccountDto
from bot.messages.start_message import send_start_message
from bot.api.account_link import account_link
from bot.model.state import UserState
import bot.keyboards as keyboards


async def send_loading_message(
    text: str, msg: types.Message
) -> Callable[[], Awaitable[None]]:
    loading_messaage = await msg.answer(text, reply_markup=types.ReplyKeyboardRemove())

    async def delete_loading_message():
        if loading_messaage:
            await loading_messaage.delete()

    return delete_loading_message


async def handle_no_accounts(msg: types.Message):
    await msg.answer("Sorry, currently no accounts available. Try again later.")
    await send_start_message(msg)


def update_accounts_data(chat_id: int, accounts: list[AccountDto]):
    get_data(chat_id)["accounts"] = {}  # Очищение памяти
    for account in accounts:
        dbId = str(account.get_id())

        get_data(chat_id)["accounts"][dbId] = {"account": account}


async def query_count(msg: types.Message, state: FSMContext):
    chat_id = msg.chat.id

    delete_loading_message = await send_loading_message("Fetching accounts...", msg)

    try:
        accounts = get_accounts_by_provider(msg)

        if not accounts:
            await handle_no_accounts(msg)
            return

        update_accounts_data(chat_id, accounts)

        await msg.answer(f"Count of currently available accounts: {len(accounts)}.")
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


async def set_count(msg: types.Message, state: FSMContext):
    chat_id = msg.chat.id
    if msg.text == keyboards.TEXTS["menu"]:  # Выход из состояния
        await state.clear()
        await send_start_message(msg)

    elif not msg.text.isdigit() or int(msg.text) < 1:  # Некорректный ввод
        await state.set_state(UserState.count)
        await msg.answer(
            "Please, enter a number greater than 0",
            reply_markup=keyboards.main_menu_keyboard,
        )

    else:
        ready_accounts = get_data(chat_id)["accounts"]

        validated_count = (
            len(ready_accounts)
            if int(msg.text) > len(ready_accounts)
            else int(msg.text)
        )
        await state.update_data(count=validated_count)

        delete_loading_message = await send_loading_message("Preparing links...", msg)

        try:
            for i, (db_id, account) in enumerate(ready_accounts.items()):
                if i >= validated_count:
                    break

                response = account_link(db_id)
                chat = get_data(chat_id)

                chat["accounts"][db_id]["link"] = response
                chat["delayed"][db_id] = time.time()

                await msg.answer(
                    stringify_message(account["account"], response),
                    reply_markup=keyboards.create_link_keyboard(db_id),
                )

        except Exception as e:
            await msg.answer(
                f"Error while generating links. Contact your admin or try again.\n\n Detailed Error: {e}",
            )
            await send_start_message(msg)

        finally:
            await delete_loading_message()
            await state.clear()
