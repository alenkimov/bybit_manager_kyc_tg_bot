from bot.utils.get_data import get_data


def mark_bad(db_id, chat_id):
    del get_data(chat_id)["accounts"][db_id]
    print(get_data(chat_id))
    if not db_id in get_data(chat_id)["bad"]:
        get_data(chat_id)["bad"].append(db_id)
