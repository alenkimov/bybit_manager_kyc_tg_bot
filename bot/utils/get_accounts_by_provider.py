from bot.api.accounts_list import ids_by_tg_provider
from bot.api.account_info import account_info
from bot.utils.check_account import check_account
from aiogram.types import Message
import time


def get_accounts_by_provider(msg: Message):
    ids = ids_by_tg_provider(msg.from_user.username)
    accounts = []
    for id in ids:
        account = account_info(id)
        if check_account(account, msg.chat.id):
            accounts.append(account)

    return accounts
