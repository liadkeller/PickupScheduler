from month_schedule import MonthSchedule
from passengers_manager import PassengersManager
from station_manager import StationManager
from travel import Travel

def main():
    month_schedule = MonthSchedule(8, 2020)

    station_manager = StationManager()
    passengers_manager = PassengersManager(station_manager)

    for date in month_schedule.dates[4:]:
        travel = Travel(date, month_schedule.get_passengers(date), passengers_manager, station_manager)
        travel.export_to_csv()


if __name__ == "__main__":
    main()