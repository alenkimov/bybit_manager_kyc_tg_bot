from aiogram.types import Message

from bot.api.accounts_list import ids_by_tg_provider
from bot.api.account_info import account_info
from bot.utils.check_account import check_account
from api_client.dto.account_dto import AccountDto


def get_accounts_by_provider(msg: Message) -> list[AccountDto]:
    ids = ids_by_tg_provider(msg.from_user.username)
    accounts = []

    for database_id in ids:
        account = account_info(database_id)

        if check_account(account, msg.chat.id):
            accounts.append(account)

    return accounts
