from aiogram.fsm.state import State, StatesGroup


class LocationState(StatesGroup):
    name = State()
    link = State()
    address = State()


class QuizState(StatesGroup):
    name = State()
    link = State()


class CategoryState(StatesGroup):
    name = State()


class RePeakState(StatesGroup):
    text = State()
    categories = State()
    date = State()


class ChoiceState(StatesGroup):
    choice = State()
    new_string = State()


class ReWriteQuizName(StatesGroup):
    name = State()
    link = State()


class ReWriteLocation(StatesGroup):
    name = State()
    link = State()
    address = State()