from bot.utils.get_data import get_data
import time


def check_account(account, chat_id):
    return (
        check_status(account)
        and check_db(account, chat_id)
        and check_cooldown(account, chat_id)
    )


def check_cooldown(account, chat_id):
    current_time = time.time()
    db_id = str(account["database_id"])

    print(get_data(chat_id)["delayed"].keys())
    if db_id in get_data(chat_id)["delayed"].keys():
        print(current_time - get_data(chat_id)["delayed"][db_id])

    return not (
        db_id in get_data(chat_id)["delayed"].keys()
        and current_time - get_data(chat_id)["delayed"][db_id] < 600
    )


def check_db(account, chat_id):
    dbId = str(account["database_id"])
    return not dbId in get_data(chat_id)["bad"]


def check_status(account):
    return (
        account["state"][0]["status"] == "ALLOW"
        or account["state"][0]["status"] == "FAILED_AND_CAN_RETRY"
    )
