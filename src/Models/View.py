from ..DataAccessLayer.DAL import Database

class View:
    def __init__(self, id_client, view=0, dateFrom=0, dateTo = 0):
        self._clientId = id_client
        self._view = view
        self._dateFrom = dateFrom
        self._dateTo = dateTo

    
    def add_views(self):
        return Database(" ", 'view', [self._clientId, self._view, self._dateFrom]).insert_data()

    def get_views(self):
        return Database(" ", 'views').get_data(self._dateFrom, self._dateTo)

    # def update_views(self):
    #     pass