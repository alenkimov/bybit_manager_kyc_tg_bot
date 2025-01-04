import time

from bot.utils.get_data import get_data
from api_client.dto.account_dto import AccountDto


COOLDOWN_SEC = 600


def check_account(account: AccountDto, chat_id):
    return (
        check_status(account)
        and check_db(account, chat_id)
        and check_cooldown(account, chat_id)
    )


def check_cooldown(account: AccountDto, chat_id):
    current_time = time.time()
    db_id = str(account.get_id())

    return not (
        db_id in get_data(chat_id)["delayed"].keys()
        and current_time - get_data(chat_id)["delayed"][db_id] < COOLDOWN_SEC
    )


def check_db(account: AccountDto, chat_id):
    dbId = str(account.get_id())
    return not dbId in get_data(chat_id)["bad"]


def check_status(account: AccountDto):
    return (
        account.get_status() == "ALLOW"
        or account.get_status() == "FAILED_AND_CAN_RETRY"
    )
