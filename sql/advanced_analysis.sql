SELECT date,
       symbol,
       (close - open) / open AS daily_return
FROM stocks;

SELECT symbol,
       AVG((close - open) / open) AS avg_return,
       SQRT(AVG(((close - open) / open) * ((close - open) / open))) AS volatility
FROM stocks
GROUP BY symbol
ORDER BY volatility DESC;

SELECT sector,
       symbol,
       AVG((close - open) / open) AS avg_return,
       RANK() OVER (
           PARTITION BY sector
           ORDER BY AVG((close - open) / open) DESC
       ) AS sector_rank
FROM stocks
GROUP BY sector, symbol;

SELECT
    CASE
        WHEN close > open THEN 'Bull Day'
        ELSE 'Bear Day'
    END AS market_type,
    COUNT(*) AS days
FROM stocks
GROUP BY market_type;

