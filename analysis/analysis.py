import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("market.db")

# Load stock data
df = pd.read_sql("""
SELECT date, close, symbol, sector
FROM stocks
ORDER BY symbol, date
""", conn)

conn.close()

# Convert date
df["date"] = pd.to_datetime(df["date"])

# Calculate daily return (%) per stock
df["daily_return"] = (
    df.groupby("symbol")["close"]
    .pct_change() * 100
)

# Drop first rows with NaN return
df = df.dropna()

# Sector-level metrics
sector_metrics = df.groupby("sector").agg(
    avg_return=("daily_return", "mean"),
    volatility=("daily_return", "std")
).reset_index()
# Round values for readability
sector_metrics["avg_return"] = sector_metrics["avg_return"].round(2)
sector_metrics["volatility"] = sector_metrics["volatility"].round(2)


print("\nSector Metrics:")
print(sector_metrics)
