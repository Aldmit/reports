from ..DataAccessLayer import Database
import json

#тут нужно реализовать модуль по работе с системным временем, чтобы получать даты по умолчанию и для дат формата -7 дней

from . import Client

class User:
    def __init__(self, id=0, login=0, name=0, role=0, clients=[], created=""):
        self._id = str(id)
        self._login = login
        self._name = name
        self._role = role
        self._clients = clients
        self._created = created




    def get_statistics(self):
        stats_data = list()
        for i in self._clients:
            # stats_data.append([View(i,)])
            pass
        
        
    def get_users_clients(self):
        users = User().get_users()
        clients = list()
        text = ""
        for user in users:
            text += f'<b>{user[1]} - ({user[0]})</b>:\n'
            clients = (User(user[0]).get_clients())
            for i in clients:
                text += f'▶ {i}\n'
            text += '\n'
        return text


    def get_clients(self):
        clients_list = list()
        user = User(self._id).get_current_user_info()
        clients = json.loads(user._clients)
        for client in clients:
            if client != '0':
                clients_list.append(clients[client]) # тут надо смотреть чё выдаёт
                print(clients_list)
        return clients_list
    


    def add_user(self):
        return Database(self._id, "user", [self._login, self._name, self._role]).insert_data()
        

    def add_client(self):
        user = User(self._id).get_current_user_info()
        clients = json.loads(user._clients)
        clients.update({
            len(clients.keys()):self._login
        })
        user._clients = json.dumps(clients)
        User(self._id).update_user(user)
        return "Информация пользователя обновлена"



    def update_user(self, user):
        return Database(self._id,"users").update_data(user)

    def get_users(self):
        return  Database(self._id,"users").get_data()
    

    def get_current_user_info(self):
        users = Database(self._id, "users").get_data()
        for user in users:
            if user[0] == self._id:
                return User(user[0],user[1],user[2],user[3],user[4],user[5])
        return (False, "Пользователь не найден")

    
    def create_user(self): # Отличается от add_user() тем, что может создавать модераторов и администраторов
        return Database(self._id,"user",[self._login, self._name, self._role]).insert_data()
    

# class Moderator(User):
#     def get_users(self):
#         pass

#     def add_user(self):
#         pass

#     def update_user(self):
#         pass

#     def remove_user(self):
#         pass



#     def add_client(self):
#         pass

#     def update_client(self):
#         pass

#     def remove_client(self):
#         pass



#     def get_clients_of_user(self):
#         pass

#     def add_client_to_user(self):
#         pass

#     def remove_client_of_user(self):
#         pass


# class Administrator(User, Moderator):
#     def create_user(self): # Отличается от add_user() тем, что может создавать модераторов и администраторов
#         pass






