import numpy as np
import re
from collections import Counter
from datetime import datetime
from lxml import html, etree
from io import StringIO

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
        string_replaced = string.replace(old, new)
    return string_replaced.replace("\s+","")

def try_parsing_date(text):
    for fmt in ('%d%m%Y', '%d.%m.%Y', '%d/%m/%Y'):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            pass
            
       

class HocrParser:

    def __init__(self):
        self.doc = None
        self.root = None
        self.parsed_document = None

    def read_file(self, path):
#         with open(path) as file:
        with open(path, encoding='UTF-8', errors='ignore') as file:
            lines = file.readlines()
            first_line_i = 0
            for i, line in enumerate(lines):
                if line.find("xml version") > -1:
                    first_line_i = i
                    break
            xml_string = "".join(lines[first_line_i + 1:])
            parser = etree.HTMLParser()
            self.doc = etree.parse(StringIO(xml_string), parser)
            self.root = self.doc.getroot()
            del lines

    def parse_(self):
        document = []
        pages = [page for page in self.root[1] if page.attrib.get('class', "") == 'ocr_page']
        for page in pages:
            page_l = []
            lines = [line for line in page if line.attrib.get('class', "") == 'ocrx_line']
            for i, line in enumerate(lines):
                words = [word.text for word in line if
                         word.attrib.get('class', "") == 'ocrx_word' and type(word.text) == str]
                if words:
                    line_joined = " ".join(words)
                page_l.append(line_joined)
            document.append(page_l)
        self.parsed_document = document
        return document
    
    def get_release_date(self):
        results = []
        pages = len(self.parsed_document)
        for page in range(pages):
            rows = len(self.parsed_document[page])
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
                formated_date = timestamp_date.strftime("%d/%m/%Y")
            else:
                formated_date = None
        else:
            formated_date = None
        return formated_date
        


    ####### Example usage: #######

    # parser = HocrParser()
    # parser.read_file("./Sprawozdanie.hocr")
    # document = parser.parse_()
    # release_date = parser.get_release_date()