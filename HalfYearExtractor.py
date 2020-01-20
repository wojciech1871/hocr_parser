import re

from datetime import date


class HalfYearExtractor:

    def __init__(self):
        self.regex = r'(?P<half_year_number>(?:I{1,2})|(?:pierwsze|drugie)|(?:i|ii)|(?:1|2))\s+p[óÓ][łŁ]rocz[eu]\s+(?P<year>\d{4})'


    def extract(self, text):
        m = re.search(self.regex, text)
        if m is None:
            return None
        
        first_half_year = True
        half_year_number = m['half_year_number']
        if half_year_number == 'II' or half_year_number == 'drugie':
            first_half_year = False

        year = int(m['year'])

        if first_half_year:
            from_month = 1
            to_month = 6
            to_day = 30
        else:
            from_month = 7
            to_month = 12
            to_day = 31

        date_from = date(year, from_month, 1)
        date_to = date(year, to_month, to_day)

        return date_from, date_to