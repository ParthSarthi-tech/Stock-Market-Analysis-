import sqlite3

# Connect to database
conn = sqlite3.connect("market.db")
cursor = conn.cursor()

sector_map = {
    "HDFCBANK": "Banking",
    "ICICIBANK": "Banking",
    "SBIN": "Banking",

    "INFY": "IT",
    "TCS": "IT",

    "HINDUNILVR": "FMCG",
    "ITC": "FMCG",

    "RELIANCE": "Energy"
}

for symbol, sector in sector_map.items():
    cursor.execute("""
        UPDATE stocks
        SET sector = ?
        WHERE symbol = ?
    """, (sector, symbol))

conn.commit()
conn.close()

print("✅ Sectors updated successfully")
