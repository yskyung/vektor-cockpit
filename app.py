import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import streamlit.components.v1 as components

# 1. 페이지 및 다크 테마 설정
st.set_page_config(page_title="VEKTOR SIGNALS LIVE", layout="wide", initial_sidebar_state="collapsed")

# 2. 글로벌 CSS 스타일 (티커 테이프, 네온 컬러 체인징, 펄스 애니메이션)
st.markdown("""
<style>
    .stApp { background-color: #06090e; color: #f1f5f9; font-family: 'Segoe UI', -apple-system, sans-serif; }
    .block-container { padding: 0.2rem 0.6rem !important; }
    
    /* 4차 산업 50대 종목 롤링 티커 전광판 */
    .ticker-wrap {
        width: 100%;
        overflow: hidden;
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 6px;
        padding: 5px 0;
        margin-bottom: 6px;
        white-space: nowrap;
        box-shadow: 0 2px 8px rgba(0,0,0,0.6);
    }
    .ticker-move {
        display: inline-block;
        white-space: nowrap;
        animation: ticker 45s linear infinite;
    }
    .ticker-move:hover { animation-play-state: paused; }
    @keyframes ticker {
        0% { transform: translate3d(0, 0, 0); }
        100% { transform: translate3d(-50%, 0, 0); }
    }
    .ticker-item {
        display: inline-block;
        padding: 0 14px;
        font-size: 11.5px;
        font-weight: 700;
        color: #e2e8f0;
    }
    .ticker-item strong { color: #38bdf8; font-weight: 800; margin-right: 3px; }
    .up { color: #00ff88; text-shadow: 0 0 6px rgba(0,255,136,0.3); }
    .down { color: #ef4444; text-shadow: 0 0 6px rgba(239,68,68,0.3); }

    /* 패널 공통 */
    .panel-box {
        background: #0b0f17;
        border: 1px solid #1e293b;
        border-radius: 6px;
        padding: 8px;
        margin-bottom: 6px;
    }
    .panel-header {
        font-size: 11px;
        font-weight: 800;
        color: #94a3b8;
        border-bottom: 1px solid #1e293b;
        padding-bottom: 3px;
        margin-bottom: 5px;
        letter-spacing: 0.5px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* Vektor 봇 네온 컬러 체인징 애니메이션 */
    @keyframes pulse-green {
        0% { box-shadow: 0 0 5px rgba(0,255,136,0.3); border-color: #00ff88; }
        50% { box-shadow: 0 0 16px rgba(0,255,136,0.8); border-color: #34d399; }
        100% { box-shadow: 0 0 5px rgba(0,255,136,0.3); border-color: #00ff88; }
    }
    @keyframes pulse-blue {
        0% { box-shadow: 0 0 5px rgba(56,189,248,0.3); border-color: #38bdf8; }
        50% { box-shadow: 0 0 16px rgba(56,189,248,0.8); border-color: #60a5fa; }
        100% { box-shadow: 0 0 5px rgba(56,189,248,0.3); border-color: #38bdf8; }
    }
    .bot-card-buy {
        background: linear-gradient(135deg, rgba(6,78,59,0.35) 0%, #0b0f17 100%);
        border: 1.5px solid #00ff88;
        border-radius: 6px;
        padding: 8px;
        animation: pulse-green 2.5s infinite;
        margin-bottom: 6px;
    }
    .bot-card-macro {
        background: linear-gradient(135deg, rgba(30,58,138,0.35) 0%, #0b0f17 100%);
        border: 1.5px solid #38bdf8;
        border-radius: 6px;
        padding: 8px;
        animation: pulse-blue 3s infinite;
    }
    
    /* 마켓 브레스 카드 */
    .breadth-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 4px;
        padding: 4px 6px;
        font-size: 9px;
    }
    .breadth-title { display: flex; justify-content: space-between; font-weight: bold; margin-bottom: 3px; }
    .bar-container { width: 100%; height: 5px; background: #ef4444; border-radius: 3px; overflow: hidden; display: flex; }
</style>
""", unsafe_allow_html=True)

# 3. 최상단 롤링 전광판 (4차산업 50개 종목 리스트)
TICKERS = [
    'GOOG', 'META', 'TSLA', 'NVDA', 'AMZN', 'LMT', 'NOC', 'LHX', 'RKLB', 'ASTS',
    'SPCX', 'IBM', 'IONQ', 'RGTI', 'PLTR', 'ORCL', 'MU', 'INTC', 'SNDK', 'AVGO',
    'AMD', 'AMAT', 'LRCX', 'ASML', 'MP', 'CRML', 'OKLO', 'SMR', 'LEU', 'VIST',
    'FN', 'COHR', 'MRVL', 'GLW', 'AAOI', 'WMT', 'COST', 'HD', 'LLY', 'MRNA',
    'CRSP', 'UMAC', 'ONDS', 'KTOS', 'AVAV', 'XOM', 'CVX'
]

@st.cache_data(ttl=60)
def load_ticker_prices():
    data = []
    try:
        tickers_str = " ".join(TICKERS[:25])
        df = yf.download(tickers_str, period="2d", interval="1d", progress=False)['Close']
        for t in TICKERS[:25]:
            if t in df.columns:
                series = df[t].dropna()
                if len(series) >= 2:
                    curr, prev = float(series.iloc[-1]), float(series.iloc[-2])
                    chg = ((curr - prev) / prev) * 100
                    data.append((t, curr, chg))
                elif len(series) == 1:
                    data.append((t, float(series.iloc[-1]), 0.0))
    except:
        pass
    fallback = [
        ('TSLA', 367.95, 5.51), ('NVDA', 128.80, -0.23), ('PLTR', 31.20, 2.10),
        ('IONQ', 8.95, 4.80), ('MU', 114.50, -0.29), ('AVGO', 168.40, 0.26),
        ('AMD', 148.20, -0.24), ('GLW', 42.10, 0.85), ('COHR', 78.50, 3.40),
        ('OKLO', 12.30, 6.70), ('RKLB', 7.45, 3.20), ('ASTS', 28.50, 4.10),
        ('LMT', 568.20, 0.80), ('LLY', 945.10, 0.43), ('GOOG', 165.30, 0.08),
        ('META', 510.40, -0.06), ('AMZN', 178.50, 0.17), ('XOM', 118.40, 0.15),
        ('IBM', 198.20, 1.10), ('KTOS', 23.40, 1.80), ('AVAV', 195.00, 2.40),
        ('INTC', 21.80, 0.20), ('ASML', 840.00, -0.50), ('SMR', 10.80, 5.20)
    ]
    return data if len(data) >= 10 else fallback

prices = load_ticker_prices()
items_html = ""
for t, p, c in prices:
    cls = "up" if c >= 0 else "down"
    arrow = "▲" if c >= 0 else "▼"
    items_html += f'<span class="ticker-item"><strong>{t}</strong> ${p:,.2f} <span class="{cls}">{arrow} {c:+.2f}%</span></span>'

st.markdown(f'<div class="ticker-wrap"><div class="ticker-move">{items_html} {items_html}</div></div>', unsafe_allow_html=True)

# 4. 3열 그리드 분할 (좌 1.05 : 중 2.7 : 우 1.15)
col_left, col_center, col_right = st.columns([1.05, 2.7, 1.15])

# =========================================================
# [좌측 1열] VEKTOR AI 실시간 아나운서 봇 & 시그널 & 속보
# =========================================================
with col_left:
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header">🤖 VEKTOR AI ANNOUNCER BOT <span style="color:#00ff88; font-size:9px;">● LIVE ON-AIR</span></div>', unsafe_allow_html=True)
    
    # 1. 색상 변화 네온 펄스 시그널 카드 (매수/과매도)
    st.markdown("""
    <div class="bot-card-buy">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="color:#00ff88; font-weight:800; font-size:11px;">⚡ [BUY SIGNAL] TSLA OVERSOLD</span>
            <span style="background:#059669; color:#fff; font-size:9px; padding:1px 4px; border-radius:3px;">ACCUMULATE</span>
        </div>
        <div style="color:#cbd5e1; font-size:10px; line-height:1.4; margin-top:4px;">
            • 현재가: $367.95 (RSI 32.4)<br>
            • 볼린저 하단 지지 및 거래량 반등 포착<br>
            • <strong>경박사 앵커 브리핑:</strong> "야간 선물 지지선을 확인하며 분할 매수 타점 유효합니다."
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. 색상 변화 네온 펄스 매크로 카드 (블루)
    st.markdown("""
    <div class="bot-card-macro">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="color:#38bdf8; font-weight:800; font-size:11px;">🌐 [MACRO BOT] NQ 야간선물</span>
            <span style="background:#2563eb; color:#fff; font-size:9px; padding:1px 4px; border-radius:3px;">BULLISH</span>
        </div>
        <div style="color:#cbd5e1; font-size:10px; line-height:1.4; margin-top:4px;">
            • NQ 선물 20,410.50 (+0.65%) 반등 지속<br>
            • 10년물 국채금리 안정세, 4차산업 섹터 수급 유입
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 3. 실시간 AI 아나운서 음성(TTS) 리딩 버튼 컴포넌트
    tts_html = """
    <div style="margin-top:6px; text-align:center;">
        <button onclick="speakAlert()" style="width:100%; background:linear-gradient(90deg, #1e293b 0%, #0f172a 100%); border:1px solid #00ff88; color:#00ff88; font-weight:bold; font-size:11px; padding:6px 0; border-radius:4px; cursor:pointer; box-shadow:0 0 8px rgba(0,255,136,0.2);">
            🎙️ AI 아나운서 음성 브리핑 듣기
        </button>
    </div>
    <script>
    function speakAlert() {
        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel();
            var text = "캘리포니아 경박사 Vektor AI 긴급 시그널 브리핑입니다. 테슬라 종가 367달러 선에서 볼린저 밴드 하단 지지와 과매도 신호가 감지되었습니다. 야간 선물 반등 흐름에 맞춰 분할 매집 전략이 유효합니다.";
            var msg = new SpeechSynthesisUtterance(text);
            msg.lang = 'ko-KR';
            msg.rate = 0.95;
            window.speechSynthesis.speak(msg);
        } else {
            alert('이 브라우저는 음성 합성을 지원하지 않습니다.');
        }
    }
    </script>
    """
    components.html(tts_html, height=45)
    st.markdown('</div>', unsafe_allow_html=True)

    # 4. 실시간 속보 & 코인 수혜주
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header">🚨 실시간 속보 & 마켓 피드</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#111827; border-left:3px solid #ef4444; padding:4px 6px; font-size:10px; margin-bottom:4px;">
        <strong>[BREAKING]</strong> 빅테크 AI 가이던스 상향 발표
    </div>
    <div style="background:#111827; border-left:3px solid #6366f1; padding:4px 6px; font-size:10px;">
        <strong>[QUANTUM]</strong> 아이온큐(IONQ) 양자 네트워킹 수주 소식
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header">🪙 FINVIZ & COIN 수혜주 등락</div>', unsafe_allow_html=True)
    st.markdown("""
    <table style="width:100%; font-size:11px; border-collapse:collapse;">
        <tr style="border-bottom:1px solid #1e293b;"><td><strong>COIN</strong></td><td>$215.40</td><td><span class="up">+3.10%</span></td></tr>
        <tr style="border-bottom:1px solid #1e293b;"><td><strong>MSTR</strong></td><td>$142.80</td><td><span class="up">+4.50%</span></td></tr>
        <tr style="border-bottom:1px solid #1e293b;"><td><strong>CRCL</strong></td><td>$15.40</td><td><span class="down">-0.80%</span></td></tr>
        <tr><td><strong>MARA</strong></td><td>$18.20</td><td><span class="up">+2.40%</span></td></tr>
    </table>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# [중앙 2열] 상단 1/3: 4대 지표 미니 차트 + 하단 2/3: S&P 500 풀 섹터 히트맵
# =========================================================
with col_center:
    def create_mini_chart(title, change_str, current_val, up=True):
        times = ["10AM", "11AM", "12PM", "1PM", "2PM", "3PM", "4PM"]
        np.random.seed(42 if "S&P" in title else (7 if "NASDAQ" in title else 15))
        opens = np.linspace(100, 105 if up else 98, 7) + np.random.randn(7)*0.8
        closes = opens + np.random.randn(7)*1.2
        highs = np.maximum(opens, closes) + 0.5
        lows = np.minimum(opens, closes) - 0.5

        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=times, open=opens, high=highs, low=lows, close=closes, increasing_line_color='#00ff88', decreasing_line_color='#ef4444', increasing_fillcolor='#00ff88', decreasing_fillcolor='#ef4444'))
        fig.add_hline(y=opens[0], line_dash="dash", line_color="#ef4444" if not up else "#38bdf8", line_width=1)
        fig.update_layout(template="plotly_dark", paper_bgcolor="#0f172a", plot_bgcolor="#0f172a", height=115, margin=dict(l=2, r=2, t=18, b=10), xaxis_rangeslider_visible=False, showlegend=False, title=dict(text=f"<b>{title}</b> <span style='color:{'#00ff88' if up else '#ef4444'}; font-size:9px;'>{change_str}</span> <b style='color:#facc15; font-size:10px;'>{current_val}</b>", font=dict(size=10, color="#cbd5e1"), x=0.02, y=0.98))
        fig.update_xaxes(showgrid=True, gridcolor="#1e293b", tickfont=dict(size=7))
        fig.update_yaxes(showgrid=True, gridcolor="#1e293b", tickfont=dict(size=7), side="right")
        return fig

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.plotly_chart(create_mini_chart("S&P 500", "-25.62 (0.33%)", "7686.14", False), use_container_width=True)
    with c2: st.plotly_chart(create_mini_chart("NASDAQ", "-31.53 (0.12%)", "26370.9", False), use_container_width=True)
    with c3: st.plotly_chart(create_mini_chart("DOW", "-374.09 (0.70%)", "53185.9", False), use_container_width=True)
    with c4: st.plotly_chart(create_mini_chart("RUSSELL 2000", "-1.82 (0.62%)", "293.93", False), use_container_width=True)

    b1, b2, b3, b4, b5 = st.columns(5)
    with b1: st.markdown('<div class="breadth-card"><div class="breadth-title"><span style="color:#00ff88;">Adv 35.1%</span><span style="color:#ef4444;">Dec 60.4%</span></div><div class="bar-container"><div style="width:35.1%; background:#00ff88;"></div></div></div>', unsafe_allow_html=True)
    with b2: st.markdown('<div class="breadth-card"><div class="breadth-title"><span style="color:#00ff88;">High 26.1%</span><span style="color:#ef4444;">Low 73.9%</span></div><div class="bar-container"><div style="width:26.1%; background:#00ff88;"></div></div></div>', unsafe_allow_html=True)
    with b3: st.markdown('<div class="breadth-card"><div class="breadth-title"><span style="color:#00ff88;">>SMA50 46.9%</span><span style="color:#ef4444;">53.1%</span></div><div class="bar-container"><div style="width:46.9%; background:#00ff88;"></div></div></div>', unsafe_allow_html=True)
    with b4: st.markdown('<div class="breadth-card"><div class="breadth-title"><span style="color:#00ff88;">>SMA200 51.2%</span><span style="color:#ef4444;">48.8%</span></div><div class="bar-container"><div style="width:51.2%; background:#00ff88;"></div></div></div>', unsafe_allow_html=True)
    with b5: st.markdown('<div class="breadth-card"><div class="breadth-title"><span style="color:#00ff88;">BULL 53%</span><span style="color:#ef4444;">BEAR 47%</span></div><div class="bar-container"><div style="width:53%; background:#00ff88;"></div></div></div>', unsafe_allow_html=True)

    st.markdown('<div class="panel-header" style="margin-top:6px;">🗺️ S&P 500 - Aftermarket Performance (FINVIZ FULL SECTOR MAP)</div>', unsafe_allow_html=True)
    
    full_heat_data = pd.DataFrame([
        {"Sector": "Technology", "Sub": "Semiconductors", "Ticker": "NVDA", "MarketCap": 3100, "Change": -0.23},
        {"Sector": "Technology", "Sub": "Semiconductors", "Ticker": "AVGO", "MarketCap": 800, "Change": 0.26},
        {"Sector": "Technology", "Sub": "Semiconductors", "Ticker": "AMD", "MarketCap": 250, "Change": -0.24},
        {"Sector": "Technology", "Sub": "Semiconductors", "Ticker": "MU", "MarketCap": 120, "Change": -0.29},
        {"Sector": "Technology", "Sub": "Semiconductors", "Ticker": "INTC", "MarketCap": 90, "Change": 0.20},
        {"Sector": "Technology", "Sub": "Semiconductors", "Ticker": "QCOM", "MarketCap": 180, "Change": -0.10},
        {"Sector": "Technology", "Sub": "Semiconductors", "Ticker": "TXN", "MarketCap": 180, "Change": 0.20},
        {"Sector": "Technology", "Sub": "Semiconductors", "Ticker": "LRCX", "MarketCap": 110, "Change": 0.23},
        {"Sector": "Technology", "Sub": "Semiconductors", "Ticker": "AMAT", "MarketCap": 170, "Change": -0.23},
        {"Sector": "Technology", "Sub": "Consumer Elec", "Ticker": "AAPL", "MarketCap": 3400, "Change": 0.05},
        {"Sector": "Technology", "Sub": "Software", "Ticker": "MSFT", "MarketCap": 3100, "Change": 0.09},
        {"Sector": "Technology", "Sub": "Software", "Ticker": "PLTR", "MarketCap": 80, "Change": 0.09},
        {"Sector": "Technology", "Sub": "Software", "Ticker": "ORCL", "MarketCap": 380, "Change": 0.13},
        {"Sector": "Technology", "Sub": "Software", "Ticker": "CRM", "MarketCap": 290, "Change": 0.20},
        {"Sector": "Technology", "Sub": "Hardware", "Ticker": "DELL", "MarketCap": 90, "Change": 0.88},
        {"Sector": "Technology", "Sub": "Hardware", "Ticker": "CSCO", "MarketCap": 200, "Change": 0.14},
        {"Sector": "Consumer Cyclical", "Sub": "E-Commerce", "Ticker": "AMZN", "MarketCap": 2000, "Change": 0.17},
        {"Sector": "Consumer Cyclical", "Sub": "Auto", "Ticker": "TSLA", "MarketCap": 1100, "Change": -0.14},
        {"Sector": "Consumer Cyclical", "Sub": "Retail", "Ticker": "HD", "MarketCap": 400, "Change": -0.05},
        {"Sector": "Consumer Cyclical", "Sub": "Restaurants", "Ticker": "MCD", "MarketCap": 210, "Change": 0.31},
        {"Sector": "Communication Services", "Sub": "Internet", "Ticker": "GOOGL", "MarketCap": 2100, "Change": 0.08},
        {"Sector": "Communication Services", "Sub": "Internet", "Ticker": "META", "MarketCap": 1400, "Change": -0.06},
        {"Sector": "Communication Services", "Sub": "Media", "Ticker": "NFLX", "MarketCap": 300, "Change": -0.04},
        {"Sector": "Healthcare", "Sub": "Pharma", "Ticker": "LLY", "MarketCap": 850, "Change": 0.43},
        {"Sector": "Healthcare", "Sub": "Pharma", "Ticker": "JNJ", "MarketCap": 390, "Change": 0.21},
        {"Sector": "Healthcare", "Sub": "Pharma", "Ticker": "ABBV", "MarketCap": 340, "Change": 0.60},
        {"Sector": "Healthcare", "Sub": "Managed", "Ticker": "UNH", "MarketCap": 500, "Change": 0.28},
        {"Sector": "Financial", "Sub": "Banks", "Ticker": "JPM", "MarketCap": 650, "Change": 0.00},
        {"Sector": "Financial", "Sub": "Banks", "Ticker": "BAC", "MarketCap": 310, "Change": 0.18},
        {"Sector": "Financial", "Sub": "Invest", "Ticker": "BRK-B", "MarketCap": 950, "Change": 0.02},
        {"Sector": "Financial", "Sub": "Credit", "Ticker": "V", "MarketCap": 560, "Change": 0.17},
        {"Sector": "Financial", "Sub": "Credit", "Ticker": "MA", "MarketCap": 440, "Change": 0.61},
        {"Sector": "Industrials", "Sub": "Aero", "Ticker": "GE", "MarketCap": 200, "Change": 0.09},
        {"Sector": "Industrials", "Sub": "Aero", "Ticker": "CAT", "MarketCap": 170, "Change": 0.19},
        {"Sector": "Energy", "Sub": "Oil", "Ticker": "XOM", "MarketCap": 460, "Change": 0.15},
        {"Sector": "Energy", "Sub": "Oil", "Ticker": "CVX", "MarketCap": 280, "Change": 0.35},
        {"Sector": "Consumer Defensive", "Sub": "Discount", "Ticker": "WMT", "MarketCap": 600, "Change": -0.07},
        {"Sector": "Consumer Defensive", "Sub": "Discount", "Ticker": "COST", "MarketCap": 380, "Change": 0.04},
        {"Sector": "Consumer Defensive", "Sub": "Beverage", "Ticker": "KO", "MarketCap": 290, "Change": 0.29},
        {"Sector": "Consumer Defensive", "Sub": "Household", "Ticker": "PG", "MarketCap": 390, "Change": -0.11},
    ])

    fig_full_heat = px.treemap(full_heat_data, path=["Sector", "Sub", "Ticker"], values="MarketCap", color="Change", color_continuous_scale=["#991b1b", "#1e293b", "#065f46", "#047857", "#00ff88"], color_continuous_midpoint=0)
    fig_full_heat.update_traces(texttemplate="<b>%{label}</b><br>%{color:+.2f}%", textfont=dict(size=10, color="#ffffff"))
    fig_full_heat.update_layout(template="plotly_dark", paper_bgcolor="#0b0f17", height=380, margin=dict(l=2, r=2, t=2, b=2), coloraxis_showscale=False)
    st.plotly_chart(fig_full_heat, use_container_width=True)

# =========================================================
# [우측 3열] 방송 실시간 비디오 송출 + 라이브 채팅 & 슈퍼챗
# =========================================================
with col_right:
    st.markdown('<div class="panel-box" style="text-align:center;"><div class="panel-header">🔴 BROADCAST LIVE STREAM</div><div style="background:#000000; border:1px solid #334155; border-radius:6px; height:180px; display:flex; flex-direction:column; justify-content:center; align-items:center;"><div style="font-size:26px;">🔴 LIVE</div><div style="color:#94a3b8; font-size:11px; margin-top:4px;">[캘리포니아 경박사 라이브 캠]</div></div></div>', unsafe_allow_html=True)
    st.markdown('<div class="panel-box"><div class="panel-header">💬 LIVE CHAT & SUPER CHAT</div><div style="height:270px; overflow-y:auto; padding-right:4px;"><div style="background:#831843; border-left:3px solid #f43f5e; padding:5px 8px; border-radius:4px; font-size:11px; margin-bottom:5px; color:#fff;"><strong>서학개미1호</strong> $50.00 슈퍼챗<br>"경박사님 Vektor 봇 네온 시그널과 음성 브리핑 진짜 방송용으로 대박입니다!"</div><div style="font-size:11px; margin-bottom:4px; color:#cbd5e1;"><strong style="color:#38bdf8;">캘리포니아팬:</strong> 봇이 아나운서처럼 실시간 타점 읽어주니 몰입감이 엄청납니다.</div><div style="font-size:11px; margin-bottom:4px; color:#cbd5e1;"><strong style="color:#38bdf8;">뉴욕트레이더:</strong> 상단 50대 티커 롤링과 히트맵 조합 완벽하네요.</div></div><input type="text" placeholder="실시간 메시지 입력..." style="width:100%; background:#0f172a; border:1px solid #1e293b; color:#fff; padding:6px; border-radius:4px; font-size:11px;"></div>', unsafe_allow_html=True)
