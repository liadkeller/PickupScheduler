from date_parser import DateParser
from output_writer import TravelOutputWriter

class Travel:
    def __init__(self, date, passengers_names, passangers_manager, station_manager):
        self.date = date
        self.passengers_names = passengers_names
        self.is_sunday = DateParser.is_sunday(date)

        self.passengers_manager = passangers_manager
        self.station_manager = station_manager

        self.passengers = TravelPassengers(date, passengers_names, passangers_manager, station_manager)
    
    def export_to_csv(self):
        TravelOutputWriter(self.date, self.passengers).export_to_csv()


class TravelPassengers:
    def __init__(self, date, passengers_names, passangers_manager, station_manager):
        self.date = date
        self.passengers_names = passengers_names
        self.is_sunday = DateParser.is_sunday(date)

        self.passengers_manager = passangers_manager
        self.station_manager = station_manager

    def get_travel_passengers_list(self):
        """
        Return an ordered list of tuples with the passengers and their station number
        """
        stations_to_passengers = self._get_stations_to_passengers_map()
        all_stations = self.station_manager.get_stations(self.is_sunday)
        travel_stations = [station for station in all_stations if station in stations_to_passengers]

        ordered_passengers = []
        for i, station in enumerate(travel_stations, start=1):
            passengers = stations_to_passengers[station]
            ordered_passengers.extend([(i, passenger) for passenger in passengers])
        
        return ordered_passengers
    
    def _get_stations_to_passengers_map(self):
        """
        Returns a mapping from each stations in the travel to its passengers
        """
        stations_to_passengers = {}

        for passenger in self.passengers_manager.all_passengers:
            if passenger.name in self.passengers_names:
                station = passenger.get_station(self.is_sunday)
                assert station, f"Station of {passenger.name} on {self.date} is not available (sunday={self.is_sunday})"

                if station not in stations_to_passengers:
                    stations_to_passengers[station] = []

                stations_to_passengers[station].append(passenger)

        return stations_to_passengers
