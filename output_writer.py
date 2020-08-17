import csv

from date_parser import DateParser

ENCODING = 'utf-8-sig'

class TravelOutputWriter:
    EXTRA_STATIONS_TO = ('הורדה בגדעונים', 'הגעה - שער יפו')
    EXTRA_STATIONS_BACK = ('יציאה - שער יפו', 'איסוף מגדעונים')

    def __init__(self, date, passengers):
        self.date = date
        self.passengers = passengers
        self.is_sunday = DateParser.is_sunday(date)

    def export_to_csv(self):
        with open(f'travels/travel-{self.date}.csv', 'w', newline='', encoding=ENCODING) as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')

            csv_header = ('שם', 'מספר תחנה', 'שעה מוערכת', 'עיר', 'תחנה', 'מזהה תחנה', 'כתובת מגורים', 'טלפון')
            csv_writer.writerow(csv_header)

            for record in self._get_records():
                csv_writer.writerow(record)
            
            csv_writer.writerow((tuple()))
            csv_writer.writerow(('מספר הנוסעים:', len(list(self._get_passengers_records()))))
            csv_writer.writerow(('מפקד הנסיעה:',))

    def _get_records(self):
        if not self.is_sunday:
            for city in TravelOutputWriter.EXTRA_STATIONS_BACK:
                yield ('', '', '', city)

        yield from self._get_passengers_records()

        if self.is_sunday:
            for city in TravelOutputWriter.EXTRA_STATIONS_TO:
                yield ('', '', '', city)

    def _get_passengers_records(self):
        for i, passenger in self.passengers.get_travel_passengers_list():
            station = passenger.get_station(self.is_sunday)
            yield (passenger.name, i, "", station.city, station.name, station.num, passenger.address, passenger.phone)
