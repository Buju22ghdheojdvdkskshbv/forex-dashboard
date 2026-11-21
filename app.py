import streamlit as st
import yfinance as yf
import pandas as pd
st.set_page_config(page_title='Forex & Crypto Analyst', layout='centered')
st.title('📊 FOREX & CRYPTO ANALYST')
st.caption('Market data • Technical analysis • Research')
m = st.selectbox('MARKET', ['Forex', 'Cryptocurrency'])
if m == 'Forex':
    p = st.selectbox('PAIR / ASSET', ['EURUSD=X', 'GBPUSD=X', 'USDJPY=X'])
else:
    p = st.selectbox('PAIR / ASSET', ['BTC-USD', 'ETH-USD', 'SOL-USD'])
tf = st.selectbox('TIMEFRAME', ['1h', '4h', '1d'])
if st.button('Analyse market', type='primary'):
    with st.spinner('Analyzing market...'):
        df = yf.download(p, period='1mo', interval='1d')
    if not df.empty:
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
        price = float(df['Close'].iloc[-1].item())
        sl = price * 0.99
        tp = price * 1.02
        delta = df['Close'].diff()
        gain = delta.clip(lower=0).rolling(14).mean()
        loss = (-delta.clip(upper=0)).rolling(14).mean()
        rsi = 100 - (100 / (1 + (gain / loss)))
        curr_rsi = float(rsi.iloc[-1].item()) if not rsi.empty and not pd.isna(rsi.iloc[-1]) else 50.0
        bias = 'BULLISH (Oversold)' if curr_rsi < 30 else ('BEARISH (Overbought)' if curr_rsi > 70 else 'MIXED / UNCLEAR')
        res = 'BUY' if curr_rsi < 30 else ('SELL' if curr_rsi > 70 else 'WAIT')
        c1, c2 = st.columns(2)
        c1.metric('Current price', f'{price:,.4f}')
        c2.metric('Market bias', bias)
        c3, c4 = st.columns(2)
        c3.metric('Analysis result', res)
        c4.metric('RSI (14)', f'{curr_rsi:.5f}')
        st.subheader('🎯 Trade Risk Levels')
        s1, s2 = st.columns(2)
        s1.metric('Stop Loss (SL)', f'{sl:,.4f}', '-1%')
        s2.metric('Take Profit (TP)', f'{tp:,.4f}', '+2%')
        st.subheader('Recent price history')
        st.line_chart(df['Close'])
    else:
        st.error('Could not fetch data.')
else:
    st.info('Select your options and click **Analyse market**.')
