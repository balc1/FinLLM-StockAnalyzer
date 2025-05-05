import customtkinter as ctk
from tkinter import filedialog
from app import load_file, veri_isle, llm_isle

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

load_file()

# Dosya yükleme butonu
upload_btn = ctk.CTkButton(app, text="Excel / CSV Yükle", command=load_file)
upload_btn.pack(pady=10)

# Durum etiketi
status_label = ctk.CTkLabel(app, text="", font=("Arial", 14))
status_label.pack(pady=5)

# Metin kutusu (çıktılar burada gösterilecek)
output_textbox = ctk.CTkTextbox(app, width=850, height=450)
output_textbox.pack(pady=10)

process_button = ctk.CTkButton(app, text="Veriyi İşle", command=veri_isle)
process_button.pack(pady=10)

llm_button = ctk.CTkButton(app, text="llm", command=llm_isle)
llm_button.pack(ipadx=10)

app.mainloop()