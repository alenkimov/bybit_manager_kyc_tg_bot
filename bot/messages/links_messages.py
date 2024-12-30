from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.utils.get_accounts_by_provider import get_accounts_by_provider
from bot.model.state import UserState

import bot.keyboards as keyboards

from bot.messages.message_parser import stringify_message
from bot.messages.start_message import send_start_message

from bot.api.account_link import account_link


async def query_count(msg: types.Message, chat_data, state: FSMContext):
    chat_id = msg.chat.id
    answer = await msg.answer(
        "Fetching accounts...", reply_markup=types.ReplyKeyboardRemove()
    )
    try:
        accounts = get_accounts_by_provider(msg.from_user.username)
        for account in accounts:
            chat_data[chat_id] = {
                "accounts": {str(account["database_id"]): {"account": account}}
            }

        await msg.answer(f"Count of currently available accounts: {len(accounts)}.")
        await state.set_state(UserState.count)
        await msg.answer(
            "Specify how many accounts you want to process",
            reply_markup=keyboards.main_menu_keyboard,
        )

    except Exception:
        await msg.answer(
            "Error while retrieving accounts. Try again or contact an admin.",
        )
        await send_start_message(msg)
    finally:
        await answer.delete()


async def set_count(msg: types.Message, chat_data, state: FSMContext):
    chat_id = msg.chat.id
    if msg.text == keyboards.texts["menu"]:  # Выход из состояния
        await state.clear()
        await send_start_message(msg)
    elif not msg.text.isdigit() or int(msg.text) < 1:  # Некорректный ввод
        await state.set_state(UserState.count)
        await msg.answer(
            "Please, enter a number greater than 0",
            reply_markup=keyboards.main_menu_keyboard,
        )
    else:
        ready_accounts = chat_data[chat_id]["accounts"]
        validated_count = (
            len(ready_accounts)
            if int(msg.text) > len(ready_accounts)
            else int(msg.text)
        )
        await state.update_data(count=validated_count)
        loading_answer = await msg.answer("Preparing links...")
        try:
            for i, (dbId, account) in enumerate(ready_accounts.items()):
                if i >= validated_count:
                    break
                response = account_link(dbId)
                chat_data[chat_id]["accounts"][dbId]["link"] = response
                await msg.answer(
                    stringify_message(account["account"], response),
                    reply_markup=keyboards.create_link_keyboard(dbId),
                )
        except Exception:
            await msg.answer(
                "Error while generating links. Contact your admin or try again.",
            )
            await send_start_message(msg)
        finally:
            await loading_answer.delete()
            await state.clear()
