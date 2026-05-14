SELECT 
    name as stock_name,
    open_price,
    close_price,
    high_price,
    low_price,
    volume,
    date,
    AVG(close_price) OVER (PARTITION BY stock_name ORDER BY date ROWS BETWEEN 4 PRECEDING AND CURRENT ROW) AS moving_avg_5days_close,
    AVG(open_price) OVER (PARTITION BY stock_name ORDER BY date ROWS BETWEEN 4 PRECEDING AND CURRENT ROW) AS moving_avg_5days_open
FROM
    {{ ref('fact_table') }}
LEFT JOIN {{ ref('dim_time') }}
ON {{ ref('fact_table') }}.time_id = {{ ref('dim_time') }}.id
LEFT JOIN {{ ref('dim_stocks_final') }}
ON {{ ref('fact_table') }}.stock_id = {{ ref('dim_stocks_final') }}.id