r"""The Database class has the following methods:

    - get_data(self, data: str) - Получает все данные из таблицы по ключу пользователя и названию таблицы
    - update_data(self, data: str, json_data: str) -> bool - Обновляет таблицу table данными из массива arr
    - insert_user(self) -> None - Добавляет пользователя в базу, создавая запись о нём в таблицы
    - create_tables(self) -> None - Создаёт таблицы users, wordlist, user_dictionary

"""

import sqlite3 as sq
import os
import json

class Database:
    
    def __init__(self, chat_id: str = "", typeData: str = "", requestData:list = []):
        self._id = chat_id
        self._typeData = typeData

        match typeData:
            case "user":
                self._login = requestData[0]
                self._name = requestData[1]
                self._role = int(requestData[2])
            case "client":
                self._login = requestData[0]
                self._name = requestData[1]
                self._ads = int(requestData[2])
            case "budget":
                self._date = requestData[0]
                self._clientId = int(requestData[1])
                self._budget = float(requestData[2])
            case "click":
                self._date = requestData[0]
                self._clientId = int(requestData[1])
                self._clicks = int(requestData[2])
            case "view":
                self._date = requestData[0]
                self._clientId = int(requestData[1])
                self._views = int(requestData[2])
            case "cost":    
                self._date = requestData[0]
                self._clientId = int(requestData[1])
                self._costs = float(requestData[2])
            case _:
                pass

        path = os.path.dirname(os.path.abspath(__file__)) # Получение текущего пути к файлу
        self.__bd_name = os.path.dirname(path)+"/data/database.sql"
        x= 0


    def get_data(self, date_from=0, date_to=0):
        match self._typeData:
            case "users":
                conn = sq.connect(self.__bd_name)
                cur = conn.cursor()
                request = f"SELECT * FROM {self._typeData}"
                cur.execute(request)
                user_data = cur.fetchall()
                cur.close()
                conn.close()
                return user_data
                
            case "clients":
                conn = sq.connect(self.__bd_name)
                cur = conn.cursor()
                request = f"SELECT * FROM {self._typeData}"
                cur.execute(request)
                user_data = cur.fetchall()
                cur.close()
                conn.close()
                return user_data

            case _:
                conn = sq.connect(self.__bd_name)
                cur = conn.cursor()
                request = f"SELECT * FROM {self._typeData} WHERE `date` BETWEEN {date_from} AND {date_to}"
                cur.execute(request)
                user_data = cur.fetchall()
                cur.close()
                conn.close()
                return user_data
            


    def update_data(self) -> str:
        pass
    


    def insert_data(self) -> str:
        match self._typeData:
            case 'user':  
                user_id = self._id
                login = self._login
                name = self._name
                role = self._role
                clients_id = json.dumps({0:" "})

                conn = sq.connect(self.__bd_name) # Работа с подключением к БД через встроенный import sq
                cur = conn.cursor()
                cur.execute("INSERT INTO users(user_id, login, name, role, clients_id) VALUES ('%s', '%s', '%s', '%i', '%s')" %(user_id,login,name,role,clients_id))
                conn.commit()
                cur.close()
                conn.close()
                return f"User has insert: {user_id}, {login}, {name}, {role}, {clients_id}"

            case 'client':  
                login = self._login
                name = self._name
                ads = self._ads

                conn = sq.connect(self.__bd_name) # Работа с подключением к БД через встроенный import sq
                cur = conn.cursor()
                cur.execute("INSERT INTO clients(login, name, ads) VALUES ('%s', '%s', '%i')" %(login,name,ads))
                conn.commit()
                cur.close()
                conn.close()
                return f"Client has insert: {login}, {name}, {ads}"
            
            case 'budget':  
                client_id = self._clientId
                budget = self._budget
                date = self._date

                conn = sq.connect(self.__bd_name) # Работа с подключением к БД через встроенный import sq
                cur = conn.cursor()
                cur.execute("INSERT INTO budgets(data, client_id, budget) VALUES ('%s', '%s', '%s')" %(date,client_id,budget))
                conn.commit()
                cur.close()
                conn.close()
                return f"Budget has insert: {client_id}, {budget}"
            
            case 'click':  
                client_id = self._clientId
                clicks = self._clicks
                date = self._date

                conn = sq.connect(self.__bd_name) # Работа с подключением к БД через встроенный import sq
                cur = conn.cursor()
                cur.execute("INSERT INTO clicks(data, client_id, clicks) VALUES ('%s', '%s', '%s')" %(date,client_id,clicks))
                conn.commit()
                cur.close()
                conn.close()
                return f"Clicks has insert: {client_id}, {budget}"

            case 'view':  
                client_id = self._clientId
                views = self._views
                date = self._date

                conn = sq.connect(self.__bd_name) # Работа с подключением к БД через встроенный import sq
                cur = conn.cursor()
                cur.execute("INSERT INTO views(data, client_id, views) VALUES ('%s', '%s', '%s')" %(date,client_id,views))
                conn.commit()
                cur.close()
                conn.close()
                return f"Views has insert: {client_id}, {views}"
            
            case 'cost':  
                client_id = self._clientId
                costs = self._costs
                date = self._date

                conn = sq.connect(self.__bd_name) # Работа с подключением к БД через встроенный import sq
                cur = conn.cursor()
                cur.execute("INSERT INTO costs(data, client_id, costs) VALUES ('%s', '%s', '%s')" %(date,client_id,costs))
                conn.commit()
                cur.close()
                conn.close()
                return f"Costs has insert: {client_id}, {costs}"
            
            case _:
                return f"Uncorrect values."



    
    def create_tables(self) -> None:

        conn = sq.connect(self.__bd_name) # USERS
        cur = conn.cursor()
        cur.execute(f'''CREATE TABLE IF NOT EXISTS users (
                    user_id varchar(100) primary key, 
                    login varchar(100) NOT NULL,
                    name varchar(100) NOT NULL,
                    role TINYINT UNSIGNED NOT NULL,
                    clients_id varchar(65535),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )''')
        conn.commit()
        cur.close()
        conn.close()
        print("Tab users has created\n\n")

        
        conn = sq.connect(self.__bd_name) # CLIENTS
        cur = conn.cursor()
        cur.execute(f'''CREATE TABLE IF NOT EXISTS clients (
                    id int UNSIGNED AUTO_INCREMENT PRIMARY KEY, 
                    login varchar(200) NOT NULL,
                    name varchar(200) NOT NULL,
                    ads tinyint NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )''')
        conn.commit()
        cur.close()
        conn.close()
        print("Tab clients has created\n\n")
        
        
        conn = sq.connect(self.__bd_name) # BUDGETS
        cur = conn.cursor()
        cur.execute(f'''CREATE TABLE IF NOT EXISTS budgets (
                    id int UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                    date DATE NOT NULL,
                    client_id int NOT NULL,
                    budget decimal(13,2)
                    )''')
        conn.commit()
        cur.close()
        conn.close()
        print("Tab budgets has created\n\n")
        
        
        conn = sq.connect(self.__bd_name) # CLICKS
        cur = conn.cursor()
        cur.execute(f'''CREATE TABLE IF NOT EXISTS clicks (
                    id int UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                    date DATE NOT NULL,
                    client_id int NOT NULL,
                    clicks int
                    )''')
        conn.commit()
        cur.close()
        conn.close()
        print("Tab clicks has created\n\n")

        
        conn = sq.connect(self.__bd_name) # VIEWS
        cur = conn.cursor()
        cur.execute(f'''CREATE TABLE IF NOT EXISTS views (
                    id int UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                    date DATE NOT NULL,
                    client_id int NOT NULL,
                    views int
                    )''')
        conn.commit()
        cur.close()
        conn.close()
        print("Tab views has created\n\n")

        
        conn = sq.connect(self.__bd_name) # COSTS
        cur = conn.cursor()
        cur.execute(f'''CREATE TABLE IF NOT EXISTS costs (
                    id int UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                    date DATE NOT NULL,
                    client_id int NOT NULL,
                    costs decimal(13,2)
                    )''')
        conn.commit()
        cur.close()
        conn.close()
        print("Tab costs has created\n\n")

        