from aiogram.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    count = State()
