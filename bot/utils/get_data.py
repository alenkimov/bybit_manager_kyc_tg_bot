from bot.model.chatData import ChatData, chat_data


def get_data(chat_id: str) -> ChatData:
    if not chat_id in chat_data:
        chat_data[chat_id] = {"accounts": {}, "bad": [], "delayed": {}}
    return chat_data[chat_id]
