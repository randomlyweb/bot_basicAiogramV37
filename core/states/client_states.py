from aiogram.fsm.state import State, StatesGroup


class TimeState(StatesGroup):
    time = State()