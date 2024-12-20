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
from src.Models.Client import Client


# Инициализируем роутер уровня модуля
router = Router()



@router.callback_query(F.data == "clients_mode")
async def start_chinese_train_1(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Status.Mode_clients)
    
    def get_keyboard():
            buttons = [
                [types.InlineKeyboardButton(text="Показать всех клиентов", callback_data="show_clients")],
                [types.InlineKeyboardButton(text="Добавить клиента", callback_data="add_clients")],
                # [types.InlineKeyboardButton(text="Обновить текущего клиента", callback_data="update_clients")],
                [types.InlineKeyboardButton(text="Удалить клиента", callback_data="rem_clients")]
            ]
            keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
            return keyboard
    
    await callback.message.answer(f"Выберите необходимую функцию из предложенных ниже.", reply_markup=get_keyboard())



@router.callback_query(F.data == "show_clients")
async def start_chinese_train_1(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Status.Mode_clients_show)

    clients = Client(callback.from_user.id).get_clients()
    answer = ""
    ads = ""
    for client in clients:
        match client[3]:
            case 1:
                ads = "yandex"
            case 2:
                ads = "vk"
            case _:
                pass   
             
        answer += f"<b>Название</b>: {client[2]}\n{client[1]} | {ads}\n\n" 
    await callback.message.answer(f"<b>Список текущих клиентов:</b>\n{answer}")



    
@router.callback_query(F.data == "add_clients")
async def start_chinese_train_1(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Status.Mode_clients_create)
    await callback.message.answer(f"Введите ниже данные клиента, которого необходимо добавить. \n\nДанные следует вводить следующим образом:\nclient_login client_name client_ads\n\nlogin - логин клиентского кабинета\nname - имя для отображения\nads - рекламная система (yandex, vk)\n\nПример:\nbeautywindows_spb Красивые_окна_СПБ yandex")


@router.message(Status.Mode_clients_create, F.text)
async def get_message_base(message: types.Message, bot: Bot, state: FSMContext):
    # (message.from_user.username, message.chat.id)
    split_message = message.text.split(' ', maxsplit=2)

    try:
        if split_message[0] is None:
            await message.answer("Ошибка: переданы не все аргументы")
            return
        match split_message[2]:
            case "yandex":
                split_message[2] = 1
            case "vk":
                split_message[2] = 2
            case _:
                pass
        request = Client(split_message[0],split_message[1],split_message[2]).create_client()
        await message.answer(request)

    except:
        await message.answer(
            "Ошибка: неправильный формат ввода. Попробуйте ещё раз:\n"
            "user_chat_id @tg_login name role"
        )
        return
    


    
@router.callback_query(F.data == "rem_clients")
async def start_chinese_train_1(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Status.Mode_clients_delete)
    await callback.message.answer(f"Введите ниже логин клиента и рекламную систему, которого необходимо удалить. \n\nДанные следует вводить следующим образом:\nclient_login ads\n\nlogin - логин клиентского кабинета\nads - рекламная система (yandex, vk)\n\nПример:\nbeautywindows_spb yandex")


@router.message(Status.Mode_clients_delete, F.text)
async def get_message_base(message: types.Message, bot: Bot, state: FSMContext):
    # (message.from_user.username, message.chat.id)
    split_message = message.text.split(' ', maxsplit=1)

    try:
        if split_message[0] is None:
            await message.answer("Ошибка: переданы не все аргументы")
            return
        match split_message[1]:
            case "yandex":
                split_message[1] = 1
            case "vk":
                split_message[1] = 2
            case _:
                pass
        request = Client(split_message[0],split_message[1],split_message[2]).delete_client()
        await message.answer(request)
        await state.set_state(Status.Mode_clients)      
        return
    except:
        await message.answer(
            "Ошибка: неправильный формат ввода. Попробуйте ещё раз:\n"
            "user_chat_id @tg_login name role"
        )
        return
    