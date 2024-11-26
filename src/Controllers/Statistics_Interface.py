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
from src.Models.User import User

from src.Services import Service_yd
import numpy as np
from pandas import Series,DataFrame
import pandas as pd
import math

from datetime import datetime, timedelta


# Инициализируем роутер уровня модуля
router = Router()



@router.callback_query(F.data == "reports_mode")
async def start_chinese_train_1(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Status.Mode_reports)
    
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
    await callback.message.answer(f"Выберите что хотите сделать со статистикой", reply_markup=get_keyboard())



@router.callback_query(F.data == "all_stats")
async def start_chinese_train_1(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Status.Mode_reports_download)

    clients = Client().get_clients()

    for client in clients:
        # (None, 'avrorakuhni-spb', 'АврораСПБ', 'yandex', '2024-11-16 12:17:39')
        match client[3]:
            case "yandex":
                Service_yd.get_report(client[1])
            case "vk":
                # Service_vk.get_report(client[1])
                pass
            case _:
                pass
        
    await callback.message.answer(f"Статистика за 3 месяца обновлена.")



@router.callback_query(F.data == "yesterday")
async def start_chinese_train_1(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Status.Mode_reports_yesterday)
    
    user_clients = User(callback.from_user.id).get_clients()
    clients_info = list() 

    for client in user_clients:
        clients_info.append(Client(client).get_current_client_info())

    def get_keyboard():
            buttons = []
            for client_info in clients_info:
                # client_info - объект
                buttons.append([types.InlineKeyboardButton(text=client_info._name, callback_data=client_info._login)])
            
            keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
            return keyboard
    
    await callback.message.answer(f"Выберите клиента по которому требуется показать данные.\n Вам доступны следующие клиенты:", reply_markup=get_keyboard())


@router.callback_query(Status.Mode_reports_yesterday,  F.data)
async def start_chinese_train_1(callback: types.CallbackQuery, state: FSMContext):
    clients = Client().get_clients()
    for client in clients:
        if callback.data in client[1]:

            yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

            df = Service_yd.get_report(client[1], 1)
            x = df.loc[[yesterday],['Impressions', 'Clicks', 'Cost']]

            view = int(x.iloc[0,0])
            click = int(x.iloc[0,1])
            cost =x.iloc[0,2]
            cpc = cost/click

            await callback.message.answer(f"Данные по клиенту {client[2]} на {yesterday}:\nПросмотры: {view} \nКлики: {click} \nРасход: {cost} \nСРС: {math.round(cpc,2)}")




@router.callback_query(F.data == "custom_date")
async def start_chinese_train_1(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Status.Mode_reports_custom_input)
    await callback.message.answer(f"Введите две даты ОТ и ДО, в диапазоне которых вы хотите получить выгрузку данных.\nФормат: YYYY-MM-DD YYYY-MM-DD" )
    

@router.message(Status.Mode_reports_custom_input, F.text)
async def get_message_base(message: types.Message, bot: Bot, state: FSMContext):
    await state.set_state(Status.Mode_reports_custom_output)
    split_message = message.text.split(' ', maxsplit=1)

    try:
        if split_message[0] is None:
            await message.answer("Ошибка: переданы не все аргументы")
            return
        
        clients = Client().get_clients()

        for client in clients:
            # (None, 'avrorakuhni-spb', 'АврораСПБ', 'yandex', '2024-11-16 12:17:39')
            client[1]
        
        # for client in clients:
        #     if callback.data in client[1]:

        #     yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

        #     df = Service_yd.get_report(client[1], 1)
        #     x = df.loc[[yesterday],['Impressions', 'Clicks', 'Cost']]

        #     view = int(x.iloc[0,0])
        #     click = int(x.iloc[0,1])
        #     cost =x.iloc[0,2]
        #     cpc = cost/click

        #     await callback.message.answer(f"Данные по клиенту {client[2]} на {yesterday}:\nПросмотры: {view} \nКлики: {click} \nРасход: {cost} \nСРС: {math.round(cpc,2)}")


        # user = User(split_message[0]).get_current_user_info()
        # client = Client(split_message[1]).get_current_client_info()

        # request = User(user._id, client._login).add_client()
        # user = User(message.chat.id).get_current_user_info()
        # await message.answer(f"{request}.")
        
        return
    
    except:
        await message.answer(
            "Ошибка: неправильный формат ввода.\nПопробуйте ещё раз:\n"
            "YYYY-MM-DD YYYY-MM-DD"
        )
        return




# @router.callback_query(Status.Mode_reports, F.data)
# async def start_chinese_train_1(callback: types.CallbackQuery, state: FSMContext):
#     await state.set_state(Status.Mode_reports_custom_input)
#     clients = Client().get_clients()
#     for client in clients:
#         if callback.data in client[1]:

#             yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

#             df = Service_yd.get_report(client[1], 1)
#             x = df.loc[[yesterday],['Impressions', 'Clicks', 'Cost']]

#             view = int(x.iloc[0,0])
#             click = int(x.iloc[0,1])
#             cost =x.iloc[0,2]
#             cpc = cost/click

#             await callback.message.answer(f"Данные по клиенту {client[2]} на {yesterday}:\nПросмотры: {view} \nКлики: {click} \nРасход: {cost} \nСРС: {math.round(cpc,2)}")

