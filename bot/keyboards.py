from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

TEXTS = {"menu": "Main menu", "links": "Get links"}
LINK_BUTTONS = {
    "CHECK": {"text": "CHECK", "callback_data": "check"},
    "REFRESH": {"text": "REFRESH LINK", "callback_data": "refresh"},
    "BAD": {"text": "BAD", "callback_data": "bad"},
}

links_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=TEXTS["links"])]],
    resize_keyboard=True,
    input_field_placeholder="Enter your option",
)

main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=TEXTS["menu"])]],
    resize_keyboard=True,
    input_field_placeholder="Enter count of links",
)

link_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=LINK_BUTTONS["CHECK"]["text"],
                callback_data=LINK_BUTTONS["CHECK"]["callback_data"],
            ),
            InlineKeyboardButton(
                text=LINK_BUTTONS["REFRESH"]["text"],
                callback_data=LINK_BUTTONS["REFRESH"]["callback_data"],
            ),
            InlineKeyboardButton(
                text=LINK_BUTTONS["BAD"]["text"],
                callback_data=LINK_BUTTONS["BAD"]["callback_data"],
            ),
        ]
    ]
)


def create_link_keyboard(db_id) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=LINK_BUTTONS["CHECK"]["text"],
                    callback_data=f"{LINK_BUTTONS['CHECK']['callback_data']}:{db_id}",
                ),
                InlineKeyboardButton(
                    text=LINK_BUTTONS["REFRESH"]["text"],
                    callback_data=f"{LINK_BUTTONS['REFRESH']['callback_data']}:{db_id}",
                ),
                InlineKeyboardButton(
                    text=LINK_BUTTONS["BAD"]["text"],
                    callback_data=f"{LINK_BUTTONS['BAD']['callback_data']}:{db_id}",
                ),
            ]
        ]
    )
