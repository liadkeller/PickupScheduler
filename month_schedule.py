from date_parser import DateParser
from csv_loadable import CSVLoadable

class MonthSchedule(CSVLoadable):
    def __init__(self, month, year):
        self.dates_parser = DateParser(month, year)
        self._csv_path = 'data/month.csv'

        self._passenger_to_dates_map = {}
        self._date_to_passengers_map = {date: [] for date in self.dates_parser.all_dates()}

        self.load()
    
    @property
    def dates(self):
        return list(self._date_to_passengers_map.keys())
    
    def get_passengers(self, date):
        return self._date_to_passengers_map[date]

    def add(self, name, dates_request):
        dates = self.parse_dates(dates_request)

        self._passenger_to_dates_map[name] = dates
        for date in dates:
            self._date_to_passengers_map[date].append(name)
    
    def parse_dates(self, dates_request):
        return self.dates_parser.parse_dates(dates_request)
