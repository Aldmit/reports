from aiogram.fsm.state import StatesGroup, State

# Состояния здесь нужны, чтобы понимать, какие из обработчиков слушать (у обработчиков могут быть одинакоые команды, но нам важно, какой у них при этом статус состояния)
class Status(StatesGroup):
    Mode_ON = State()
    Mode_OFF = State()


    Mode_budgets = State()

    
    Mode_clients = State()
    Mode_clients_show = State()
    Mode_clients_create = State()
    Mode_clients_update = State()
    Mode_clients_delete = State()
    

    Mode_reports = State()
    Mode_reports_download = State()
    Mode_reports_yesterday = State()
    Mode_reports_lastweek = State()
    Mode_reports_lastmonth = State()

    Mode_reports_custom_input = State()
    Mode_reports_custom_output = State()
    

    Mode_users = State()
    Mode_users_show = State()
    Mode_users_create = State()
    Mode_users_update = State()
    Mode_users_delete = State()
    Mode_users_showclients = State()
    Mode_users_addclient = State()
    Mode_users_remclient = State()