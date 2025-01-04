from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.model.state import UserState
import bot.keyboards as keyboards
from bot.messages.links_messages import query_count, set_count
from bot.messages.start_message import send_start_message

from bot.utils.proccess_account import process_account, proccess_bad


router = Router()


def callback(button):
    return keyboards.LINK_BUTTONS[button]["callback_data"]


@router.message(Command("start"))
async def start_handler(msg: Message):
    await send_start_message(msg)


@router.message(F.text == keyboards.TEXTS["menu"])
async def menu_handler(msg: Message):
    await send_start_message(msg)


@router.message(F.text == keyboards.TEXTS["links"])
async def get_links_handler(msg: Message, state: FSMContext):
    await query_count(msg, state)


@router.message(UserState.count)
async def setting_count(msg: Message, state: FSMContext):
    await set_count(msg, state)


@router.callback_query(F.data.startswith(callback("CHECK")))
async def check_handler(callback_query: types.CallbackQuery):
    await process_account(callback_query)


@router.callback_query(F.data.startswith(callback("REFRESH")))
async def check_handler(callback_query: types.CallbackQuery):
    await process_account(callback_query, update_link=True)


@router.callback_query(F.data.startswith(callback("BAD")))
async def check_handler(callback_query: types.CallbackQuery):
    await proccess_bad(callback_query)
