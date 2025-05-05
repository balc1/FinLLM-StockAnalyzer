import customtkinter as ctk
from tkinter import filedialog
import pandas as pd
import json
import groq_res
from stock_data import stock_info
import os

# Tema
ctk.set_appearance_mode("System")  # "Dark", "Light", "System"
ctk.set_default_color_theme("blue")  # Tema rengi

# Ana pencere
app = ctk.CTk()
app.title("Finansal Rapor Analiz Aracı")
app.geometry("900x710")

# Başlık etiketi
title_label = ctk.CTkLabel(app, text="Finansal Rapor Analizi", font=("Arial", 24, "bold"))
title_label.pack(pady=20)

# Yüklenen dosyayı saklayacağımız değişken
data = None
balance_sheet_df = None
income_statement_df = None
file_name = None

def load_file():
    global data
    global balance_sheet_df
    global income_statement_df
    global file_name

    # Dosya seçme penceresi açılır
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")])

    if file_path:
        # Dosya adını ayıkla (örn. "THYAO (TRY).xlsx" → "THYAO")
        file_name = os.path.basename(file_path)         # "THYAO (TRY).xlsx"
        file_name = os.path.splitext(file_name)[0]      # "THYAO (TRY)"
        file_name = file_name.split(' ')[0]             # "THYAO"

        try:
            if file_path.endswith('.csv'):
                # Eğer CSV dosyasıysa:
                balance_sheet_df = pd.read_csv(file_path)  # CSV'de sheet yoktur
                income_statement_df = None  # CSV için ikinci sheet olmayabilir
            else:
                # Eğer Excel dosyasıysa, iki farklı sheet yüklenir
                balance_sheet_df = pd.read_excel(file_path, sheet_name="Bilanço", skiprows=0)
                income_statement_df = pd.read_excel(file_path, sheet_name="Gelir Tablosu (Çeyreklik)", skiprows=0)

            status_label.configure(text="✅ Dosya yüklendi!", text_color="green")

        except Exception as e:
            status_label.configure(text=f"❌ Hata oluştu: {e}", text_color="red")

    else:
        status_label.configure(text="❌ Dosya seçilmedi!", text_color="red")
   


# Kullanacağımız kalemler
important_items_balance = [
    "Nakit ve Nakit Benzerleri",
    "Ticari Alacaklar",
    "Stoklar",
    "Toplam Dönen Varlıklar",
    "Toplam Kısa Vadeli Yükümlülükler",
    "Toplam Uzun Vadeli Yükümlülükler",
    "Finansal Borçlar",
    "Ticari Borçlar",
    "Diğer Borçlar",
    "Maddi Duran Varlıklar",
    "Yatırım Amaçlı Gayrimenkuller",
    "İştirakler, İş Ortaklıkları ve Bağlı Ortaklıklardaki Yatırımlar",
    "Dönem Net Kar/Zararı",
    "Geçmiş Yıllar Kar/Zararları",
    "Toplam Özkaynaklar",
    "Ana Ortaklığa Ait Özkaynaklar",
    "Ödenmiş Sermaye"
]
important_items_income=[
    "Satış Gelirleri",
    "Satışların Maliyeti (-)",
    "Brüt Kar (Zarar)",
    "Pazarlama, Satış ve Dağıtım Giderleri (-)",
    "Genel Yönetim Giderleri (-)",
    "Araştırma ve Geliştirme Giderleri (-)",
    "Faaliyet Karı (Zararı)",
    "Yatırım Faaliyetlerinden Gelirler",
    "Özkaynak Yöntemiyle Değerlenen Yatırımların Karlarından (Zararlarından) Paylar",
    "Dönem Vergi Geliri (Gideri)",
    "Dönem Karı (Zararı)",
    "Ana Ortaklık Payları"

]

def filter_important_data(df, items):
    """Önemli kalemleri seçip döndürür."""
    filter_df = df[items].copy()

    filter_df = filter_df.applymap(lambda x: int(x) if pd.notnull(x) else x)

    filter_df.index = filter_df.index.map(str)

    filter_df = filter_df.loc[filter_df.index >= "2022/3"]

    filter_df = filter_df.dropna(axis=1)

    return filter_df 

def data_preprocessing(df):
    df.columns = df.columns.map(lambda x: str(x).strip())

    df.iloc[:,0] = df.iloc[:,0].str.strip()

    df = df.set_index(df.columns[0])

    df = df.transpose()

    return df

# Dosya yükleme butonu
upload_btn = ctk.CTkButton(app, text="Excel / CSV Yükle", command=load_file)
upload_btn.pack(pady=10)

# Durum etiketi
status_label = ctk.CTkLabel(app, text="", font=("Arial", 14))
status_label.pack(pady=5)

# Metin kutusu (çıktılar burada gösterilecek)
output_textbox = ctk.CTkTextbox(app, width=850, height=450)
output_textbox.pack(pady=10)



def return_str():
    balance_df = filter_important_data(data_preprocessing(balance_sheet_df),important_items_balance)
    income_df = filter_important_data(data_preprocessing(income_statement_df),important_items_income)
    str_balance = balance_df.to_string(index=True)
    str_income = income_df.to_string(index=True)
    return str_balance, str_income 

def return_json():
    balance_df = filter_important_data(data_preprocessing(balance_sheet_df),important_items_balance)
    income_df = filter_important_data(data_preprocessing(income_statement_df),important_items_income)

    json_balance = balance_df.to_dict(orient='index')
    json_income = income_df.to_dict(orient='index')

    return json_balance, json_income

def veri_isle():
    #if data:
        #sonuc = filter_important_data(data_preprocessing(income_statement_df),important_items_income)
        sonuc , gelir = return_json()
        #sonuc = veri_isle()
        output_textbox.delete("1.0", "end")
        #with pd.option_context('display.max_rows', None, 'display.max_columns', 5):
        #output_textbox.insert("end", sonuc.to_string(index=False))
        formatted_json = json.dumps(sonuc, indent=4, ensure_ascii=False) 
        gelir_json = json.dumps(gelir, indent=4, ensure_ascii=False) # JSON'u formatlı hale getir
        output_textbox.insert("end", "-----------------------------Bilanço Tablosu-----------------------------")
        output_textbox.insert("end", formatted_json) # Text alanına yazdır
        output_textbox.insert("end", "-----------------------------Gelir Tablosu-------------------------------")
        output_textbox.insert("end", gelir_json)
    #else:
        #output_textbox.insert("end", "Lütfen önce bir dosya yükleyin.")

       

process_button = ctk.CTkButton(app, text="Veriyi İşle", command=veri_isle)
process_button.pack(pady=10)

def llm_isle():
    balance , income = return_str()
    values, rsi_sig, macd_sig, bol_sig = stock_info(file_name)
    json.dumps(values)
    llm = groq_res.llm_response(balance=balance, income=income, stock_info=values, rsi_sig=rsi_sig, macd_signal=macd_sig, bol_signal=bol_sig)
    #print(file_name)
    #print(stock_info(file_name))
    output_textbox.delete("1.0", "end")
    output_textbox.insert("end", llm)


llm_button = ctk.CTkButton(app, text="llm", command=llm_isle)
llm_button.pack(ipadx=10)

app.mainloop()