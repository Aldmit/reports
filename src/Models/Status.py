from aiogram.fsm.state import StatesGroup, State

# Состояния здесь нужны, чтобы понимать, какие из обработчиков слушать (у обработчиков могут быть одинакоые команды, но нам важно, какой у них при этом статус состояния)
class Status(StatesGroup):
    Mode_ON = State()
    Mode_budgets = State()
    Mode_clients = State()
    Mode_reports = State()
    Mode_OFF = State()
