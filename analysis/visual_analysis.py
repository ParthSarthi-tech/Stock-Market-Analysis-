import sqlite3
import pandas as pd
import plotly.express as px

conn = sqlite3.connect("market.db")

df = pd.read_sql("""
SELECT date, open, close, symbol, sector
FROM stocks
""", conn)

conn.close()

df["date"] = pd.to_datetime(df["date"])

# Daily return in %
df["daily_return"] = ((df["close"] - df["open"]) / df["open"]) * 100

df = df.dropna()

# Aggregate
metrics = df.groupby(["symbol", "sector"]).agg(
    avg_return=("daily_return", "mean"),
    volatility=("daily_return", "std")
).reset_index()

# Risk-adjusted return 
metrics["risk_adjusted_return"] = (
    metrics["avg_return"] / metrics["volatility"]
).round(2)

#  ROUND FOR READABILITY
metrics["avg_return"] = metrics["avg_return"].round(2)
metrics["volatility"] = metrics["volatility"].round(2)

# Scatter
fig = px.scatter(
    metrics,
    x="volatility",
    y="avg_return",
    color="sector",
    text="symbol",
    title="Risk vs Return Analysis by Sector (Indian Stocks)",
    labels={
        "avg_return": "Average Daily Return (%)",
        "volatility": "Risk (Volatility %)"
    }
)

fig.update_traces(textposition="top center")
fig.show()

# Bar chart
sector_df = metrics.groupby("sector")["avg_return"].mean().reset_index()

fig2 = px.bar(
    sector_df,
    x="sector",
    y="avg_return",
    title="Average Return by Sector",
    labels={"avg_return": "Average Daily Return (%)"}
)

fig2.show()

fig3 = px.bar(
    metrics.sort_values("risk_adjusted_return", ascending=False),
    x="symbol",
    y="risk_adjusted_return",
    color="sector",
    title="Risk-Adjusted Return by Stock",
    labels={"risk_adjusted_return": "Return per Unit Risk"}
)

fig3.show()

# Rolling return trend for one stock (example: RELIANCE)
stock = "RELIANCE"

stock_df = df[df["symbol"] == stock].copy()
stock_df["rolling_return"] = stock_df["daily_return"].rolling(30).mean()

fig4 = px.line(
    stock_df,
    x="date",
    y="rolling_return",
    title=f"30-Day Rolling Average Return – {stock}",
    labels={"rolling_return": "Return (%)"}
)

fig4.show()
