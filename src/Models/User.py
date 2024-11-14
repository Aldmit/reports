from ..DataAccessLayer import Database

#тут нужно реализовать модуль по работе с системным временем, чтобы получать даты по умолчанию и для дат формата -7 дней

from . import Client

class User:
    def __init__(self, id, login, name, role):
        self._id = id
        self._login = login
        self._name = name
        self._role = role
        self._clients = []
        self._created = ""

    def get_statistics(self):
        stats_data = list()
        for i in self._clients:
            # stats_data.append([View(i,)])
            pass
        

    def get_clients(self):
        clients_list = list()
        all_clients = Client().get_stats_of_client()
        if self._clients in all_clients:
            clients_list.append(all_clients) # тут надо смотреть чё выдаёт

        return clients_list

    def add_user(self):
        return Database(self._id, "user", [self._login, self._name, self._role]).insert_data()
        

    def add_client(self, login: str, name: str, ads: int):
        return Client("",login,name,ads).add_stats_of_client()

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






