SELECT *
FROM {{ ref('fact_table') }} f
JOIN {{ ref('dim_stock') }} s ON f.stock_id = s.id
JOIN {{ ref('dim_time') }} t ON f.time_id = t.id
ORDER BY t.date, s.symbol;