import re

from datetime import date


class WordMonthExtractor:

    def __init__(self):
        self.regex = r'(?:za [\w\s]*?(?P<months_period>[\węóąśłżźćńĘÓĄŚŁŻŹĆŃ]+) miesi[ęĘ]cy zako[ńŃ]czony(?:ch)? (?:dnia\s)?)?(?P<date>(?P<day>\d{1,2})\s(?P<month>\w+)\s(?P<year>\d{4}))'
        self.months = {
            'styczeń':1,
            'stycznia':1,
            'luty':2,
            'lutego':2,
            'marzec':3,
            'marca':3,
            'kwiecień':4,
            'kwietnia':4,
            'maj':5,
            'maja':5,
            'czerwiec':6,
            'czerwca':6,
            'lipiec':7,
            'lipca':7,
            'sierpień':8,
            'sierpnia':8,
            'wrzesień':9,
            'września':9,
            'październik':10,
            'października':10,
            'listopad':11,
            'listopada':11,
            'grudzień':12,
            'grudnia':12
        }


    def extract(self, text):
        iterator = re.finditer(self.regex, text)

        try:
            first_match = iterator.__next__()
        except:
            return None

        if first_match['months_period'] is None:
            try:
                second_match = iterator.__next__()
            except:
                return None

            date_from = self.match_to_date(first_match)
            date_to = self.match_to_date(second_match)
            return date_from, date_to
        
        return self.get_dates_from_period_match(first_match)


    def match_to_date(self, match):
        year = int(match['year'])
        month = match['month']
        day = int(match['day'])

        month = self.months[month.lower()]

        date_output = date(year, month, day)
        return date_output


    def get_dates_from_period_match(self, match):
        months_period = match['months_period']
        
        if months_period.isdigit():
            months_period = int(months_period)
        elif months_period.lower() == 'sześciu':
            months_period = 6

        date_to = self.match_to_date(match)
        date_from = date_to.replace(day=1).replace(month=date_to.month + 1 - months_period)

        return date_from, date_to
        