from datetime import date, timedelta

class DateParser:
    WEEK = 7
    
    SUNDAY = 6
    THURSDAY = 3

    NO_PREFIX_INDEX = 1

    def __init__(self, month, year):
        self.month = month
        self.year = year
    
    @staticmethod
    def is_sunday(date):
        return date.weekday() == DateParser.SUNDAY

    def parse_dates(self, dates_request):
        all_index = dates_request.find('all')
        no_index = dates_request.find('no')
        plus_index = dates_request.find('plus')

        if all_index > -1:
            all_params = dates_request[all_index:]
            no_params = dates_request[no_index:plus_index] if plus_index > no_index else dates_request[no_index:]
            plus_params = dates_request[plus_index:no_index] if no_index > plus_index else dates_request[plus_index:]

            dates = []

            if all_params.startswith('all sundays'):
                dates += self._all_weekdays_in_month(DateParser.SUNDAY)
            
            elif all_params.startswith('all thursdays'):
                dates += self._all_weekdays_in_month(DateParser.THURSDAY)
            
            else:
                dates += self.all_dates()
            
            for date_str in no_params.split()[DateParser.NO_PREFIX_INDEX:]:
                date = self._str_to_date(date_str)
                if date in dates:
                    dates.remove(date)
            
            for date_str in plus_params.split()[DateParser.NO_PREFIX_INDEX:]:
                dates.append(self._str_to_date(date_str))

        else:
            dates = [self._str_to_date(date_str) for date_str in dates_request.split()]

        return dates

    def _str_to_date(self, date_str):
        day, month = date_str.split('.')
        return date(self.year, int(month), int(day))

    def all_dates(self):
        return sorted(self._all_weekdays_in_month(DateParser.SUNDAY) + self._all_weekdays_in_month(DateParser.THURSDAY))

    def _all_weekdays_in_month(self, weekday):
        """
        Given a weekday, return all dates of the given weekday 
        For example, if weekday=SUNDAY, return dates of all sundays in month
        """
        first_day = date(self.year, self.month, 1)
        first_weekday = first_day + timedelta(days = weekday - first_day.weekday() if weekday >= first_day.weekday() else weekday - first_day.weekday() + DateParser.WEEK)

        dates = []
        d = first_weekday
        while d.month == self.month:
            dates.append(d)
            d += timedelta(days = DateParser.WEEK)

        return dates