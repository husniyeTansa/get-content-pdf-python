import fitz
import getProductsFromPdf
import json
import os
import logging
import datetime
import shutil

# PDF yolunu tanımlama
input_dir = 'C:/Users/HusniyeTasna/Desktop/get-content-pdf-python/midpoint-ybp-orders/tmp'
output_dir = 'C:/Users/HusniyeTasna/Desktop/get-content-pdf-python/tmp-txt'

#-----------------------------------------------------------------------------------------------

# Log dosyasının adını belirleyin
current_month_year = datetime.datetime.now().strftime('%m%Y')
log_filename = f'python-getContent-{current_month_year}.log'

# Log dosyasının kaydedileceği yolu belirleyin
log_path = os.path.join('C:/Users/HusniyeTasna/Desktop/get-content-pdf-python/log/midpoint-ybp-orders/', log_filename)

# Log yapılandırması
logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s - %(message)s')

#-----------------------------------------------------------------------------------------------
# Error a taşıma fonksiyonunu tanımlama
def move_pdf_to_error(input_path):

    output_path = 'C:/Users/HusniyeTasna/Desktop/get-content-pdf-python/midpoint-ybp-orders/err'
    file_name = os.path.basename(input_path)
    output_path = os.path.join(output_path, file_name)
    
    try:
        # shutil.move metodu ile dosyayı taşıma
        shutil.move(input_path, output_path)
        return True, f"File {file_name} moved error!"
    except Exception as e:
        return False, f"Error moving file {file_name}. Reason: {e}"

#-----------------------------------------------------------------------------------------------

os.makedirs(output_dir, exist_ok=True)

# Belirtilen yoldaki tüm PDF dosyalarını al
pdf_files = [os.path.join(input_dir, file) for file in os.listdir(input_dir) if file.endswith('.pdf')]

for path in pdf_files:

    # PDF yolunu tanımlama
    file_name = os.path.basename(path)

    #-----------------------------------------------------------------------------------------------

    logging.info("Process of get content from PDF start!")

    # PDF dosyasını açma
    file = fitz.open(path)

    text = ""
    for page in file:
        text += page.get_text()

    # Öncelikle "Sayfa" kelimesine kadar olan metni ayıklayalım
    start_index = text.find("Satınalma Siparişleri")
    end_index = text.find("Sayfa")
    trimmed_text = text[start_index:end_index].strip()

    # Şimdi her satırı ayrı ayrı dolaşıp belirlediğiniz anahtar kelimeleri arayalım
    lines = trimmed_text.split("\n")
    info = {}
    title = lines[0]  # İlk satırı başlık olarak al
    info["title"] = title

    def get_value_from_next_line(line, lines):
        split_line = line.split(":")
        if len(split_line) > 1:
            return split_line[1].strip()
        else:
            index = lines.index(line)
            if index < len(lines) - 1:
                return lines[index + 1].strip()
        return None

    # Diğer satırları inceleyelim
    for line in lines[1:]:
        if "Sipariş Tarihi" in line:
            text = get_value_from_next_line(line, lines)
            text = text.replace(":", "")
            info["orderDate"] = text
        elif "Teslim Tarihi" in line:
            text = get_value_from_next_line(line, lines)
            text = text.replace(":", "")
            info["deliveryDate"] = text
        elif "Sipariş No" in line:
            text = get_value_from_next_line(line, lines)
            text = text.replace(":", "")
            info["orderNumber"] = text
        elif "Depo Adı" in line:
            text = get_value_from_next_line(line, lines)
            text = text.replace(":", "")
            info["deliveryPoint"] = text

    temp_products = getProductsFromPdf.get_products(path)

    if isinstance(temp_products, list) and len(temp_products) > 0 and temp_products[0] is not None:
        if temp_products[0] == False:
            logging.error("There is an error on pull product from PDF!")
            success, message = move_pdf_to_error(path)
            if success:
                logging.info(message)
            else:
                logging.error(message)
            continue

    info['product'] = temp_products

    logging.info("Get content from PDF is success!")

    #-----------------------------------------------------------------------------------------------

    file_name_txt = file_name.replace("pdf", "txt")
    file_path = os.path.join(output_dir, file_name_txt)

    # Klasörün var olup olmadığını kontrol et, yoksa oluştur
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Dosyaya JSON formatında kaydetme
    with open(file_path, 'w', encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=4)

    logging.info(f"Content saved to {file_path}")


