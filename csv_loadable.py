import csv

ENCODING = 'utf-8-sig'

class CSVLoadable:
    def add(self):
        raise NotImplementedError()

    def load(self):
        with open(self._csv_path, 'r', encoding=ENCODING) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            for row in csv_reader:
                self.add(*row)

    def _load_csv(self):
        self._csv_data = []

        with open(self._csv_path, 'r', encoding=ENCODING) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            for row in csv_reader:
                self._csv_data.append(tuple(row))
