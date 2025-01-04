from bot.model.chat_data import ChatDataEntry, chat_data


def get_data(chat_id: str) -> ChatDataEntry:
    if chat_id not in chat_data:
        chat_data[chat_id] = {"accounts": {}, "bad": [], "delayed": {}}
    return chat_data[chat_id]
