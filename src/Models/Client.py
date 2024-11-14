from ..DataAccessLayer.DAL import Database

class Client:
    def __init__(self, id=0, login=0, name=0, ads=0):
        self._id = id
        self._login = login
        self._name = name
        self._ads = ads 
        self._created = ""


    def get_info(self, param=""):
        match param:
            case "id":
                return self._id
            case "login":
                return self._login
            case "name":
                return self._name
            case "ads":
                return self._id
            case "created":
                return self._id
            case _:
                return lambda x: x in self
    

    def add_stats_of_client(self):
        return Database(self._id, 'client', [self._login, self._name, self._ads]).insert_data()

    def get_stats_of_client(self):
        return Database(self._id, 'clients').get_data()