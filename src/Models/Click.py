from ..DataAccessLayer.DAL import Database

class Click:
    def __init__(self, id_client, click=0, dateFrom=0, dateTo = 0):
        self._clientId = id_client
        self._click = click
        self._dateFrom = dateFrom
        self._dateTo = dateTo

    
    def add_clicks(self):
        return Database(" ", 'click', [self._clientId, self._view, self._dateFrom]).insert_data()
    
    def get_clicks(self):
        return Database(" ", 'clicks').get_data(self._dateFrom, self._dateTo)

    # def update_clicks(self):
    #     pass
    