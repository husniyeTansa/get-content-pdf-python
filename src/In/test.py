# import pdfplumber

# def extract_text_from_pdf(input_path, output_path):
#     with pdfplumber.open(input_path) as pdf:
#         all_text = ""
#         for page_number, page in enumerate(pdf.pages, start=1):
#             text = page.extract_text()
#             all_text += f'Page {page_number}:\n{text}\n\n'

#     with open(output_path, 'w', encoding='utf-8') as output_file:
#         output_file.write(all_text)

# # Kullanım örneği
# input_path = 'SatinAlmaSiparisi_911757.pdf'
# output_path = 'output.txt'
# extract_text_from_pdf(input_path, output_path)



import fitz

# PDF dosyasını açma
doc = fitz.open('C:/Users/HusniyeTasna/Desktop/get-content-pdf-python/src/In/SatinAlmaSiparisi_911747.pdf')

text = ""
for page in doc:
    text += page.get_text()

# Başlangıç ve bitiş noktalarını belirleme
start_key = "Ürün Adı\nÜrün Kodu\nMiktar\nBirim\nBr.Fiyat\nİnd.\nİnd.2\nTutar\nNotlar\nÖdeme\nKDV"
end_key = "Toplam"

start_index = text.find(start_key) + len(start_key)
end_index = text.find(end_key)

# Başlangıç ve bitiş noktaları arasındaki veriyi alma
products_text = text[start_index:end_index].strip()

# Tüm satırları ayırma
lines = products_text.split("\n")

products = [] # Ürünleri bu listeye ekleyeceğiz
current_product = [] # Geçici olarak şu anki ürün bilgisini bu listede tutacağız

percent_count = 0

for line in lines:
    if "%" in line:
        percent_count += 1
        
    current_product.append(line)
    
    # Eğer üç defa "%" işareti gördüysek, bu ürünün tamamlandığını varsayalım
    if percent_count == 3:
        products.append("\n".join(current_product))
        current_product = [] # Geçici ürün listesini sıfırla
        percent_count = 0 # Sayacı sıfırla

# Ürünleri yazdıralım
# for product in products:
#     print(product)
#     print("---------")  # Ürünler arasında ayırıcı olarak koydum

# Son ürünü al
last_product = products[-1]

print(last_product)




