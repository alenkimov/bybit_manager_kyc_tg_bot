from bot.model.chatData import ChatDataEntry, chat_data


def get_data(chat_id: str) -> ChatDataEntry:
    if not chat_id in chat_data:
        chat_data[chat_id] = {"accounts": {}, "bad": [], "delayed": {}}
    return chat_data[chat_id]
