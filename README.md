# 📊 FinLLM – LLM-Powered Financial Report Analyzer

## 🔍 About the Project

**FinLLM** is an AI-powered financial analysis application that evaluates companies based on their balance sheets and income statements. You can either select from preloaded financial reports or upload your own balance sheet file for analysis.

The model combines past financial report data with current market indicators fetched via the `yfinance` API (e.g., latest stock price, RSI, MACD, market cap, etc.) to perform a deep analysis using a powerful Language Model (LLM).

## 🖥️ Usage Modes

The application supports two user interfaces:

### 1. 🖱️ Streamlit Web Interface

A clean, browser-based interface for easy interaction.

**To run:**

```bash
streamlit run main.py
2. 🧾 Tkinter Desktop Interface
A minimal desktop GUI for local use.

To run:

bash
Kopyala
Düzenle
python tk_interface.py
📁 File Upload
You can:

Choose from sample financial report files provided with the app.

Or upload your own file in Excel or CSV format.

📌 Notes:
Expected format:

Excel file: Should include two sheets named "Bilanço" (Balance Sheet) and "Gelir Tablosu (Quarterly Income Statement)".

CSV file: Should contain only balance sheet data.

🧠 Analysis Process
Once a file is uploaded:

Required columns are filtered and cleaned.

Data is limited to the latest financial quarters.

Based on the company in the file, yfinance fetches current market data:

Latest price

RSI, MACD, Bollinger Bands, etc.

Market Cap, Beta, and more

All information is combined and processed by an LLM for smart analysis.

A detailed output is presented to the user.

🔒 Authentication
The Streamlit interface includes a login system. Unauthorized users cannot access the main interface.

🛠️ Requirements
bash
Kopyala
Düzenle
pip install -r requirements.txt
Main dependencies:

streamlit

pandas

yfinance

tkinter

streamlit-authenticator

openai or groq (for LLM interaction)

📦 Deployment
The Streamlit version can be deployed on Streamlit Community Cloud, Render, or similar platforms.

📬 Contact
Developer: [Your Name]
Email: [yourname@example.com]

This application is for educational and analysis purposes only. It does not constitute investment advice.
