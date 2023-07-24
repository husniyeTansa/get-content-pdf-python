from pypdf import PdfReader

input_dir = 'C:/Users/HusniyeTasna/Desktop/get-content-pdf-python/midpoint-ybp-orders/tmp'
output_dir = 'C:/Users/HusniyeTasna/Desktop/get-content-pdf-python/tmp-txt'

def extract_text_from_pdf(input_path, output_path):
    pdf_reader = PdfReader(input_path)

    with open(output_path, 'w', encoding='utf-8') as output_file:
        for page_number, page in enumerate(pdf_reader.pages, start=1):
            text = page.extract_text()
            output_file.write(f'Page {page_number}:\n{text}\n\n')

def process_pdf_files():
    import os

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Get all PDF files in the input directory
    pdf_files = [file for file in os.listdir(input_dir) if file.endswith('.pdf')]

    for pdf_file in pdf_files:
        input_path = os.path.join(input_dir, pdf_file)
        output_file = os.path.splitext(pdf_file)[0] + '.txt'
        output_path = os.path.join(output_dir, output_file)

        extract_text_from_pdf(input_path, output_path)
        print('PDF processed: {pdf_file}')

# Process the PDF files
process_pdf_files()


#from pypdf import PdfReader

#pdf_reader = PdfReader('satinalim_siparisi.pdf')

#page_content = {}

#for indx, pdf_page in enumerate(pdf_reader.pages):
#    page_content[indx + 1] = pdf_page.extract_text()
    
#print(page_content)    