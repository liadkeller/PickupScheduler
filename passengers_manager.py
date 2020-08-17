from csv_loadable import CSVLoadable

class PassengersManager(CSVLoadable):
    def __init__(self, station_manager):
        self.station_manager = station_manager
        self.all_passengers = []
        self._csv_path = 'data/passengers.csv'

        self.load()

    def add(self, name, address, phone, *stations):
        city_to, city_back = self._fetch_stations(*stations)

        station_to = self.station_manager.get_to(city_to)
        station_back = self.station_manager.get_back(city_back)

        self.all_passengers.append(Passenger(name, address, phone, station_to, station_back))

    @staticmethod
    def _fetch_stations(*stations):
        city_to, city_back = stations

        if not city_back:
            city_back = city_to
        
        return city_to, city_back


class Passenger:
    def __init__(self, name, address, phone, station_to, station_back):
        self.name = name
        self.address = address
        self.phone = phone
        self._station_to = station_to
        self._station_back = station_back
    
    def get_station(self, is_sunday):
        return self._station_to if is_sunday else self._station_back
