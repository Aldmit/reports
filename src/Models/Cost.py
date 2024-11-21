from ..DataAccessLayer.DAL import Database

class Cost:
    def __init__(self, id_client, cost=0, dateFrom=0, dateTo = 0):
        self._clientId = id_client
        self._cost = cost
        self._dateFrom = dateFrom
        self._dateTo = dateTo


    def add_costs(self):
        return Database(" ", 'cost', [self._clientId, self._cost, self._dateFrom]).insert_data()
    
    def get_costs(self):
        return Database(" ", 'costs').get_data(self._dateFrom, self._dateTo)

    # def update_costs(self):
    #     pass
