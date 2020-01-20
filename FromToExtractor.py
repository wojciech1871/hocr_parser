import re

from datetime import date


class FromToExtractor:

    def __init__(self):
        self.regex = r'(?P<date>(?P<day>\d{1,2})(?P<separator>[.\/-])(?P<month>\d{1,2})(?P=separator)(?P<year>\d{2,4}))'


    def extract(self, text):
        iterator = re.finditer(self.regex, text)

        try:
            first_match = iterator.__next__()
        except:
            return None
        second_match = iterator.__next__()

        date_from = self.get_dates_from_match(first_match)
        date_to = self.get_dates_from_match(second_match)

        return date_from, date_to


    def get_dates_from_match(self, match):
        year = int(match['year'])
        month = int(match['month'])
        day = int(match['day'])

        date_output = date(year, month, day)
        return date_output