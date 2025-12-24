SELECT * FROM stocks
LIMIT 10;

SELECT symbol,
       AVG(close) AS avg_close_price
FROM stocks
GROUP BY symbol
ORDER BY avg_close_price DESC;

SELECT sector,
       AVG((close - open) / open) AS avg_daily_return
FROM stocks
GROUP BY sector
ORDER BY avg_daily_return DESC;

SELECT symbol,
       AVG(volume) AS avg_volume
FROM stocks
GROUP BY symbol
ORDER BY avg_volume DESC
LIMIT 10;
