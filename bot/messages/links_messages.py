import time

from aiogram import types
from aiogram.fsm.context import FSMContext

import bot.keyboards as keyboards
from bot.utils.get_accounts_by_provider import get_accounts_by_provider
from bot.utils.get_data import get_data
from bot.model.state import UserState
from bot.messages.message_parser import stringify_message
from bot.messages.start_message import send_start_message
from bot.api.account_link import account_link


async def query_count(msg: types.Message, state: FSMContext):
    chat_id = msg.chat.id
    answer = await msg.answer(
        "Fetching accounts...", reply_markup=types.ReplyKeyboardRemove()
    )
    try:
        accounts = get_accounts_by_provider(msg)

        if not len(accounts):
            await msg.answer(
                "Sorry, currently no accounts available. Try again later.",
            )
            await send_start_message(msg)
            return

        get_data(chat_id)["accounts"] = {}
        for account in accounts:
            dbId = str(account.get_id())

            get_data(chat_id)["accounts"][dbId] = {"account": account}

        await msg.answer(
            f"Count of currently available accounts: {len(get_data(chat_id)['accounts'])}."
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
        if answer:
            await answer.delete()


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
        loading_answer = await msg.answer("Preparing links...")

        try:
            for i, (db_id, account) in enumerate(ready_accounts.items()):
                if i >= validated_count:
                    break

                response = account_link(db_id)
                get_data(chat_id)["accounts"][db_id]["link"] = response
                get_data(chat_id)["delayed"][db_id] = time.time()
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
            await loading_answer.delete()
            await state.clear()
