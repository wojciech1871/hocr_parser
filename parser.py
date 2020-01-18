from lxml import html, etree
from io import StringIO


class HocrParser:

    def __init__(self):
        self.doc = None
        self.root = None

    def read_file(self, path):
        with open(path, encoding='utf8') as file:
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
        return document


    ####### Example usage: #######

    # parser = HocrParser()
    # parser.read_file("./Sprawozdanie.hocr")
    # document = parser.parse_()
