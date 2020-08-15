from csv_loadable import CSVLoadable

class StationManager:
    def __init__(self):
        self._stations_to_manager = SingleDirectionStationsManager('data/stations_to.csv')
        self._stations_back_manager = SingleDirectionStationsManager('data/stations_back.csv')
        
    def get_stations(self, is_sunday):
        return self._stations_to_manager.get_stations() if is_sunday else self._stations_back_manager.get_stations()
    
    def get_to(self, city):
        return self._stations_to_manager._get(city)

    def get_back(self, city):
        return self._stations_back_manager._get(city)


class SingleDirectionStationsManager(CSVLoadable):
    def __init__(self, csv_path):
        self._csv_path = csv_path
        self._cities = {}

        self.load()
    
    def get_stations(self):
        return [station for city in self._cities.values() for station in city._stations]

    def add(self, station_city, station_name, station_num):
        if station_city in self._cities:
            self._cities[station_city].add(station_name, station_num)
        
        else:
            self._cities[station_city] = City(station_city, station_name, station_num)

    def _get(self, station_city):
        try:
            if ': ' in station_city:
                station_city, station_name = station_city.split(': ')
                return self._cities[station_city].get(station_name)

            else:
                return self._cities[station_city].get()
        
        except KeyError:
            return None  # might be unnecessary, will lead to exception only if necessary


class City:
    def __init__(self, city, name, num):
        self.city = city

        self._stations = []
        self.add(name, num)
    
    def add(self, name, num):
        self._stations.append(Station(self.city, name, num))
    
    def get(self, *args):
        if len(args) > 0:
            station_name, *_ = args
            return self._get_station(station_name)

        else:    
            return self._stations[0]

    def _get_station(self, station_name):
        for station in self._stations:
            if station.name == station_name:
                return station
        
        raise KeyError(f"{station_name} not found.")


class Station:
    def __init__(self, city, name, num):
        self.city = city
        self.name = name
        self.num = num
