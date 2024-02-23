from aiogram.fsm.state import StatesGroup, State


class States(StatesGroup):
    top_up = State()
    withdrawal = State()
    change_requisites = State()
    change_commission = State()
    ban_unban = State()
    change_balance = State()
    set_capitalization = State()
    mailing = State()
    requisites = State()
    change_info = State()


