import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# 1. 페이지 및 와이드 다크 테마 설정
st.set_page_config(page_title="VEKTOR SIGNALS LIVE", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    .stApp { background-color: #06090e; color: #f1f5f9; font-family: 'Segoe UI', sans-serif; }
    .block-container { padding: 0.3rem 0.6rem !important; }
    
    /* 최상단 티커 */
    .ticker-bar {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 6px;
        padding: 5px 12px;
        font-size: 12px;
        font-weight: bold;
        display: flex;
        justify-content: space-between;
        margin-bottom: 6px;
    }
    .up { color: #00ff88; }
    .down { color: #ef4444; }
    
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
    }
    
    /* 봇 카드 */
    .bot-alert {
        background: linear-gradient(135deg, #064e3b33 0%, #0b0f17 100%);
        border: 1.5px solid #00ff88;
        border-radius: 6px;
        padding: 8px;
    }
    
    /* 브레스 카드 */
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

# 최상단 티커 테이프
st.markdown("""
<div class="ticker-bar">
    <span><strong>TSLA</strong> $367.95 <span class="up">▲ +5.51%</span></span>
    <span><strong>NVDA</strong> $128.80 <span class="down">▼ -0.23%</span></span>
    <span><strong>NQ 선물</strong> 20,410.50 <span class="up">▲ +0.65%</span></span>
    <span><strong>IONQ</strong> $8.95 <span class="up">▲ +4.80%</span></span>
    <span><strong>PLTR</strong> $31.20 <span class="up">▲ +2.10%</span></span>
    <span><strong>CRCL</strong> $15.40 <span class="down">▼ -0.80%</span></span>
    <span><strong>BTC</strong> $64,250 <span class="up">▲ +1.20%</span></span>
</div>
""", unsafe_allow_html=True)

# 3열 분할 (좌측 1.05 : 중앙 2.7 : 우측 1.15)
col_left, col_center, col_right = st.columns([1.05, 2.7, 1.15])

# =========================================================
# [좌측 1열] 속보 / Finviz & COIN / Vektor Bot
# =========================================================
with col_left:
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header">🚨 실시간 속보 & 마켓 피드</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#111827; border-left:3px solid #ef4444; padding:4px 6px; font-size:10px; margin-bottom:4px;">
        <strong>[BREAKING]</strong> 빅테크 장후 실적 가이던스 발표
    </div>
    <div style="background:#111827; border-left:3px solid #6366f1; padding:4px 6px; font-size:10px;">
        <strong>[MACRO]</strong> 나스닥 야간 선물(NQ) 반등 지속 관제
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

    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header">🤖 VEKTOR BOT REAL-TIME</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="bot-alert">
        <div style="color:#00ff88; font-weight:bold; font-size:11px;">● TSLA OVERSOLD ACCUMULATION</div>
        <div style="color:#cbd5e1; font-size:10px; line-height:1.4; margin-top:3px;">
            • 종가 $367.95 (RSI 32.4)<br>
            • 볼린저 하단 지지 및 골든크로스<br>
            • 야간 선물 지지 확인 후 분할 매집 유효
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# [중앙 2열] 상단 1/3: 4대 지표 미니 차트 + 하단 2/3: S&P 500 히트맵
# =========================================================
with col_center:
    # 1. 4대 지수 미니 차트
    def create_mini_chart(title, change_str, current_val, up=True):
        times = ["10AM", "11AM", "12PM", "1PM", "2PM", "3PM", "4PM"]
        np.random.seed(42 if "S&P" in title else (7 if "NASDAQ" in title else 15))
        opens = np.linspace(100, 105 if up else 98, 7) + np.random.randn(7)*0.8
        closes = opens + np.random.randn(7)*1.2
        highs = np.maximum(opens, closes) + 0.5
        lows = np.minimum(opens, closes) - 0.5

        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=times, open=opens, high=highs, low=lows, close=closes,
            increasing_line_color='#00ff88', decreasing_line_color='#ef4444',
            increasing_fillcolor='#00ff88', decreasing_fillcolor='#ef4444'
        ))
        fig.add_hline(y=opens[0], line_dash="dash", line_color="#ef4444" if not up else "#38bdf8", line_width=1)
        fig.update_layout(
            template="plotly_dark", paper_bgcolor="#0f172a", plot_bgcolor="#0f172a",
            height=115, margin=dict(l=2, r=2, t=18, b=10),
            xaxis_rangeslider_visible=False, showlegend=False,
            title=dict(text=f"<b>{title}</b> <span style='color:{'#00ff88' if up else '#ef4444'}; font-size:9px;'>{change_str}</span> <b style='color:#facc15; font-size:10px;'>{current_val}</b>", font=dict(size=10, color="#cbd5e1"), x=0.02, y=0.98)
        )
        fig.update_xaxes(showgrid=True, gridcolor="#1e293b", tickfont=dict(size=7))
        fig.update_yaxes(showgrid=True, gridcolor="#1e293b", tickfont=dict(size=7), side="right")
        return fig

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.plotly_chart(create_mini_chart("S&P 500", "-25.62 (0.33%)", "7686.14", False), use_container_width=True)
    with c2: st.plotly_chart(create_mini_chart("NASDAQ", "-31.53 (0.12%)", "26370.9", False), use_container_width=True)
    with c3: st.plotly_chart(create_mini_chart("DOW", "-374.09 (0.70%)", "53185.9", False), use_container_width=True)
    with c4: st.plotly_chart(create_mini_chart("RUSSELL 2000", "-1.82 (0.62%)", "293.93", False), use_container_width=True)

    # 2. 마켓 브레스 바
    b1, b2, b3, b4, b5 = st.columns(5)
    with b1:
        st.markdown('<div class="breadth-card"><div class="breadth-title"><span style="color:#00ff88;">Adv 35.1%</span><span style="color:#ef4444;">Dec 60.4%</span></div><div class="bar-container"><div style="width:35.1%; background:#00ff88;"></div></div></div>', unsafe_allow_html=True)
    with b2:
        st.markdown('<div class="breadth-card"><div class="breadth-title"><span style="color:#00ff88;">High 26.1%</span><span style="color:#ef4444;">Low 73.9%</span></div><div class="bar-container"><div style="width:26.1%; background:#00ff88;"></div></div></div>', unsafe_allow_html=True)
    with b3:
        st.markdown('<div class="breadth-card"><div class="breadth-title"><span style="color:#00ff88;">>SMA50 46.9%</span><span style="color:#ef4444;">53.1%</span></div><div class="bar-container"><div style="width:46.9%; background:#00ff88;"></div></div></div>', unsafe_allow_html=True)
    with b4:
        st.markdown('<div class="breadth-card"><div class="breadth-title"><span style="color:#00ff88;">>SMA200 51.2%</span><span style="color:#ef4444;">48.8%</span></div><div class="bar-container"><div style="width:51.2%; background:#00ff88;"></div></div></div>', unsafe_allow_html=True)
    with b5:
        st.markdown('<div class="breadth-card"><div class="breadth-title"><span style="color:#00ff88;">BULL 53%</span><span style="color:#ef4444;">BEAR 47%</span></div><div class="bar-container"><div style="width:53%; background:#00ff88;"></div></div></div>', unsafe_allow_html=True)

    # 3. 중앙 하단 2/3: S&P 500 Aftermarket Performance 전체 섹터 히트맵
    st.markdown('<div class="panel-header" style="margin-top:6px;">🗺️ S&P 500 - Aftermarket Performance (FINVIZ FULL SECTOR MAP)</div>', unsafe_allow_html=True)
    
    # 세부 섹터 데이터셋 (보내주신 Finviz 히트맵 완벽 매핑)
    full_heat_data = pd.DataFrame([
        # TECHNOLOGY
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
        {"Sector": "Technology", "Sub": "Software", "Ticker": "ADBE", "MarketCap": 240, "Change": -0.15},
        {"Sector": "Technology", "Sub": "Software", "Ticker": "NOW", "MarketCap": 190, "Change": 0.05},
        {"Sector": "Technology", "Sub": "Software", "Ticker": "CRWD", "MarketCap": 60, "Change": -0.62},
        {"Sector": "Technology", "Sub": "Hardware", "Ticker": "DELL", "MarketCap": 90, "Change": 0.88},
        {"Sector": "Technology", "Sub": "Hardware", "Ticker": "CSCO", "MarketCap": 200, "Change": 0.14},
        
        # CONSUMER CYCLICAL
        {"Sector": "Consumer Cyclical", "Sub": "E-Commerce", "Ticker": "AMZN", "MarketCap": 2000, "Change": 0.17},
        {"Sector": "Consumer Cyclical", "Sub": "Auto", "Ticker": "TSLA", "MarketCap": 1100, "Change": -0.14},
        {"Sector": "Consumer Cyclical", "Sub": "Retail", "Ticker": "HD", "MarketCap": 400, "Change": -0.05},
        {"Sector": "Consumer Cyclical", "Sub": "Retail", "Ticker": "LOW", "MarketCap": 140, "Change": -0.08},
        {"Sector": "Consumer Cyclical", "Sub": "Restaurants", "Ticker": "MCD", "MarketCap": 210, "Change": 0.31},
        {"Sector": "Consumer Cyclical", "Sub": "Restaurants", "Ticker": "SBUX", "MarketCap": 100, "Change": -0.20},
        
        # COMMUNICATION SERVICES
        {"Sector": "Communication Services", "Sub": "Internet", "Ticker": "GOOGL", "MarketCap": 2100, "Change": 0.08},
        {"Sector": "Communication Services", "Sub": "Internet", "Ticker": "META", "MarketCap": 1400, "Change": -0.06},
        {"Sector": "Communication Services", "Sub": "Media", "Ticker": "NFLX", "MarketCap": 300, "Change": -0.04},
        {"Sector": "Communication Services", "Sub": "Media", "Ticker": "DIS", "MarketCap": 180, "Change": 0.03},
        {"Sector": "Communication Services", "Sub": "Telecom", "Ticker": "VZ", "MarketCap": 170, "Change": 0.05},
        {"Sector": "Communication Services", "Sub": "Telecom", "Ticker": "T", "MarketCap": 140, "Change": 0.08},

        # HEALTHCARE
        {"Sector": "Healthcare", "Sub": "Pharma", "Ticker": "LLY", "MarketCap": 850, "Change": 0.43},
        {"Sector": "Healthcare", "Sub": "Pharma", "Ticker": "JNJ", "MarketCap": 390, "Change": 0.21},
        {"Sector": "Healthcare", "Sub": "Pharma", "Ticker": "ABBV", "MarketCap": 340, "Change": 0.60},
        {"Sector": "Healthcare", "Sub": "Pharma", "Ticker": "MRK", "MarketCap": 220, "Change": 0.43},
        {"Sector": "Healthcare", "Sub": "Pharma", "Ticker": "PFE", "MarketCap": 160, "Change": 0.18},
        {"Sector": "Healthcare", "Sub": "Managed", "Ticker": "UNH", "MarketCap": 500, "Change": 0.28},
        
        # FINANCIAL
        {"Sector": "Financial", "Sub": "Banks", "Ticker": "JPM", "MarketCap": 650, "Change": 0.00},
        {"Sector": "Financial", "Sub": "Banks", "Ticker": "BAC", "MarketCap": 310, "Change": 0.18},
        {"Sector": "Financial", "Sub": "Banks", "Ticker": "WFC", "MarketCap": 200, "Change": 0.30},
        {"Sector": "Financial", "Sub": "Banks", "Ticker": "C", "MarketCap": 120, "Change": 0.07},
        {"Sector": "Financial", "Sub": "Invest", "Ticker": "BRK-B", "MarketCap": 950, "Change": 0.02},
        {"Sector": "Financial", "Sub": "Credit", "Ticker": "V", "MarketCap": 560, "Change": 0.17},
        {"Sector": "Financial", "Sub": "Credit", "Ticker": "MA", "MarketCap": 440, "Change": 0.61},
        {"Sector": "Financial", "Sub": "Invest", "Ticker": "GS", "MarketCap": 160, "Change": 0.11},

        # INDUSTRIALS & ENERGY & DEFENSIVE
        {"Sector": "Industrials", "Sub": "Aero", "Ticker": "GE", "MarketCap": 200, "Change": 0.09},
        {"Sector": "Industrials", "Sub": "Aero", "Ticker": "RTX", "MarketCap": 160, "Change": 0.25},
        {"Sector": "Industrials", "Sub": "Aero", "Ticker": "CAT", "MarketCap": 170, "Change": 0.19},
        {"Sector": "Energy", "Sub": "Oil", "Ticker": "XOM", "MarketCap": 460, "Change": 0.15},
        {"Sector": "Energy", "Sub": "Oil", "Ticker": "CVX", "MarketCap": 280, "Change": 0.35},
        {"Sector": "Consumer Defensive", "Sub": "Discount", "Ticker": "WMT", "MarketCap": 600, "Change": -0.07},
        {"Sector": "Consumer Defensive", "Sub": "Discount", "Ticker": "COST", "MarketCap": 380, "Change": 0.04},
        {"Sector": "Consumer Defensive", "Sub": "Beverage", "Ticker": "KO", "MarketCap": 290, "Change": 0.29},
        {"Sector": "Consumer Defensive", "Sub": "Beverage", "Ticker": "PEP", "MarketCap": 230, "Change": 0.06},
        {"Sector": "Consumer Defensive", "Sub": "Household", "Ticker": "PG", "MarketCap": 390, "Change": -0.11},
    ])

    fig_full_heat = px.treemap(
        full_heat_data,
        path=["Sector", "Sub", "Ticker"],
        values="MarketCap",
        color="Change",
        color_continuous_scale=["#991b1b", "#1e293b", "#065f46", "#047857", "#00ff88"],
        color_continuous_midpoint=0,
        hover_data={"Change": ":.2f%"}
    )
    fig_full_heat.update_traces(
        textinfo="label+value",
        texttemplate="<b>%{label}</b><br>%{color:+.2f}%",
        textfont=dict(size=10, family="Segoe UI", color="#ffffff")
    )
    fig_full_heat.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0b0f17",
        height=380,
        margin=dict(l=2, r=2, t=2, b=2),
        coloraxis_showscale=False
    )
    st.plotly_chart(fig_full_heat, use_container_width=True)

# =========================================================
# [우측 3열] 방송 실시간 비디오 송출 + 라이브 채팅 & 슈퍼챗
# =========================================================
with col_right:
    st.markdown('<div class="panel-box" style="text-align:center;">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header">🔴 BROADCAST LIVE STREAM</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#000000; border:1px solid #334155; border-radius:6px; height:180px; display:flex; flex-direction:column; justify-content:center; align-items:center;">
        <div style="font-size:26px;">🔴 LIVE</div>
        <div style="color:#94a3b8; font-size:11px; margin-top:4px;">[캘리포니아 경박사 라이브 캠]</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header">💬 LIVE CHAT & SUPER CHAT</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="height:270px; overflow-y:auto; padding-right:4px;">
        <div style="background:#831843; border-left:3px solid #f43f5e; padding:5px 8px; border-radius:4px; font-size:11px; margin-bottom:5px; color:#fff;">
            <strong>서학개미1호</strong> $50.00 슈퍼챗<br>"경박사님 Finviz 애프터마켓 히트맵과 지수 브레스 조합 최고입니다!"
        </div>
        <div style="font-size:11px; margin-bottom:4px; color:#cbd5e1;"><strong style="color:#38bdf8;">캘리포니아팬:</strong> 반도체 쪽 NVDA, MU 약세 속 AVGO 방어가 눈에 띄네요.</div>
        <div style="font-size:11px; margin-bottom:4px; color:#cbd5e1;"><strong style="color:#38bdf8;">뉴욕트레이더:</strong> 실시간 전체 섹터 맵 한눈에 들어와서 너무 좋습니다.</div>
    </div>
    """, unsafe_allow_html=True)
    st.text_input("채팅 입력", placeholder="실시간 메시지 입력...", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
