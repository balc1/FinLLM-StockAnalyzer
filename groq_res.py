from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os


load_dotenv()  # .env dosyasını yükler

def llm_response(balance, income, stock_info, rsi_sig, macd_signal, bol_signal):
    prompt2 = f"""
You are a financial analyst AI. Below is a company's last 10 quarterly financial statements (balance sheet and income statement), key market data, and technical analysis indicators (RSI, MACD, Bollinger Bands). Your task is to analyze the data and provide a comprehensive investment report.

🔹 **1. Company Growth Evaluation:**  
Analyze revenue, net income, debt, and equity trends. Is the company showing signs of growth or decline?

🔹 **2. Next Quarter Forecast:**  
Based on the recent trends, estimate the expected figures for the next quarter: revenue, net income, total debt, and equity.

🔹 **3. MarketCap & Stock Price Forecast:**  
Based on financial and technical indicators, forecast the expected market capitalization and stock price for:  
- 1 month  
- 3 months  
- 6 months  
- 1 year  
Clearly state your assumptions and reasoning.

🔹 **4. Valuation Analysis:**  
Estimate the company’s intrinsic value using appropriate methods such as P/E, P/S, or discounted cash flow (DCF), based on the available trends.

🔹 **5. Investment Recommendation:**  
Would you recommend buying this company's stock now? Justify your answer with financial ratios, valuation results, and trend analysis.

🔹 **6. Key Financial Ratios & Interpretation:**  
Calculate and explain:  
- Gross Margin  
- Net Margin  
- Debt-to-Equity Ratio  
- Current Ratio  
- Return on Equity (ROE)  
- Return on Assets (ROA)  

🔹 **7. RSI Signal Focused Analysis (Very Important):**  
Provide a specific and detailed analysis of the RSI (Relative Strength Index) signal:  
- What is the RSI value indicating?  
- Is it in overbought or oversold territory?  
- Has there been a recent divergence with price action?  
- How strong is the RSI signal compared to MACD and Bollinger Bands?  
⚠️ Place **greater weight on RSI** than MACD or Bollinger Bands when making forecasting and investment decisions.

---

### Input Data

📊 **Market Data:**  
{stock_info}

📄 **Balance Sheet Data:**  
{balance}

📈 **Income Statement Data:**  
{income}

📉 **RSI Signal:**
{rsi_sig}

📉 **MACD Signal:**  
{macd_signal}

📉 **Bollinger Bands Signal:**  
{bol_signal}

**Language of output**: Turkish
"""
    prompt = f"""
You are a professional financial analyst AI.

Your job is to analyze a company's last 10 quarterly financial statements (balance sheet and income statement), as well as market and technical indicators (RSI, MACD, Bollinger Bands). Your focus should be **primarily on financial fundamentals**. Use technical signals **only as supporting evidence**.

### Tasks

1. **Company Health Summary (max 3 sentences):**  
Is the company fundamentally strong or weak? Focus on revenue growth, net income, total debt, and equity trends.

2. **Next Quarter Forecast:**  
Estimate next quarter’s revenue, net income, and total debt based on trends.

3. **Valuation (only one method):**  
Use one appropriate method (P/E, P/S, or DCF) to estimate intrinsic value. Be concise and logical.

4. **1-Month Price & Market Cap Forecast (Optional):**  
Give a 1-month price prediction only **if the company is fundamentally strong**. Use RSI/MACD/Bollinger only to fine-tune the estimate.

5. **Investment Recommendation (Buy / Hold / Sell):**  
Make a clear recommendation based on financials. RSI can support short-term timing but cannot override fundamentals.

6. **Key Ratios (List only):**  
- Gross Margin  
- Net Margin  
- ROE  
- Debt/Equity  
- Current Ratio

7. **RSI Analysis (Secondary Importance):**  
Analyze the RSI trend over the last 10 entries. State whether it supports a short-term move. Use this **only to time** the entry or exit, not to override fundamentals.

8. **Currency Type:** Turkish Lira (TL)
---

📊 **Market Data:**  
{stock_info}

📄 **Balance Sheet:**  
{balance}

📈 **Income Statement:**  
{income}

📉 **RSI Trend:**  
{rsi_sig}

📉 **MACD:**  
{macd_signal}

📉 **Bollinger Bands:**  
{bol_signal}

**Output Language**: Turkish
"""


    llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile",
    temperature= 0.3,
    top_p = 0.9,
    max_tokens = 10000
    )

    messages = [
        ("system",prompt),
        ("human", "Please share your opinion about the stock"),
    ]
    ai_msg = llm.invoke(messages)

    return ai_msg.content

if __name__ == "__main__":
    pass