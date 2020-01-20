import numpy as np
import re
os.chdir('C:\\Users\\tomas\\Downloads\\NLP\\PADT-1\\proj-2-poleval\\')
from collections import Counter
from datetime import datetime

def polish_month_name_to_nr(string):
    month_names = {
            'styczeń':'01',
            'stycznia':'01',
            'luty':'02',
            'lutego':'02',
            'marzec':'03',
            'marca':'03',
            'kwiecień':'04',
            'kwietnia':'04',
            'maj':'05',
            'maja':'05',
            'czerwiec':'06',
            'czerwca':'06',
            'lipiec':'07',
            'lipca':'07',
            'sierpień':'08',
            'sierpnia':'08',
            'wrzesień':'09',
            'września':'09',
            'październik':'10',
            'października':'10',
            'listopad':'11',
            'listopada':'11',
            'grudzień':'12',
            'grudnia':'12'
        }
    for old, new in month_names.items():
        string = string.replace(old, new)
    return re.sub('\s+','',string)

def try_parsing_date(text):
    text = text.lower()
    text = re.sub('[^0-9].*','', text)
    for fmt in ('%d%m%Y', '%d.%m.%Y', '%d/%m/%Y'):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            pass

def get_release_date(document):
        results = []
        pages = len(document)
        for page in range(pages):
            rows = len(document[page])
            for row in range(rows):
                date_search = re.search('[A-Z].*(,{1}|,{1}\s+dnia)\s+([0-3][0-9].*(styczeń|stycznia|luty|lutego|marzec|marca|kwiecień|kwietnia|maj|maja|czerwiec|czerwca|lipiec|lipca|sierpień|sierpnia|wrzesień|września|październik|października|listopad|listopada|grudzień|grudnia|[0-9]).*[12][0][0-1][0-9])',self.parsed_document[page][row], re.IGNORECASE)
                if date_search:
                    results.append(date_search.group(2))

        keys=Counter(results).keys() # equals to list(set(words))
        counts=Counter(results).values() # counts the elements' frequency
        if len(keys) != 0:
            date = list(keys)[np.argmax(counts)]
            numeric_date = polish_month_name_to_nr(date)
            timestamp_date = try_parsing_date(numeric_date)
            if timestamp_date is not None:
                formated_date = timestamp_date.strftime("%d-%m-%Y")
            else:
                formated_date = None
        else:
            formated_date = None
        return formated_date