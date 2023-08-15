import re
from pdfminer.high_level import extract_text
from pdfminer.layout import LTTextBoxHorizontal
from pdfminer.high_level import extract_pages

pdf_path = "C:/Users/HusniyeTasna/Desktop/get-content-pdf-python/src/In/SatinAlmaSiparisi_911747.pdf"
search_term = "Toplam"

def find_text_in_pdf(pdf_path, search_term):
    for page_layout in extract_pages(pdf_path):
        for element in page_layout:
            if isinstance(element, LTTextBoxHorizontal):
                if search_term in element.get_text():
                    # Başlangıç konumu:
                    x, y = element.bbox[0], element.bbox[1]
                    return x, y
    return None

position = find_text_in_pdf(pdf_path, search_term)
if position:
    print(f"'{search_term}' metni şu konumda bulundu: {position}")
else:
    print(f"'{search_term}' metni PDF'te bulunamadı.")
