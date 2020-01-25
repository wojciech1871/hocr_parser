from lxml import html, etree
from io import StringIO

from WordMonthExtractor import WordMonthExtractor
from HalfYearExtractor import HalfYearExtractor
from FromToExtractor import FromToExtractor
from ReleaseDateExtractor import get_release_date
from CompanyAddressExtractor import get_company_address_info

class HocrParser:

    def __init__(self):
        self.doc = None
        self.root = None
        self.parsed_document = None


    def read_file(self, path):
        with open(path, 'r', encoding='utf-8', errors='ignore') as file:
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
        pages = [page for page in next(x for x in self.root if x.tag == 'body') if page.attrib.get('class', "") == 'ocr_page']
        for page in pages:
            page_l = []
            lines = [line for line in page if line.attrib.get('class', "") == 'ocrx_line']
            for _, line in enumerate(lines):
                words = [word.text for word in line if
                         word.attrib.get('class', "") == 'ocrx_word' and type(word.text) == str]
                if words:
                    line_joined = " ".join(words)
                page_l.append(line_joined)
            document.append(page_l)
        self.parsed_document = document
        return document

    def get_release_date(self):
        return get_release_date(self.parsed_document)

    def get_dates(self):
        text = " ".join(self.parsed_document[0][0:15])
        text = text.lower()
        
        extractors = [
            HalfYearExtractor(), 
            WordMonthExtractor(), 
            FromToExtractor()
            ]

        for extractor in extractors:
            dates = extractor.extract(text)
            if dates is not None:
                return dates[0].isoformat(), dates[1].isoformat()
        
        return None
    
    def get_company_address_info(self):
        return get_company_address_info(self.parsed_document)

####### Example usage: #######
# parser = HocrParser()
# parser.read_file("./data/contest/train/reports/208910/ZMR_PSr_2012_SPRAWOZDANIE_ZARZADU.hocr")
# parser.read_file("./data/contest/train/reports/15988/rozszerzone_skonsolidowane_sprawozdanie__finansowe_Grupy_Kapitalowej_ProchemSA_na_30.06.2005.hocr")
# document = parser.parse_()
# release_date = parser.get_release_date()
# dates = parser.get_dates()