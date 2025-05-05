import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import os
import json
from stock_data import stock_info
import groq_res
from streamlit_auth import login, is_authenticated, logout

# Giriş kontrolü
if not is_authenticated():
    login()
    #st.stop() bu sefer sayfa inmiyor login içine yerleştiricez

col1, col2, col3 = st.columns([4, 1, 1])
with col3:
    if st.button("🚪 Çıkış Yap"):
        logout()

# 👇 Giriş başarılıysa buradan sonrası çalışır:
# st.title("📊 Admin Paneline Hoş Geldiniz")
# st.write("Burada uygulamanın asıl içeriği çalışır.")

# --- Sidebar (Sol Panel) ---
st.sidebar.title("📂 Dosya Seçimi")

# Hazır Excel dosyalarının bulunduğu klasör
uploaded_dir = "uploaded_files"
ready_files = [f for f in os.listdir(uploaded_dir) if f.endswith('.xlsx') or f.endswith('.csv')]
ready_files.insert(0, "⛔ Kendi Dosyamı Yükleyeceğim")

# Dosya seçimi
selected_file = st.sidebar.selectbox("Hazır Dosyalar:", ready_files)

uploaded_file = None
file_name = None
balance_sheet_df = None
income_statement_df = None

# --- Fonksiyonlar ---
important_items_balance = [
    "Nakit ve Nakit Benzerleri", "Ticari Alacaklar", "Stoklar", "Toplam Dönen Varlıklar",
    "Toplam Kısa Vadeli Yükümlülükler", "Toplam Uzun Vadeli Yükümlülükler", "Finansal Borçlar",
    "Ticari Borçlar", "Diğer Borçlar", "Maddi Duran Varlıklar", "Yatırım Amaçlı Gayrimenkuller",
    "İştirakler, İş Ortaklıkları ve Bağlı Ortaklıklardaki Yatırımlar", "Dönem Net Kar/Zararı",
    "Geçmiş Yıllar Kar/Zararları", "Toplam Özkaynaklar", "Ana Ortaklığa Ait Özkaynaklar",
    "Ödenmiş Sermaye"
]

important_items_income = [
    "Satış Gelirleri", "Satışların Maliyeti (-)", "Brüt Kar (Zarar)",
    "Pazarlama, Satış ve Dağıtım Giderleri (-)", "Genel Yönetim Giderleri (-)",
    "Araştırma ve Geliştirme Giderleri (-)", "Faaliyet Karı (Zararı)",
    "Yatırım Faaliyetlerinden Gelirler", "Özkaynak Yöntemiyle Değerlenen Yatırımların Karlarından (Zararlarından) Paylar",
    "Dönem Vergi Geliri (Gideri)", "Dönem Karı (Zararı)", "Ana Ortaklık Payları"
]

def data_preprocessing(df):
    df.columns = df.columns.map(lambda x: str(x).strip())
    df.iloc[:, 0] = df.iloc[:, 0].str.strip()
    df = df.set_index(df.columns[0])
    return df.transpose()

def filter_important_data(df, items):
    filter_df = df[items].copy()
    filter_df = filter_df.applymap(lambda x: int(x) if pd.notnull(x) else x)
    filter_df.index = filter_df.index.map(str)
    filter_df = filter_df.loc[filter_df.index >= "2022/3"]
    return filter_df.dropna(axis=1)

def return_json(balance_df, income_df):
    json_balance = balance_df.to_dict(orient='index')
    json_income = income_df.to_dict(orient='index')
    return json_balance, json_income

# --- Dosya Okuma ---
def read_file(file_path, custom_upload=False):
    try:
        if custom_upload:
            file_name = os.path.splitext(file_path.name)[0].split(' ')[0]
        else:
            file_name = os.path.splitext(os.path.basename(file_path))[0].split(' ')[0]

        if (file_path.name if custom_upload else file_path).endswith(".csv"):
            balance_df = pd.read_csv(file_path)
            income_df = None
        else:
            balance_df = pd.read_excel(file_path, sheet_name="Bilanço")
            income_df = pd.read_excel(file_path, sheet_name="Gelir Tablosu (Çeyreklik)")

        return file_name, balance_df, income_df

    except Exception as e:
        st.error(f"❌ Okuma hatası: {e}")
        return None, None, None

# --- Seçim ve Yükleme İşlemleri ---
if selected_file == "⛔ Kendi Dosyamı Yükleyeceğim":
    uploaded_file = st.sidebar.file_uploader("Excel veya CSV dosyası yükleyin", type=['xlsx', 'csv'])
    if uploaded_file:
        file_name, balance_sheet_df, income_statement_df = read_file(uploaded_file, custom_upload=True)
else:
    file_path = os.path.join(uploaded_dir, selected_file)
    file_name, balance_sheet_df, income_statement_df = read_file(file_path)

# --- Veri Gösterme ve İşlem ---
if balance_sheet_df is not None:
    st.success(f"✅ {file_name} dosyası hazır!")
    
    # Ham veri önizleme
    with st.expander("📄 Ham Bilanço Verisi"):
        st.dataframe(balance_sheet_df.iloc[:, :7].dropna(), use_container_width=True)
    if income_statement_df is not None:
        with st.expander("📄 Ham Gelir Tablosu Verisi"):
            st.dataframe(income_statement_df.iloc[:, :7].dropna(), use_container_width=True)
    
    # Veriyi JSON Formatında Göster
    if st.button("📊 Veriyi JSON Formatında Göster"):
        balance_df = filter_important_data(data_preprocessing(balance_sheet_df), important_items_balance)
        income_df = filter_important_data(data_preprocessing(income_statement_df), important_items_income)

        json_balance, json_income = return_json(balance_df, income_df)

        st.subheader("📘 Bilanço (JSON)")
        st.json(json_balance)

        st.subheader("📗 Gelir Tablosu (JSON)")
        st.json(json_income)

    # LLM Analizi
    if st.button("🤖 LLM ile Analiz Et"):
        balance_df = filter_important_data(data_preprocessing(balance_sheet_df), important_items_balance)
        income_df = filter_important_data(data_preprocessing(income_statement_df), important_items_income)

        str_balance = balance_df.to_string()
        str_income = income_df.to_string()

        values, rsi_sig, macd_sig, bol_sig = stock_info(file_name)

        llm_response = groq_res.llm_response(
            balance=str_balance,
            income=str_income,
            stock_info=values,
            rsi_sig=rsi_sig,
            macd_signal=macd_sig,
            bol_signal=bol_sig
        )

        st.subheader("🧠 LLM Yanıtı")
        st.write(llm_response)
else:
    st.info("📥 Lütfen bir dosya yükleyin veya hazır dosyalardan seçin.")

