import pandas as pd
import os

def read_file(file, filename=None):
    """
    Excel veya CSV dosyasını okur, dosya adı ve DataFrame'leri döner.
    file: Dosya yolu (str) veya dosya objesi (BytesIO)
    filename: Yüklenen dosyanın adı (opsiyonel, frontend'den geliyorsa gerekir)
    """
    # Dosya adını ayıkla
    if filename:
        base_name = os.path.splitext(filename)[0].split(' ')[0]
    else:
        base_name = os.path.splitext(os.path.basename(file))[0].split(' ')[0]

    # Dosya uzantısı kontrolü
    ext = filename.split('.')[-1] if filename else file.split('.')[-1]
    try:
        if ext == "csv":
            balance_df = pd.read_csv(file)
            income_df = None
        else:
            balance_df = pd.read_excel(file, sheet_name="Bilanço")
            income_df = pd.read_excel(file, sheet_name="Gelir Tablosu (Çeyreklik)")
        return base_name, balance_df, income_df
    except Exception as e:
        raise RuntimeError(f"Dosya okuma hatası: {e}")

def data_preprocessing(df):
    """Sütunları ve index'i temizler, transpoze eder."""
    df.columns = df.columns.map(lambda x: str(x).strip())
    df.iloc[:, 0] = df.iloc[:, 0].str.strip()
    df = df.set_index(df.columns[0])
    return df.transpose()

def filter_important_data(df, items):
    """Belirli kalemleri seçip, son dönemleri ve dolu sütunları döner."""
    filter_df = df[items].copy()
    filter_df = filter_df.applymap(lambda x: int(x) if pd.notnull(x) else x)
    filter_df.index = filter_df.index.map(str)
    filter_df = filter_df.loc[filter_df.index >= "2022/3"]
    return filter_df.dropna(axis=1)