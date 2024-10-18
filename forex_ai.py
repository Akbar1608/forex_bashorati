import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Streamlit ilovasi sarlavhasi
st.title("Forex va Metall Tahlili - Jonli Tahlil")

# Tanlash mumkin bo'lgan tickerlar
tickers = {
    'Oltin (XAUUSD)': 'GC=F',
    'Kumush (XAGUSD)': 'SI=F',
    'EUR/USD': 'EURUSD=X',
    'GBP/USD': 'GBPUSD=X',
    'USD/JPY': 'USDJPY=X',
    'AUD/USD': 'AUDUSD=X',
    'USD/CAD': 'USDCAD=X',
    'NZD/USD': 'NZDUSD=X'
}

# Sidebar - tickerlarni tanlash
st.sidebar.header("Mavjud Tickerlar")
selected_ticker = st.sidebar.selectbox("Tanlang:", list(tickers.keys()))

# Tanlangan tickerni oling
ticker_input = tickers[selected_ticker]

# Tanlash mumkin bo'lgan vaqt oralig'i
timeframes = ["1m", "5m", "1h", "1d"]
selected_timeframe = st.selectbox("Vaqt oralig'ini tanlang:", timeframes)

# Jonli tahlil tugmasi
if st.button("Jonli Tahlil qilish"):
    # API orqali real vaqt bozor ma'lumotlarini olish
    ticker = yf.Ticker(ticker_input)

    # So'nggi bir kun ichidagi ma'lumotlarni olish va belgilangan vaqt oralig'iga moslashtirish
    hist = ticker.history(period="1d", interval=selected_timeframe)

    # Agar ma'lumotlar bo'sh bo'lmasa, tahlil qilish
    if not hist.empty:
        st.write(f"Ma'lumotlar uchun: {selected_ticker}")
        st.write("So'nggi bir kun ichidagi narxlar:")

        # Candlestick grafikini yaratish
        fig = go.Figure(data=[go.Candlestick(x=hist.index,
                                               open=hist['Open'],
                                               high=hist['High'],
                                               low=hist['Low'],
                                               close=hist['Close'])])

        # Qo'llab-quvvatlash va qarshilik darajalari
        support = hist['Close'].min()  # Qo'llab-quvvatlash darajasi
        resistance = hist['Close'].max()  # Qarshilik darajasi

        # Grafikda qo'llab-quvvatlash va qarshilik darajalarini qo'shish
        fig.add_trace(go.Scatter(x=[hist.index[0], hist.index[-1]], y=[support, support],
                                 mode='lines', name='Qo\'llab-quvvatlash', line=dict(color='green', width=2, dash='dash')))
        fig.add_trace(go.Scatter(x=[hist.index[0], hist.index[-1]], y=[resistance, resistance],
                                 mode='lines', name='Qarshilik', line=dict(color='red', width=2, dash='dash')))

        fig.update_layout(title=f"{ticker_input} uchun Candlestick Grafiki",
                          xaxis_title="Vaqt",
                          yaxis_title="Narx",
                          xaxis_rangeslider_visible=False)

        st.plotly_chart(fig, use_container_width=True)

        # Tahlil qilish
        latest_price = hist['Close'].iloc[-1]
        st.write(f"Eng so'nggi narx: {latest_price:.4f}")

        # O'zgarish foizi
        price_change = ((latest_price - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100

        # Tahlil natijalari
        st.write(f"Qo'llab-quvvatlash darajasi: {support:.4f}")
        st.write(f"Qarshilik darajasi: {resistance:.4f}")
        st.write(f"Narx o'zgarishi: {price_change:.2f}%")

        # Tahlil strategiyalari va grafiklar
        strategies = []

        # ICT tahlili
        if latest_price > resistance:
            prediction_ict = f"ICT: Narx oshishi kutilmoqda (Bullish). Qo'llab-quvvatlash darajasi {support:.4f}, qarshilik darajasi {resistance:.4f}."
        elif latest_price < support:
            prediction_ict = f"ICT: Narx tushishi kutilmoqda (Bearish). Qo'llab-quvvatlash darajasi {support:.4f}, qarshilik darajasi {resistance:.4f}."
        else:
            prediction_ict = f"ICT: Narx o'zgarishi kutilmoqda (Volatility). Qo'llab-quvvatlash darajasi {support:.4f}, qarshilik darajasi {resistance:.4f}."
        strategies.append(prediction_ict)

        # SNR tahlili
        if latest_price < support:
            prediction_snr = f"SNR: Narx pasayishi kutilmoqda (Bearish). Qo'llab-quvvatlash darajasi {support:.4f}, qarshilik darajasi {resistance:.4f}."
        else:
            prediction_snr = f"SNR: Narx oshishi kutilmoqda (Bullish). Qo'llab-quvvatlash darajasi {support:.4f}, qarshilik darajasi {resistance:.4f}."
        strategies.append(prediction_snr)

        # SMC tahlili
        if latest_price < (support + resistance) / 2:
            prediction_smc = f"SMC: Narx o'zgarishi kutilmoqda (Volatility). Qo'llab-quvvatlash darajasi {support:.4f}, qarshilik darajasi {resistance:.4f}."
        else:
            prediction_smc = f"SMC: Narxning oshishi kutilmoqda (Bullish). Qo'llab-quvvatlash darajasi {support:.4f}, qarshilik darajasi {resistance:.4f}."
        strategies.append(prediction_smc)

        # Fibonacci tahlili
        fib_retracement = resistance - (resistance - support) * 0.618
        if latest_price > fib_retracement:
            prediction_fib = f"Fibonacci: Narx oshishi kutilmoqda (Bullish Fibonacci). Qo'llab-quvvatlash darajasi {support:.4f}, fib retracement darajasi {fib_retracement:.4f}."
        else:
            prediction_fib = f"Fibonacci: Narxning tushishi kutilmoqda (Bearish Fibonacci). Qo'llab-quvvatlash darajasi {support:.4f}, fib retracement darajasi {fib_retracement:.4f}."
        strategies.append(prediction_fib)

        # Tahlil strategiyalarini ko'rsatish
        st.subheader("Tahlil Natijalari:")
        for strategy in strategies:
            st.write(strategy)

    else:
        st.error("Ma'lumotlar olishda xatolik yuz berdi!")
