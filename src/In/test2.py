# import pandas as pd
# import tabula

# path = "C:/Users/HusniyeTasna/Desktop/get-content-pdf-python/src/In/SatinAlmaSiparisi_911757.pdf"

# # İlk olarak guess=True ile deneme
# df_guess_true = tabula.read_pdf(path, pages='1', multiple_tables=True, guess=True)

# # Eğer tablo bulunursa, bu DataFrame'i kullan
# if len(df_guess_true) > 0 and not df_guess_true[0].empty:
#     extracted_df = df_guess_true
# else:  # Eğer tablo bulunamazsa, guess=False ile tüm sayfayı al

#     df_list = tabula.read_pdf(path, pages='1', multiple_tables=True, guess=False)

#     extracted_data = []

#     for df in df_list:
#         try:
#             # 'Ürün Adı' kelimesini içeren satırın indeksini bul
#             start_index = df[df.applymap(lambda x: 'Ürün Adı' in str(x)).any(axis=1)].index[0]
            
#             # İlgili satırları al (Ürün Adı başlığı ve ardından gelen sipariş bilgisi)
#             extracted_df = df.loc[start_index:start_index+1]
            
#             extracted_data.append(extracted_df)
#         except (IndexError, KeyError):
#             continue

#     # Elde edilen tüm sipariş bilgilerini tek bir DataFrame'de birleştir
#     final_df = pd.concat(extracted_data, axis=0)

#     print(final_df)


# print(extracted_df)



# import pandas as pd
# import tabula

# path = "C:/Users/HusniyeTasna/Desktop/get-content-pdf-python/src/In/SatinAlmaSiparisi_911849.pdf"

# # İlk olarak guess=True ile deneme
# df_guess_true = tabula.read_pdf(path, pages='1', multiple_tables=True, guess=True)

# # Eğer tablo bulunursa, bu DataFrame'i kullan
# if len(df_guess_true) > 0 and not df_guess_true[0].empty:
#     extracted_df = df_guess_true
# else:  # Eğer tablo bulunamazsa, guess=False ile tüm sayfayı al
#     extracted_df = tabula.read_pdf(path, pages='1', multiple_tables=True, guess=False, area=[160, 0, 215, 595])

# print(extracted_df)





# son satırdaki değeri alıyor
# import tabula

# path = "C:/Users/HusniyeTasna/Desktop/get-content-pdf-python/src/In/SatinAlmaSiparisi_911747.pdf"

# # PDF'ten veriyi DataFrame olarak alma
# dfs = tabula.read_pdf(path, output_format='dataframe', pages=1)

# # İlk DataFrame'i al
# df = dfs[0]

# # DataFrame'den son satırın verisini al
# last_row = df.iloc[-1]

# # Burada last_row'dan gerekli bilgiyi alarak istediğiniz işlemleri gerçekleştirebilirsiniz
# print(last_row)





# pdf den okunan değerin konumunu veriyor
# import tabula

# path = "C:/Users/HusniyeTasna/Desktop/get-content-pdf-python/src/In/SatinAlmaSiparisi_911747.pdf"
# json_output = tabula.read_pdf(path, output_format='json', pages=1)

# # Aradığınız kelimeyi belirleme
# search_word = "HİNDİ FÜME"

# # Kelimenin konumunu bulma
# for page in json_output:
#     for word in page['data']:
#         for letter in word:
#             if letter['text'] == search_word:
#                 print(f"Top-left corner coordinates: {letter['top']}, {letter['left']}")



# her değeri frame içerisindeki sıra ile yazdırma
# import tabula

# path = "C:/Users/HusniyeTasna/Desktop/get-content-pdf-python/src/In/SatinAlmaSiparisi_911747.pdf"

# # PDF'ten veriyi DataFrame olarak alma
# dfs = tabula.read_pdf(path, output_format='dataframe', pages=1)

# # İlk DataFrame'i al
# df = dfs[0]

# # DataFrame'in her bir satırını sırayla yazdırma
# for index, row in df.iterrows():
#     print(f"Satır {index}:\n{row}\n")



# data frame deki ürünleri sırası ile alıp listeye kaydediyor
# import tabula
# import pandas as pd

# path = "C:/Users/HusniyeTasna/Desktop/get-content-pdf-python/src/In/SatinAlmaSiparisi_911747.pdf"

# # PDF'ten veriyi DataFrame olarak alma
# dfs = tabula.read_pdf(path, output_format='dataframe', pages=1)

# # İlk DataFrame'i al
# df = dfs[0]

# # Ürünlerin saklanacağı liste
# products = []

# # DataFrame'in her bir satırını sırayla işleme alma
# for _, row in df.iterrows():
#     # Nan değerleri atma
#     product = {key: value for key, value in row.items() if not pd.isna(value)}
#     products.append(product)

# # Ürünleri yazdırma
# for product in products:
#     print(product)




import tabula
import pandas as pd

path = "C:/Users/HusniyeTasna/Desktop/get-content-pdf-python/src/In/SatinAlmaSiparisi_911747.pdf"

# PDF'ten veriyi DataFrame olarak alma
dfs = tabula.read_pdf(path, output_format='dataframe', pages=1)

# Eğer tablo bulunursa, bu DataFrame'i kullan
if len(dfs) > 0 and not dfs[0].empty:
    dfs = dfs
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

merged_list = merge_products(products)

# Birleştirilmiş ürünleri yazdırma
# for product in merged_list:
#     print(product)

last_products = merged_list[-1]
print(last_products)


# products'ın son ürünü
last_product_text = """
SOSIS
FRANKFURTER
H414578
2
KOLI =
2,04
KG
632,00000
TL
%0
%0
1.264,00 TL
869052724
SOSİS KOLİ
90 Gün Vade
%1
"""

# Sütun başlıklarının sırasını belirtmek için bir liste oluştur
column_order = ['Ürün Adı', 'Ürün Kodu', 'Unnamed: 3', 'Birim', 'Br.Fiyat', 'İnd.', 'İnd.2', 'Tutar', 'Notlar', 'Ödeme', 'KDV']

lines = last_product_text.strip().split("\n")

# Sütunları sırasıyla işlemek için bir döngü başlat
for idx, column in enumerate(column_order):
    current_value = str(last_products[column])
    
    try:
        # Şuanki değeri bul
        start_index = next(i for i, line in enumerate(lines) if line.startswith(current_value))
        
        # Eğer son sütun değilse, bir sonraki sütunun başlangıcını bul
        if idx+1 < len(column_order):
            next_column = column_order[idx+1]
            next_value = str(last_products[next_column])
            end_index = next(i for i, line in enumerate(lines) if line.startswith(next_value))
        else:
            end_index = len(lines)
        
        # Eğer başlangıç ve bitiş aynı değilse, bu sütunlardaki bilgileri birleştir
        if start_index != end_index-1:
            merged_value = ' '.join(lines[start_index:end_index])
            last_products[column] = merged_value
    except StopIteration:
        # Değer listede bulunamazsa bu sütunu atlayabiliriz
        pass

print(last_products)
