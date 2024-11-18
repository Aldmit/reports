from ..DataAccessLayer.DAL import Database

class Client:
    def __init__(self, login=0, name=0, ads=0, created=""):
        self._login = login
        self._name = name
        self._ads = ads 
        self._created = created


    def get_current_client_info(self):
        clients = Database(self._login, "clients").get_data()
        for client in clients:
            if client[1] == self._login:
                return Client(client[1],client[2],client[3],client[4])
        return (False, "Клиент не найден")

    def create_client(self):
        return Database("", 'client', [self._login, self._name, self._ads]).insert_data()

    def get_clients(self):
        return Database("", 'clients').get_data()