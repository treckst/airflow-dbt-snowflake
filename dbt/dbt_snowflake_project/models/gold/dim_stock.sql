SELECT
    {{ dbt_utils.generate_surrogate_key(['symbol']) }} AS id,
    symbol,
    name,
    exchange_name, 
    exchange_code,
    price_currency,
    AVG(open_price) OVER(PARTITION BY symbol RANGE BETWEEN UNBOUNDED PRECEDING 4 AND CURRENT ROW) AS avg_open_price
FROM
    {{ ref('enrichment') }}
QUALIFY ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY trade_date DESC) = 1