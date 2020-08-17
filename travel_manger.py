from date_parser import DateParser

class TravelManager:
    EXTRA_STATIONS_TO = ('הורדה בגדעונים', 'הגעה - שער יפו')
    EXTRA_STATIONS_BACK = ('יציאה - שער יפו', 'איסוף מגדעונים')

    def __init__(self, date, passengers, passangers_manager, station_manager):
        self.date = date
        self.passengers = passengers

        self.passengers_manager = passangers_manager
        self.station_manager = station_manager

        self.is_sunday = DateParser.is_sunday(date)

    def _get_ordered_passengers(self):
            stations_to_passengers = self._get_stations_to_passengers_map()
            all_stations = self.station_manager.get_stations(self.is_sunday)

            ordered_passengers = []

            i = 1
            for station in all_stations:
                if station in stations_to_passengers:
                    passengers = stations_to_passengers[station]
                    ordered_passengers.extend([(i, passenger) for passenger in passengers])
                    i += 1

            return ordered_passengers
    
    def _get_stations_to_passengers_map(self):
        stations_to_passengers = {}

        for passenger in self.passengers_manager.all_passengers:
            if passenger.name in self.passengers:
                station = passenger.get_station(self.is_sunday)
                assert station, f"Station of {passenger.name} on {self.date} is not available (sunday={self.is_sunday})"

                if station not in stations_to_passengers:
                    stations_to_passengers[station] = []

                stations_to_passengers[station].append(passenger)

        return stations_to_passengers
            
    def get_passengers_records(self):
        for i, passenger in self._get_ordered_passengers():
            station = passenger.get_station(self.is_sunday)
            yield (passenger.name, i, "", station.city, station.name, station.num, passenger.address, passenger.phone)

    def get_records(self):
        if not self.is_sunday:
            for city in TravelManager.EXTRA_STATIONS_BACK:
                yield ('', '', '', city)

        yield from self.get_passengers_records()

        if self.is_sunday:
            for city in TravelManager.EXTRA_STATIONS_TO:
                yield ('', '', '', city)
