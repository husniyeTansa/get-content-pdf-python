import pdfplumber
import pandas as pd

pdf_path = "C:/Users/HusniyeTasna/Desktop/get-content-pdf-python/src/In/SatinAlmaSiparisi_911757.pdf"

with pdfplumber.open(pdf_path) as pdf:
    page = pdf.pages[0]
    
    # Calculate the coordinates for the cropped area (based on average A4 page size)
    left = 30  # Left edge
    top = 150    # Top edge
    right = 550 # Right edge
    bottom = 200 # Bottom edge
    
    # Crop the page
    cropped_page = page.crop((left, top, right, bottom))
    
    text = cropped_page.extract_text()
    
    lines = text.split('\n')
    
    # Process the extracted lines into a DataFrame if needed
    data = [line.split() for line in lines if line.strip()]
    df = pd.DataFrame(data)
    
    print(df)
