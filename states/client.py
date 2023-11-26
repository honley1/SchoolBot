from aiogram.dispatcher.filters.state import State, StatesGroup


class StartFSM(StatesGroup):
    lang = State()
    person = State()
    name = State()
    Class = State()


class ChangeLangFSM(StatesGroup):
    newLang = State()


class AppealFSM(StatesGroup):
    pscZdvr = State()
    cause = State()
    descriptionOfProblem = State()
    Contact = State()


class ConsultationFSM(StatesGroup):
    pscZdvr = State()
    dayOfTheWeek = State()
    timeUser = State()
    Contact = State()