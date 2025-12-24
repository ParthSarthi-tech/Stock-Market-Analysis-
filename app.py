import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# PAGE CONFIG
st.set_page_config(
    page_title="Indian Stock Market Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)
# ENHANCED CUSTOM CSS

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.main {
    background: linear-gradient(135deg, #0a0e27 0%, #1a1d35 100%);
}

.stApp {
    background: linear-gradient(135deg, #0a0e27 0%, #1a1d35 100%);
}

/* Header Styling */
h1 {
    background: linear-gradient(120deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
    font-size: 3rem !important;
    margin-bottom: 0.5rem !important;
}

h2 {
    color: #e0e7ff;
    font-weight: 600;
    font-size: 1.5rem !important;
    margin-top: 2rem !important;
    margin-bottom: 1rem !important;
}

h3 {
    color: #c7d2fe;
    font-weight: 600;
}

/* Metric Cards */
.metric-card {
    background: linear-gradient(135deg, #1e2139 0%, #252a48 100%);
    padding: 24px;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(102, 126, 234, 0.2);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
}

.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 48px rgba(102, 126, 234, 0.2);
}

.metric-label {
    font-size: 13px;
    color: #9ca3af;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600;
    margin-bottom: 8px;
}

.metric-value {
    font-size: 32px;
    font-weight: 800;
    background: linear-gradient(120deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 8px 0;
}

.metric-subtitle {
    font-size: 16px;
    color: #d1d5db;
    font-weight: 500;
}

/* Sidebar Styling */
.css-1d391kg, [data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1d35 0%, #0f1220 100%);
    border-right: 1px solid rgba(102, 126, 234, 0.1);
}

.css-1d391kg h2, [data-testid="stSidebar"] h2 {
    color: #e0e7ff !important;
    font-size: 1.2rem !important;
}

/* Section Headers */
.section-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 40px 0 20px 0;
    padding-bottom: 12px;
    border-bottom: 2px solid rgba(102, 126, 234, 0.3);
}

.section-icon {
    font-size: 28px;
}

.section-title {
    font-size: 24px;
    font-weight: 700;
    color: #e0e7ff;
    margin: 0;
}

/* Info Banner */
.info-banner {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
    border-left: 4px solid #667eea;
    padding: 16px 20px;
    border-radius: 8px;
    margin: 20px 0;
    color: #c7d2fe;
    font-size: 15px;
}

/* Download Button */
.stDownloadButton button {
    background: linear-gradient(120deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 12px 32px;
    font-weight: 600;
    border-radius: 8px;
    transition: all 0.3s ease;
}

.stDownloadButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
}

/* Footer */
.footer {
    text-align: center;
    padding: 40px 20px;
    margin-top: 60px;
    border-top: 1px solid rgba(102, 126, 234, 0.2);
    color: #9ca3af;
}

.footer-tech {
    font-size: 14px;
    font-weight: 500;
    color: #667eea;
}

/* Selectbox */
.stSelectbox > div > div {
    background: #1e2139;
    border: 1px solid rgba(102, 126, 234, 0.2);
    color: #e0e7ff;
}

/* Multiselect */
.stMultiSelect > div > div {
    background: #1e2139;
    border: 1px solid rgba(102, 126, 234, 0.2);
}
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("""
<div style="text-align: center; margin-bottom: 30px;">
    <h1>📈 Indian Stock Market Analytics</h1>
    <p style="font-size: 18px; color: #9ca3af; margin-top: -10px;">
        Advanced data-driven financial analytics focusing on <strong style="color: #667eea;">risk</strong>, 
        <strong style="color: #667eea;">return</strong>, and 
        <strong style="color: #667eea;">sector performance</strong>
    </p>
</div>
""", unsafe_allow_html=True)

# LOAD DATA

@st.cache_data
def load_data():
    conn = sqlite3.connect("market.db")
    df = pd.read_sql("""
    SELECT date, open, close, symbol, sector
    FROM stocks
    """, conn)
    conn.close()
    
    df["date"] = pd.to_datetime(df["date"])
    df["daily_return"] = ((df["close"] - df["open"]) / df["open"]) * 100
    df = df.dropna()
    
    return df

df = load_data()
df_full = df.copy()

# SIDEBAR FILTERS

with st.sidebar:
    st.markdown("### 🎯 Analysis Controls")
    st.markdown("---")
    
    window = st.selectbox(
        "📅 Time Window",
        ["30 Days", "90 Days", "Full Period"],
        help="Select the time period for analysis"
    )
    
    st.markdown("---")

latest_date = df["date"].max()

df_filtered = df.copy()

if window == "30 Days":
    df_filtered = df_filtered[df_filtered["date"] >= latest_date - pd.Timedelta(days=30)]
elif window == "90 Days":
    df_filtered = df_filtered[df_filtered["date"] >= latest_date - pd.Timedelta(days=90)]

# AGGREGATE METRICS
metrics = df_filtered.groupby(["symbol", "sector"]).agg(
    avg_return=("daily_return", "mean"),
    volatility=("daily_return", "std")
).reset_index()

metrics["risk_adjusted_return"] = metrics["avg_return"] / metrics["volatility"]
metrics = metrics.round(2)

# Sector filter
with st.sidebar:
    selected_sectors = st.multiselect(
        "🏭 Filter by Sectors",
        options=sorted(metrics["sector"].unique()),
        default=metrics["sector"].unique(),
        help="Select one or more sectors to analyze"
    )
    
    st.markdown("---")
    st.markdown(f"""
    <div style="background: rgba(102, 126, 234, 0.1); padding: 12px; border-radius: 8px; font-size: 13px;">
        <strong style="color: #667eea;">📊 Data Overview</strong><br/>
        <span style="color: #9ca3af;">
        Stocks: {len(metrics)}<br/>
        Sectors: {len(metrics['sector'].unique())}<br/>
        Period: {window}
        </span>
    </div>
    """, unsafe_allow_html=True)

filtered = metrics[metrics["sector"].isin(selected_sectors)]

# KPI METRICS

st.markdown("## 🎯 Key Performance Indicators")

if len(filtered) > 0:
    best_stock = filtered.sort_values("avg_return", ascending=False).iloc[0]
    best_risk_adj = filtered.sort_values("risk_adjusted_return", ascending=False).iloc[0]
    most_volatile = filtered.sort_values("volatility", ascending=False).iloc[0]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">🏆 Best Average Return</div>
            <div class="metric-value">{best_stock['symbol']}</div>
            <div class="metric-subtitle">{best_stock['avg_return']:+.2f}% daily</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">⚖️ Best Risk-Adjusted</div>
            <div class="metric-value">{best_risk_adj['symbol']}</div>
            <div class="metric-subtitle">{best_risk_adj['risk_adjusted_return']:.2f} ratio</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">📊 Most Volatile</div>
            <div class="metric-value">{most_volatile['symbol']}</div>
            <div class="metric-subtitle">{most_volatile['volatility']:.2f}% std dev</div>
        </div>
        """, unsafe_allow_html=True)

# RISK VS RETURN
st.markdown("## 📊 Risk vs Return Analysis")
st.markdown('<div class="info-banner">💡 Ideal stocks are in the <strong>top-left quadrant</strong> (high return, low risk)</div>', unsafe_allow_html=True)

fig1 = px.scatter(
    filtered,
    x="volatility",
    y="avg_return",
    color="sector",
    text="symbol",
    labels={
        "volatility": "Risk (Volatility %)",
        "avg_return": "Average Daily Return (%)"
    },
    color_discrete_sequence=px.colors.qualitative.Bold
)

fig1.update_traces(
    textposition="top center",
    marker=dict(size=12, line=dict(width=2, color='white'))
)

fig1.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#e0e7ff'),
    xaxis=dict(gridcolor='rgba(102, 126, 234, 0.1)', zeroline=False),
    yaxis=dict(gridcolor='rgba(102, 126, 234, 0.1)', zeroline=True, zerolinecolor='rgba(102, 126, 234, 0.3)'),
    height=500,
    hovermode='closest'
)

st.plotly_chart(fig1, use_container_width=True)

# TWO COLUMN LAYOUT
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("## 🏭 Sector Performance")
    
    sector_df = filtered.groupby("sector")["avg_return"].mean().reset_index()
    sector_df = sector_df.sort_values("avg_return", ascending=True)
    
    fig2 = px.bar(
        sector_df,
        y="sector",
        x="avg_return",
        orientation='h',
        labels={"avg_return": "Avg Daily Return (%)", "sector": ""},
        color="avg_return",
        color_continuous_scale=["#ef4444", "#fbbf24", "#10b981"]
    )
    
    fig2.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e0e7ff'),
        xaxis=dict(gridcolor='rgba(102, 126, 234, 0.1)'),
        yaxis=dict(gridcolor='rgba(0,0,0,0)'),
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig2, use_container_width=True)

with col_right:
    st.markdown("## ⚖️ Risk-Adjusted Returns")
    
    top_stocks = filtered.sort_values("risk_adjusted_return", ascending=False).head(10)
    
    fig3 = px.bar(
        top_stocks,
        x="symbol",
        y="risk_adjusted_return",
        color="sector",
        labels={"risk_adjusted_return": "Return per Unit Risk", "symbol": ""},
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    
    fig3.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e0e7ff'),
        xaxis=dict(gridcolor='rgba(0,0,0,0)'),
        yaxis=dict(gridcolor='rgba(102, 126, 234, 0.1)'),
        height=400
    )
    
    st.plotly_chart(fig3, use_container_width=True)

# ROLLING TREND

st.markdown("## 📈 Rolling Return Trend Analysis")

stock_choice = st.selectbox(
    "Select Stock for Detailed Analysis",
    sorted(df_full["symbol"].unique()),
    help="View 30-day rolling average returns"
)

stock_df = df_full[df_full["symbol"] == stock_choice].copy()
stock_df["rolling_return"] = stock_df["daily_return"].rolling(window=30, min_periods=5).mean()

fig4 = go.Figure()

fig4.add_trace(go.Scatter(
    x=stock_df["date"],
    y=stock_df["rolling_return"],
    mode='lines',
    name='30-Day Rolling Return',
    line=dict(color='#667eea', width=3),
    fill='tozeroy',
    fillcolor='rgba(102, 126, 234, 0.1)'
))

fig4.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#e0e7ff'),
    xaxis=dict(gridcolor='rgba(102, 126, 234, 0.1)', title='Date'),
    yaxis=dict(gridcolor='rgba(102, 126, 234, 0.1)', title='30-Day Rolling Return (%)'),
    height=400,
    hovermode='x unified'
)

st.plotly_chart(fig4, use_container_width=True)

# DATA TABLE

st.markdown("## 📋 Detailed Stock Metrics")

display_df = filtered[["symbol", "sector", "avg_return", "volatility", "risk_adjusted_return"]].sort_values("avg_return", ascending=False)
display_df.columns = ["Symbol", "Sector", "Avg Return (%)", "Volatility (%)", "Risk-Adjusted Return"]

st.dataframe(
    display_df,
    use_container_width=True,
    height=400
)

# EXPORT FEATURE

st.markdown("## 📥 Export Analysis")

csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Stock Metrics (CSV)",
    data=csv,
    file_name=f"stock_analysis_{window.replace(' ', '_').lower()}.csv",
    mime="text/csv"
)

# FOOTER

st.markdown("""
<div class="footer">
    <div class="footer-tech">
        🛠️ Tech Stack: Python • SQLite • Plotly • Streamlit
    </div>
    <div style="margin-top: 8px; font-size: 13px;">
        Built for Financial & Data Analytics
    </div>
</div>
""", unsafe_allow_html=True)