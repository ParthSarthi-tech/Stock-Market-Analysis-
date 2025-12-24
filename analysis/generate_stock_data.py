import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

np.random.seed(42)

stocks = {
    "RELIANCE": 2500,
    "TCS": 3800,
    "INFY": 1600,
    "HDFCBANK": 1500,
    "ICICIBANK": 950,
    "ITC": 450,
    "HINDUNILVR": 2600,
    "SBIN": 600
}

start_date = datetime(2021, 1, 1)
days = 750  # ~3 years of trading days

os.makedirs("../data", exist_ok=True)

for stock, base_price in stocks.items():
    dates = []
    open_prices = []
    high_prices = []
    low_prices = []
    close_prices = []
    volumes = []

    price = base_price

    for i in range(days):
        date = start_date + timedelta(days=i)

        if date.weekday() >= 5:  # skip weekends
            continue

        daily_change = np.random.normal(0, 0.015)
        open_price = price
        close_price = price * (1 + daily_change)

        high_price = max(open_price, close_price) * (1 + np.random.uniform(0.001, 0.01))
        low_price = min(open_price, close_price) * (1 - np.random.uniform(0.001, 0.01))

        volume = np.random.randint(1_000_000, 10_000_000)

        dates.append(date.strftime("%Y-%m-%d"))
        open_prices.append(round(open_price, 2))
        high_prices.append(round(high_price, 2))
        low_prices.append(round(low_price, 2))
        close_prices.append(round(close_price, 2))
        volumes.append(volume)

        price = close_price

    df = pd.DataFrame({
        "Date": dates,
        "Open": open_prices,
        "High": high_prices,
        "Low": low_prices,
        "Close": close_prices,
        "Volume": volumes
    })

    df.to_csv(f"../data/{stock}.csv", index=False)

print("✅ Stock CSV files generated successfully.")
