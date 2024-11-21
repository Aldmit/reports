from aiogram import Bot, types
from aiogram import F # магические функции - позволяют вытаскивать всю нужную инфу с минимумом кода

from aiogram.filters.command import Command, CommandObject, CommandStart # Позволяет ловить команды в обработчик по схеме Command('команда')
from aiogram.types import Message,MessageEntity,FSInputFile, URLInputFile, BufferedInputFile, InputTextMessageContent, InlineQueryResultArticle # Работа с файлами
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from aiogram.utils.keyboard import ReplyKeyboardBuilder # Подстрочные кнопки
from aiogram.utils.keyboard import InlineKeyboardBuilder # Инлайновые кнопки

from aiogram import Router
from src.Models.Status import Status
from src.Models.User import User
from config import Config, load_admin_id


# Инициализируем роутер уровня модуля
router = Router()



@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.set_state(Status.Mode_ON)

    await message.answer(f"Добро пожаловать в Adwin Reports Bot. Ваш пользовательский идентификатор: {message.chat.id}")
    
    try:
        config: Config = load_admin_id()
        ADMIN_ID: str = config
        if str(message.chat.id) == ADMIN_ID: # id чата администратора
            def get_keyboard():
                buttons = [
                    # [types.InlineKeyboardButton(text="Работа с планами", callback_data="budgets_mode")],
                    [types.InlineKeyboardButton(text="Работа с клиентами", callback_data="clients_mode")],
                    [types.InlineKeyboardButton(text="Работа с пользователями", callback_data="users_mode")],
                    [types.InlineKeyboardButton(text="Получить статистику", callback_data="reports_mode")]
                ]
                keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
                return keyboard
            await message.answer(f"Выберите что нужно сделать", reply_markup=get_keyboard())

                
        user = User(message.chat.id).get_current_user_info()
        if int(user._id) != message.chat.id:
            await message.answer("Для использования сервиса необходимо запросить регистрацию у администратора.")
            return
        
        match user._role:
            case 0: # Сотрудник
                def get_keyboard():
                        buttons = [
                            [types.InlineKeyboardButton(text="Обновить всю статистику за 3 мес", callback_data="all_stats")],
                            [types.InlineKeyboardButton(text="Получить статистику за прошлый день", callback_data="yesterday")],
                            # [types.InlineKeyboardButton(text="Получить статистику за прошлую неделю", callback_data="last_week")],
                            # [types.InlineKeyboardButton(text="Получить статистику за прошлый месяц", callback_data="last_month")],
                            [types.InlineKeyboardButton(text="Получить статистику за период (сумма)", callback_data="custom_date")]

                        ]
                        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
                        return keyboard
                await message.answer(f"Выберите, что хотите сделать со статистикой", reply_markup=get_keyboard())


            case 1: # Модератор
                def get_keyboard():
                    buttons = [
                        # [types.InlineKeyboardButton(text="Работа с планами", callback_data="budgets_mode")],
                        [types.InlineKeyboardButton(text="Работа с клиентами", callback_data="clients_mode")],
                        [types.InlineKeyboardButton(text="Работа с пользователями", callback_data="users_mode")],
                        [types.InlineKeyboardButton(text="Получить статистику", callback_data="reports_mode")],
                    ]
                    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
                    return keyboard
                await message.answer(f"Выберите что нужно сделать", reply_markup=get_keyboard())

                  
            case 2: # Администратор
                pass
                  

            case _:
                await message.answer("Что-то пошло не так, обратитесь к администратору для проверки.")

                  
    except Exception:
        await message.answer("Для использования сервиса необходимо запросить регистрацию у администратора.")
        return
    
    
@router.message(Command("menu"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.set_state(Status.Mode_ON)
    try:
        config: Config = load_admin_id()
        ADMIN_ID: str = config
        if str(message.chat.id) == ADMIN_ID: # id чата администратора
            def get_keyboard():
                buttons = [
                    # [types.InlineKeyboardButton(text="Работа с планами", callback_data="budgets_mode")],
                    [types.InlineKeyboardButton(text="Работа с клиентами", callback_data="clients_mode")],
                    [types.InlineKeyboardButton(text="Работа с пользователями", callback_data="users_mode")],
                    [types.InlineKeyboardButton(text="Получить статистику", callback_data="reports_mode")]
                ]
                keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
                return keyboard
            await message.answer(f"Выберите что нужно сделать", reply_markup=get_keyboard())

                
        user = User(message.chat.id).get_current_user_info()
        if int(user._id) != message.chat.id:
            await message.answer("Для использования сервиса необходимо запросить регистрацию у администратора.")
            return
        
        match user._role:
            case 0: # Сотрудник
                def get_keyboard():
                        buttons = [
                            [types.InlineKeyboardButton(text="Обновить всю статистику за 3 мес", callback_data="all_stats")],
                            [types.InlineKeyboardButton(text="Получить статистику за прошлый день", callback_data="yesterday")],
                            # [types.InlineKeyboardButton(text="Получить статистику за прошлую неделю", callback_data="last_week")],
                            # [types.InlineKeyboardButton(text="Получить статистику за прошлый месяц", callback_data="last_month")],
                            [types.InlineKeyboardButton(text="Получить статистику за период (сумма)", callback_data="custom_date")]

                        ]
                        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
                        return keyboard
                await message.answer(f"Выберите, что хотите сделать со статистикой", reply_markup=get_keyboard())


            case 1: # Модератор
                def get_keyboard():
                    buttons = [
                        # [types.InlineKeyboardButton(text="Работа с планами", callback_data="budgets_mode")],
                        [types.InlineKeyboardButton(text="Работа с клиентами", callback_data="clients_mode")],
                        [types.InlineKeyboardButton(text="Работа с пользователями", callback_data="users_mode")],
                        [types.InlineKeyboardButton(text="Получить статистику", callback_data="reports_mode")],
                    ]
                    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
                    return keyboard
                await message.answer(f"Выберите что нужно сделать", reply_markup=get_keyboard())

                
            case 2: # Администратор
                pass
                

            case _:
                await message.answer("Что-то пошло не так, обратитесь к администратору для проверки.")

                
    except Exception:
        await message.answer("Для использования сервиса необходимо запросить регистрацию у администратора.")
        return

    

