# auth.py
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# "cookie" gibi davranacak basit bir mekanizma (session_state + file fallback)
COOKIE_FILE = "auth_token.txt"

def login():
    st.title("🔐 Giriş Yapın")

    username_input = st.text_input("Kullanıcı Adı")
    password_input = st.text_input("Şifre", type="password")

    login_button = st.button("Giriş Yap")

    if login_button:
        admin_username = os.getenv("ADMIN_USERNAME")
        admin_password = os.getenv("ADMIN_PASSWORD")

        if username_input == admin_username and password_input == admin_password:
            st.session_state["authenticated"] = True
            with open(COOKIE_FILE, "w") as f:
                f.write("authenticated")
            st.success("✅ Giriş başarılı, yönlendiriliyorsunuz...")
            st.rerun()
        else:
            st.error("❌ Hatalı kullanıcı adı veya şifre")
            st.stop()

    else:
        st.stop()            

def is_authenticated():
    # 1. Oturum açık mı?
    if st.session_state.get("authenticated", False):
        return True
    # 2. Dosyadan kontrol et
    if os.path.exists(COOKIE_FILE):
        with open(COOKIE_FILE, "r") as f:
            token = f.read()
            if token == "authenticated":
                st.session_state["authenticated"] = True
                return True
    return False

def logout():
    st.session_state["authenticated"] = False
    if os.path.exists(COOKIE_FILE):
        os.remove(COOKIE_FILE)
    st.success("🚪 Çıkış yaptınız.")
    st.rerun()
