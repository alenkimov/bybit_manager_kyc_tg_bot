from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

texts = {"menu": "Main menu", "links": "Get links"}
link_buttons = {
    "CHECK": {"text": "CHECK", "callback_data": "check"},
    "REFRESH": {"text": "REFRESH LINK", "callback_data": "refresh"},
    "BAD": {"text": "BAD", "callback_data": "bad"},
}

links_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=texts["links"])]],
    resize_keyboard=True,
    input_field_placeholder="Enter your option",
)

main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=texts["menu"])]],
    resize_keyboard=True,
    input_field_placeholder="Enter count of links",
)

link_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=link_buttons["CHECK"]["text"],
                callback_data=link_buttons["CHECK"]["callback_data"],
            ),
            InlineKeyboardButton(
                text=link_buttons["REFRESH"]["text"],
                callback_data=link_buttons["REFRESH"]["callback_data"],
            ),
            InlineKeyboardButton(
                text=link_buttons["BAD"]["text"],
                callback_data=link_buttons["BAD"]["callback_data"],
            ),
        ]
    ]
)


def create_link_keyboard(db_id) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=link_buttons["CHECK"]["text"],
                    callback_data=f"{link_buttons['CHECK']['callback_data']}:{db_id}",
                ),
                InlineKeyboardButton(
                    text=link_buttons["REFRESH"]["text"],
                    callback_data=f"{link_buttons['REFRESH']['callback_data']}:{db_id}",
                ),
                InlineKeyboardButton(
                    text=link_buttons["BAD"]["text"],
                    callback_data=f"{link_buttons['BAD']['callback_data']}:{db_id}",
                ),
            ]
        ]
    )
