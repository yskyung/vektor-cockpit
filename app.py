import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="VEKTOR SIGNALS LIVE", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    .stApp { background-color: #06090e; color: #f1f5f9; font-family: 'Segoe UI', sans-serif; }
    .block-container { padding: 0.5rem 1rem !important; }
    .ticker-bar { background: #0f172a; border: 1px solid #1e293b; border-radius: 6px; padding: 8px 15px; font-size: 13px; font-weight: bold; display: flex; justify-content: space-between; margin-bottom: 8px; }
    .up { color: #00ff88; text-shadow: 0 0 6px rgba(0,255,136,0.4); }
    .down { color: #ef4444; text-shadow: 0 0 6px rgba(239,68,68,0.4); }
    .panel-box { background: #0b0f17; border: 1px solid #1e293b; border-radius: 8px; padding: 12px; margin-bottom: 8px; }
    .panel-header { font-size: 12px; font-weight: 800; color: #94a3b8; border-bottom: 1px solid #1e293b; padding-bottom: 4px; margin-bottom: 8px; letter-spacing: 0.5px; }
    .bot-alert-buy { background: linear-gradient(135deg, #064e3b33 0%, #0b0f17 100%); border: 1.5px solid #00ff88; border-radius: 6px; padding: 10px; box-shadow: 0 0 12px rgba(0,255,136,0.15); }
    .superchat-item { background: #831843; border-left: 3px solid #f43f5e; padding: 6px 8px; border-radius: 4px; font-size: 11px; margin-bottom: 6px; color: #fff; }
    .chat-row { font-size: 11px; margin-bottom: 5px; color: #cbd5e1; }
    .chat-name { font-weight: bold; color: #38bdf8; }
</style>
""", unsafe_allow_html=True)

# 최상단 티커
st.markdown("""
<div class="ticker-bar">
    <span><strong>TSLA</strong> $367.95 <span class="up">▲ +5.51%</span></span>
    <span><strong>NVDA</strong> $128.80 <span class="down">▼ -1.15%</span></span>
    <span><strong>NQ 선물</strong> 20,410.50 <span class="up">▲ +0.65%</span></span>
    <span><strong>IONQ</strong> $8.95 <span class="up">▲ +4.80%</span></span>
    <span><strong>PLTR</strong> $31.20 <span class="up">▲ +2.10%</span></span>
    <span><strong>CRCL</strong> $15.40 <span class="down">▼ -0.80%</span></span>
    <span><strong>BTC</strong> $64,250 <span class="up">▲ +1.20%</span></span>
</div>
""", unsafe_allow_html=True)

@st.cache_data(ttl=60)
def get_data(ticker_symbol):
    df = yf.download(ticker_symbol, period="6mo", interval="1d", auto_adjust=False, progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df = df.loc[:, ~df.columns.duplicated()]
    for c in ['Open', 'High', 'Low', 'Close', 'Volume']:
        if c in df.columns:
            df[c] = pd.Series(df[c].values.flatten(), index=df.index, dtype='float64')
    df['SMA20'] = df['Close'].rolling(20).mean()
    df['STD20'] = df['Close'].rolling(20).std()
    df['BB_Upper'] = df['SMA20'] + (df['STD20'] * 2)
    df['BB_Lower'] = df['SMA20'] - (df['STD20'] * 2)
    delta = df['Close'].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    rs = gain / (loss + 1e-9)
    df['RSI'] = 100 - (100 / (1 + rs))
    return df

# 3열 레이아웃
col_left, col_center, col_right = st.columns([1.1, 2.5, 1.2])

# [좌측 1열] 속보 / 코인 등락 / 봇
with col_left:
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header">🚨 실시간 속보 & 마켓 피드</div>', unsafe_allow_html=True)
    st.markdown('<div style="background:#111827; border-left:3px solid #ef4444; padding:6px 8px; font-size:11px; margin-bottom:6px;"><strong>[BREAKING]</strong> 주요 빅테크 장후 실적 가이던스 발표</div><div style="background:#111827; border-left:3px solid #6366f1; padding:6px 8px; font-size:11px;"><strong>[MACRO]</strong> 나스닥 야간 선물(NQ) 반등 지속 관제</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header">🪙 FINVIZ & COIN 수혜주 등락</div>', unsafe_allow_html=True)
    st.markdown('<table style="width:100%; font-size:12px; border-collapse:collapse;"><tr style="border-bottom:1px solid #1e293b;"><td><strong>COIN</strong></td><td>$215.40</td><td><span class="up">+3.10%</span></td></tr><tr style="border-bottom:1px solid #1e293b;"><td><strong>MSTR</strong></td><td>$142.80</td><td><span class="up">+4.50%</span></td></tr><tr style="border-bottom:1px solid #1e293b;"><td><strong>CRCL</strong></td><td>$15.40</td><td><span class="down">-0.80%</span></td></tr><tr><td><strong>MARA</strong></td><td>$18.20</td><td><span class="up">+2.40%</span></td></tr></table>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header">🤖 VEKTOR BOT REAL-TIME</div>', unsafe_allow_html=True)
    st.markdown('<div class="bot-alert-buy"><div style="color:#00ff88; font-weight:bold; font-size:12px;">● TSLA OVERSOLD ACCUMULATION</div><div style="color:#cbd5e1; font-size:11px; line-height:1.4; margin-top:4px;">• 종가 $367.95 (RSI 32.4)<br>• 볼린저 하단 지지 포착<br>• 야간 선물 지지 확인 후 분할 매집 유효</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# [중앙 2열] 정중앙 차트 + 하단 히트맵
with col_center:
    ctrl1, ctrl2 = st.columns([2, 1])
    with ctrl1:
        st.markdown("<h4 style='margin:0; padding:0; color:#fff;'>⚡ VEKTOR FINVIZ ADVANCED CHART</h4>", unsafe_allow_html=True)
    with ctrl2:
        selected_ticker = st.selectbox("종목", ["TSLA", "NVDA", "IONQ", "PLTR", "CRCL"], label_visibility="collapsed")
    
    try:
        data = get_data(selected_ticker)
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.04, row_heights=[0.7, 0.3])
        fig.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name='Price', increasing_line_color='#00ff88', decreasing_line_color='#ef4444'), row=1, col=1)
        fig.add_trace(go.Scatter(x=data.index, y=data['BB_Upper'], line=dict(color='#38bdf8', width=1, dash='dot'), name='BB Up'), row=1, col=1)
        fig.add_trace(go.Scatter(x=data.index, y=data['BB_Lower'], line=dict(color='#38bdf8', width=1, dash='dot'), name='BB Low'), row=1, col=1)
        fig.add_trace(go.Scatter(x=data.index, y=data['SMA20'], line=dict(color='#f59e0b', width=1.5), name='20 SMA'), row=1, col=1)
        fig.add_trace(go.Scatter(x=data.index, y=data['RSI'], line=dict(color='#c084fc', width=2), name='RSI'), row=2, col=1)
        fig.add_hline(y=70, line_dash="dash", line_color="#ef4444", row=2, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="#00ff88", row=2, col=1)
        fig.update_layout(template="plotly_dark", paper_bgcolor="#0b0f17", plot_bgcolor="#0f172a", height=340, margin=dict(l=5, r=5, t=5, b=5), xaxis_rangeslider_visible=False, legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="right", x=1))
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Chart Load Error: {e}")

    st.markdown('<div class="panel-header" style="margin-top:4px;">🗺️ FINVIZ SECTOR HEATMAP (S&P 500 & TECH)</div>', unsafe_allow_html=True)
    heat_df = pd.DataFrame({"Sector": ["Tech", "Tech", "Auto", "Quantum/AI", "Quantum/AI", "Crypto", "Tech", "Tech"], "Ticker": ["NVDA", "AAPL", "TSLA", "PLTR", "IONQ", "CRCL", "MSFT", "AMZN"], "MarketCap": [3100, 3300, 1100, 70, 20, 15, 3000, 1900], "Change": [-1.15, 0.45, 5.51, 2.10, 4.80, -0.80, 0.85, 1.10]})
    fig_h = px.treemap(heat_df, path=["Sector", "Ticker"], values="MarketCap", color="Change", color_continuous_scale=["#ef4444", "#1e293b", "#00ff88"], color_continuous_midpoint=0)
    fig_h.update_layout(template="plotly_dark", paper_bgcolor="#0b0f17", height=230, margin=dict(l=2, r=2, t=2, b=2))
    st.plotly_chart(fig_h, use_container_width=True)

# [우측 3열] 실시간 비디오 + 채팅방
with col_right:
    st.markdown('<div class="panel-box" style="text-align:center;">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header">🔴 BROADCAST LIVE STREAM</div>', unsafe_allow_html=True)
    st.markdown('<div style="background:#000000; border:1px solid #334155; border-radius:6px; height:180px; display:flex; flex-direction:column; justify-content:center; align-items:center;"><div style="font-size:26px;">🔴 LIVE</div><div style="color:#94a3b8; font-size:12px; margin-top:4px;">[캘리포니아 경박사 라이브 캠]</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header">💬 LIVE CHAT & SUPER CHAT</div>', unsafe_allow_html=True)
    st.markdown('<div style="height:250px; overflow-y:auto; padding-right:4px;"><div class="superchat-item"><strong>서학개미1호</strong> 님 $50.00 슈퍼챗<br>"경박사님 TSLA 볼린저 하단 보고 진입했습니다!"</div><div class="chat-row"><span class="chat-name">캘리포니아팬:</span> 오늘 야간 선물 흐름 좋네요.</div><div class="chat-row"><span class="chat-name">뉴욕트레이더:</span> Vektor 봇 타점 정확합니다.</div></div>', unsafe_allow_html=True)
    st.text_input("메시지", placeholder="실시간 채팅 메시지 입력...", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
