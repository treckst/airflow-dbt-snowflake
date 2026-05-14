SELECT
    {{ dbt_utils.generate_surrogate_key(['symbol']) }} AS id,
    symbol,
    name,
    exchange_name, 
    exchange_code,
    price_currency
FROM
    {{ ref('enrichment') }}
QUALIFY ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY trade_date DESC) = 1