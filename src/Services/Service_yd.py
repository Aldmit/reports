import requests
from requests.exceptions import ConnectionError
from time import sleep
import json
import numpy as np
from pandas import Series,DataFrame
import pandas as pd
import os
from config import Yandex, load_ya_config

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', 1000)


clients = [
    "avrorakuhni-spb",
    "dinamikadvizhenia",
    "g-geoservis",
    "happykitchen-ru",
    "happykitchen-spb",
    "kuhni-mf-kitchen-msk",
    "kuhni-mf-kitchen-spb",
    "kuhni-mf-msk",
    "kuhni-mf-spb",
    "kuhnirubika-ru",
    "kuhnirubika-ru-spb",
    "kuhni-sinterio",
    "kuhzavod-ru",
    "kuhzavod-ru-shkafi",
    "kuhzavod-spb-kuhni",
    "logistikz2020",
    "milismebel",
    "milismebel-spb",
    "pmfb2b",
    "profprioritetadwin",
    "prostyeformy",
    "prostyeformy-msk",
    "renckuhni",
    "sdfabrika-spb",
    "sinteriospb2",
    "skatetownmoscow",
    "skatetownspb",
    "tehnospbservis",
    "vmeste-uytno-msk",
    "vmeste-uytno-ru",
    "wowkitchenmsk",
    "wowkitchen-ru2016",
    "zabota-travel-adwin"
]



# Метод для корректной обработки строк в кодировке UTF-8 как в Python 3, так и в Python 2
import sys

if sys.version_info < (3,):
    def u(x):
        try:
            return x.encode("utf8")
        except UnicodeDecodeError:
            return x
else:
    def u(x):
        if type(x) == type(b''):
            return x.decode('utf8')
        else:
            return x

def get_path():
    path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    print(path)
    print(f"{path}/Reports/Client...")

def get_report(clientLogin, mode=0):
    
    path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    if mode == 0:
        config: Yandex = load_ya_config()
        ReportsURL: str = config.yaReportURL
        token: str = config.yaToken


        # Логин клиента рекламного агентства
        # Обязательный параметр, если запросы выполняются от имени рекламного агентства
        # clientLogin = 'avrorakuhni-spb'

        # --- Подготовка запроса ---
        # Создание HTTP-заголовков запроса
        headers = {
                # OAuth-токен. Использование слова Bearer обязательно
                "Authorization": "Bearer " + token,
                # Логин клиента рекламного агентства
                "Client-Login": clientLogin,
                # Язык ответных сообщений
                "Accept-Language": "ru",
                # Режим формирования отчета
                "processingMode": "auto",
                # Формат денежных значений в отчете
                "returnMoneyInMicros": "false",
                # Не выводить в отчете строку с названием отчета и диапазоном дат
                # "skipReportHeader": "true",
                # Не выводить в отчете строку с названиями полей
                # "skipColumnHeader": "true",
                # Не выводить в отчете строку с количеством строк статистики
                # "skipReportSummary": "true"
                }

        # Создание тела запроса
        # Создание тела запроса
        body = {
            "params": {
                "SelectionCriteria": {
                    "DateFrom": "2024-10-11",
                    "DateTo": "2024-11-11"
                },
                "FieldNames": [
                    "Date",
                    "Impressions",
                    "Clicks",
                    "Cost"
                ],
                "ReportName": "Отчёт по клиенту: " + clientLogin,
                "ReportType": "ACCOUNT_PERFORMANCE_REPORT",
                "DateRangeType": "CUSTOM_DATE",
                "Format": "TSV",
                "IncludeVAT": "YES",
                "IncludeDiscount": "NO"
            }
        }
        # Кодирование тела запроса в JSON
        body = json.dumps(body, indent=4)

        # --- Запуск цикла для выполнения запросов ---
        # Если получен HTTP-код 200, то выводится содержание отчета
        # Если получен HTTP-код 201 или 202, выполняются повторные запросы
        while True:
            try:
                req = requests.post(ReportsURL, body, headers=headers)
                req.encoding = 'utf-8'  # Принудительная обработка ответа в кодировке UTF-8
                if req.status_code == 400:
                    print("Параметры запроса указаны неверно или достигнут лимит отчетов в очереди")
                    print("RequestId: {}".format(req.headers.get("RequestId", False)))
                    print("JSON-код запроса: {}".format(u(body)))
                    print("JSON-код ответа сервера: \n{}".format(u(req.json())))
                    break

                elif req.status_code == 200:
                    print("Отчет создан успешно")
                    print("RequestId: {}".format(req.headers.get("RequestId", False)))
                    print("Содержание отчета: \n{}".format(u(req.text)))
                    #создаем csv файл и записываем в него ответ
                    file = open(f"{path}/Reports/{clientLogin}.csv", "w")
                    file.write(req.text)
                    file.close()
                    break
                    
                elif req.status_code == 201:
                    print("Отчет успешно поставлен в очередь в режиме офлайн")
                    retryIn = int(req.headers.get("retryIn", 60))
                    print("Повторная отправка запроса через {} секунд".format(retryIn))
                    print("RequestId: {}".format(req.headers.get("RequestId", False)))
                    sleep(retryIn)

                elif req.status_code == 202:
                    print("Отчет формируется в режиме офлайн")
                    retryIn = int(req.headers.get("retryIn", 60))
                    print("Повторная отправка запроса через {} секунд".format(retryIn))
                    print("RequestId:  {}".format(req.headers.get("RequestId", False)))
                    sleep(retryIn)

                elif req.status_code == 500:
                    print("При формировании отчета произошла ошибка. Пожалуйста, попробуйте повторить запрос позднее")
                    print("RequestId: {}".format(req.headers.get("RequestId", False)))
                    print("JSON-код ответа сервера: \n{}".format(u(req.json())))
                    break

                elif req.status_code == 502:
                    print("Время формирования отчета превысило серверное ограничение.")
                    print("Пожалуйста, попробуйте изменить параметры запроса - уменьшить период и количество запрашиваемых данных.")
                    print("JSON-код запроса: {}".format(body))
                    print("RequestId: {}".format(req.headers.get("RequestId", False)))
                    print("JSON-код ответа сервера: \n{}".format(u(req.json())))
                    break
                
                else:
                    print("Произошла непредвиденная ошибка")
                    print("RequestId:  {}".format(req.headers.get("RequestId", False)))
                    print("JSON-код запроса: {}".format(body))
                    print("JSON-код ответа сервера: \n{}".format(u(req.json())))
                    break

            # Обработка ошибки, если не удалось соединиться с сервером API Директа
            except ConnectionError:
                # В данном случае мы рекомендуем повторить запрос позднее
                print("Произошла ошибка соединения с сервером API")
                # Принудительный выход из цикла
                break

            # Если возникла какая-либо другая ошибка
            except:
                # В данном случае мы рекомендуем проанализировать действия приложения
                print("Произошла непредвиденная ошибка")
                # Принудительный выход из цикла
                break
    else:
        # превращаем ответ в таблицу
        df = pd.read_csv(f"{path}/Reports/{clientLogin}.csv",header=1, sep='\t', index_col=0, encoding="cp1251")
        return df


        




# for name in clients:
#     get_report(ReportsURL, token, name)



# path = os.path.dirname(os.path.realpath(__file__))

# for name in clients:
#     f = pd.read_csv(f"{path}/reports/{name}.csv",header=1, sep='	', index_col=0, encoding='latin-1')
#     # f['Cost'] = f['Cost']/1000000
#     print(f,"\n\n=============================================================================\n")