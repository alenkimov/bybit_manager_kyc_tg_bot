import time
from typing import Sequence
from api_client.dto.account_dto import AccountDto
from bot.model.chat_data import ChatDataEntry


COOLDOWN_SEC = 600


def filter_accounts(
    chat_data: ChatDataEntry, accounts: Sequence[AccountDto]
) -> Sequence[AccountDto]:
    return [account for account in accounts if check_account(chat_data, account)]


def check_account(chat_data: ChatDataEntry, account: AccountDto):
    return (
        check_status(account)
        and check_bad(account, chat_data)
        and check_cooldown(account, chat_data)
    )


def check_cooldown(account: AccountDto, chat_data: ChatDataEntry):
    current_time = time.time()
    db_id = str(account.get_id())

    return not (
        db_id in chat_data["delayed"].keys()
        and current_time - chat_data["delayed"][db_id] < COOLDOWN_SEC
    )


def check_bad(account: AccountDto, chat_data: ChatDataEntry):
    dbId = str(account.get_id())
    return not dbId in chat_data["bad"]


def check_status(account: AccountDto):
    return account.is_kyc_allowed()
