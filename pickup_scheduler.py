import csv

from month_schedule import MonthSchedule
from passengers_manager import PassengersManager
from station_manager import StationManager
from travel_manger import TravelManager

ENCODING = 'utf-8-sig'

def export_travel_to_csv(travel_manager):
    with open(f'travels/travel-{travel_manager.date}.csv', 'w', newline='', encoding=ENCODING) as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')

        csv_header = ('שם', 'מספר תחנה', 'שעה מוערכת', 'עיר', 'תחנה', 'מזהה תחנה', 'כתובת מגורים', 'טלפון')
        csv_writer.writerow(csv_header)

        for record in travel_manager.get_records():
            csv_writer.writerow(record)
        
        csv_writer.writerow((tuple()))
        csv_writer.writerow(('מספר הנוסעים:', len(travel_manager.passengers)))
        csv_writer.writerow(('מפקד הנסיעה:',))


def main():
    month_schedule = MonthSchedule(8, 2020)

    station_manager = StationManager()
    passengers_manager = PassengersManager(station_manager)

    for date in month_schedule.dates[4:]:
        travel_manager = TravelManager(date, month_schedule.get_passengers(date), passengers_manager, station_manager)
        export_travel_to_csv(travel_manager)



if __name__ == "__main__":
    main()