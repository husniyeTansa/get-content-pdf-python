import fitz
import tabula
import pandas as pd


# Son üründeki eksik bilgiyi merge etme fonksiyonu
def merge_last_products(path, last_product_miss, size):
    # PDF dosyasını açma
    doc = fitz.open(path)

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

    # Get last product from dont missing data
    last_product = products[-1]

    if len(products) == size:
        # Sütun başlıklarının sırasını belirtmek için bir liste oluştur
        column_order = ['Ürün Adı', 'Ürün Kodu', 'Miktar', 'Birim', 'Br.Fiyat', 'İnd.', 'İnd.2', 'Tutar', 'Notlar', 'Ödeme', 'KDV']

        lines = last_product.strip().split("\n")

        # Sütunları sırasıyla işlemek için bir döngü başlat
        for idx, column in enumerate(column_order):
            current_value = str(last_product_miss[column])
            
            try:
                # Şuanki değeri bul
                start_index = next(i for i, line in enumerate(lines) if line.startswith(current_value))
                
                # Eğer son sütun değilse, bir sonraki sütunun başlangıcını bul
                if idx+1 < len(column_order):
                    next_column = column_order[idx+1]
                    next_value = str(last_product_miss[next_column])
                    end_index = next(i for i, line in enumerate(lines) if line.startswith(next_value))
                else:
                    end_index = len(lines)
                
                # Eğer başlangıç ve bitiş aynı değilse, bu sütunlardaki bilgileri birleştir
                if start_index != end_index-1:
                    merged_value = ' '.join(lines[start_index:end_index])
                    last_product_miss[column] = merged_value
            except StopIteration:
                # Değer listede bulunamazsa bu sütunu atlayabiliriz
                pass

        return last_product_miss
    else:
        return [False, "Incompatibility problem for missing last product data!"]

# Tabula ile alınan ürün bilgilerini merge etme fonksiyonu
def merge_products(products):
    merged_products = []
    current_product = {}

    for product in products:
        if len(product) < 7 and current_product:  # Eğer bir ürün sütunu 7'den azsa birleştirme yap
            for key, value in product.items():
                # Eğer birleştirme sırasında mevcut anahtar zaten varsa değeri birleştir
                if key in current_product:
                    current_product[key] += " " + str(value)
                else:
                    current_product[key] = value
        else:
            if current_product:
                merged_products.append(current_product)
            current_product = product

    # Son ürünü eklemeyi unutma
    if current_product:
        merged_products.append(current_product)

    return merged_products

# Ürün bilgilerini PDF üzerinden alma fonksiyonu
def get_products(path):
    # PDF'ten veriyi DataFrame olarak alma
    dfs = tabula.read_pdf(path, output_format='dataframe', pages=1)

    # Son üründe eksik bilgi gelmiş olma ihtimali
    check_product = False

    # Eğer tablo bulunursa, bu DataFrame'i kullan
    if len(dfs) > 0 and not dfs[0].empty:
        dfs = dfs
        check_product = True
    else:  # Eğer tablo bulunamazsa, guess=False ile tüm sayfayı al
        dfs = tabula.read_pdf(path, pages='1', multiple_tables=True, guess=False, area=[160, 0, 215, 595])

    # İlk DataFrame'i al
    df = dfs[0]

    # Ürünlerin saklanacağı liste
    products = []

    # DataFrame'in her bir satırını sırayla işleme alma
    for _, row in df.iterrows():
        # Nan değerleri atma
        product = {key: value for key, value in row.items() if not pd.isna(value)}
        products.append(product)

    # Merge işlemi ile ürün listesini aldık
    merged_list = merge_products(products)

    # Her bir sözlük içinde 'Unnamed: 3' gibi başlayan kolon adını 'Miktar' olarak değiştir
    for product in merged_list:
        keys_to_change = [key for key in product.keys() if key.startswith('Unnamed')]
        for key in keys_to_change:
            product['Miktar'] = product.pop(key)

    # Son üründeki eksik bilgi tamamlanacaktır
    if check_product == True:
        last_product = merged_list[-1]
        last_product_new = merge_last_products(path, last_product, len(merged_list))
        merged_list[-1] = last_product_new


    return merged_list
