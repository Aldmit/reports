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
            


    def update_data(self, data):
            
        match self._typeData:
            case "users":
                user_id = self._id
                new_login = data._login
                new_name = data._name
                new_role = int(data._role)
                new_clients = data._clients

                try:
                    with sq.connect(self.__bd_name) as conn: # Работа с подключением к БД через встроенный import sq
                        cur = conn.cursor()
                        # request = f"UPDATE {self._typeData} SET `login`={new_login},`name`={new_name},`role`={new_role},`clients_id`={new_clients} WHERE `user_id`={user_id}"
                        # cur.execute(request)

                        # Динамическое формирование SQL-запроса
                        query = f"UPDATE {self._typeData} SET "
                        params = []

                        if new_login is not None:
                            query += "login = ?, "
                            params.append(new_login)
                        if new_name is not None:
                            query += "name = ?, "
                            params.append(new_name)
                        if new_role is not None:
                            query += "role = ?, "
                            params.append(new_role)
                        if new_clients is not None:
                            query += "clients_id = ?, "
                            params.append(new_clients)

                        # Удаляем лишнюю запятую и добавляем условие WHERE
                        query = query.rstrip(", ") + " WHERE user_id = ?"
                        params.append(user_id)

                        # Выполняем запрос
                        cur.execute(query, params)
                        return "Данные успешно изменены"




                except sq.Error as e:
                    return f"Error inserting user: {e}"
                
                return f"Данные успешно изменены"

            
            case 'clients':  
                new_login = data[1]
                new_name = data[2]
                new_ads = data[3]

                try:
                    with sq.connect(self.__bd_name) as conn: # Работа с подключением к БД через встроенный import sq
                        cur = conn.cursor()
                        request = f"UPDATE {self._typeData} SET name={new_name},ads={new_ads} WHERE login={self._login};"
                        cur.execute(request)
                except sq.Error as e:
                    return f"Error inserting user: {e}"
                
                return f"Данные успешно изменены"

            case _:
                return f"Замена не была выполнена"
    


    def insert_data(self):
        match self._typeData:
            case 'user':  
                user_id = self._id
                login = self._login
                name = self._name
                role = self._role
                clients_id = json.dumps({0:" "})

                try:
                    with sq.connect(self.__bd_name) as conn: # Работа с подключением к БД через встроенный import sq
                        cur = conn.cursor()
                        cur.execute("INSERT INTO users(user_id,login,name,role,clients_id) VALUES (?, ?, ?, ?, ?)",
                                    (user_id,login,name,role,clients_id))
                except sq.Error as e:
                    return f"Error inserting user: {e}"
                return f"User has insert: {user_id}, {login}, {name}, {role}"

            case 'client':  
                login = self._login
                name = self._name
                ads = self._ads

                try:
                    with sq.connect(self.__bd_name) as conn: # Работа с подключением к БД через встроенный import sq
                        cur = conn.cursor()
                        cur.execute("INSERT INTO clients(login, name, ads) VALUES (?, ?, ?)",
                                    (login,name,ads))
                except sq.Error as e:
                    return(f"Error inserting client: {e}")
                
                return f"Client has insert: {login}, {name}, {ads}"
            
            case 'budget':  
                client_id = self._clientId
                budget = self._budget
                date = self._date

                try:
                    with sq.connect(self.__bd_name) as conn: # Работа с подключением к БД через встроенный import sq
                        cur = conn.cursor()
                        cur.execute("INSERT INTO budgets(data, client_id, budget) VALUES ('%s', '%s', '%s')" %(date,client_id,budget))
                        
                except sq.Error as e:
                    return(f"Error inserting user: {e}")
                return f"Budget has insert: {client_id}, {budget}"
            
            case 'click':  
                client_id = self._clientId
                clicks = self._clicks
                date = self._date

                try:
                    with sq.connect(self.__bd_name) as conn: # Работа с подключением к БД через встроенный import sq
                        cur = conn.cursor()
                        cur.execute("INSERT INTO clicks(data, client_id, clicks) VALUES ('%s', '%s', '%s')" %(date,client_id,clicks))
                        # conn.commit()
                        # cur.close()
                        # conn.close()
                except sq.Error as e:
                    return(f"Error inserting user: {e}")
                return f"Clicks has insert: {client_id}, {budget}"

            case 'view':  
                client_id = self._clientId
                views = self._views
                date = self._date

                try:
                    with sq.connect(self.__bd_name) as conn:# Работа с подключением к БД через встроенный import sq
                        cur = conn.cursor()
                        cur.execute("INSERT INTO views(data, client_id, views) VALUES ('%s', '%s', '%s')" %(date,client_id,views))
                        # conn.commit()
                        # cur.close()
                        # conn.close()
                        
                except sq.Error as e:
                    return(f"Error inserting user: {e}")
                return f"Views has insert: {client_id}, {views}"
            
            case 'cost':  
                client_id = self._clientId
                costs = self._costs
                date = self._date

                try:
                    with sq.connect(self.__bd_name) as conn: # Работа с подключением к БД через встроенный import sq
                        cur = conn.cursor()
                        cur.execute("INSERT INTO costs(data, client_id, costs) VALUES ('%s', '%s', '%s')" %(date,client_id,costs))
                        # conn.commit()
                        # cur.close()
                        # conn.close()
                        
                except sq.Error as e:
                    return(f"Error inserting user: {e}")
                return f"Costs has insert: {client_id}, {costs}"
            
            case _:
                return f"Uncorrect values."



    
    def create_tables(self) -> None:
        try:
            with sq.connect(self.__bd_name) as conn: # USERS
                cur = conn.cursor()
                cur.execute(f'''CREATE TABLE IF NOT EXISTS users (
                            user_id varchar(100) primary key, 
                            login varchar(100) NOT NULL,
                            name varchar(100) NOT NULL,
                            role TINYINT UNSIGNED NOT NULL,
                            clients_id text,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            )''')
                conn.commit()
                cur.close()
                conn.close()
                print("Tab users has created\n\n")

        except sq.Error as e:
            print(f"Error creating table: {e}")

        try:
            with sq.connect(self.__bd_name) as conn: # CLIENTS
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
        
        except sq.Error as e:
            print(f"Error creating table: {e}")
        
        try:
            with sq.connect(self.__bd_name) as conn:  # BUDGETS
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
        
        except sq.Error as e:
            print(f"Error creating table: {e}")
        
        try:
            with sq.connect(self.__bd_name) as conn:  # CLICKS
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
        
        except sq.Error as e:
            print(f"Error creating table: {e}")

        try:
            with sq.connect(self.__bd_name) as conn: # VIEWS
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
        
        except sq.Error as e:
            print(f"Error creating table: {e}")
 
        try:
            with sq.connect(self.__bd_name) as conn: # COSTS
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

        except sq.Error as e:
            print(f"Error creating table: {e}")



    def delete_data(self):
        match self._typeData:
            case 'user':  
                user_id = self._id

                try:
                    with sq.connect(self.__bd_name) as conn:  # Автоматическое управление подключением
                        cur = conn.cursor()
                        cur.execute("DELETE FROM users WHERE user_id = ?", (user_id))
                        conn.commit() 
                except sq.Error as e:
                    return f"Error deleting client: {e}"
                return f"Client {user_id} has been deleted."

            case 'client':  
                login = self._login
                try:
                    with sq.connect(self.__bd_name) as conn:  # Автоматическое управление подключением
                        cur = conn.cursor()
                        cur.execute("DELETE FROM clients WHERE login = ?", (login))
                        conn.commit() 
                except sq.Error as e:
                    return f"Error deleting client: {e}"
                
                return f"Client {login} has been deleted."