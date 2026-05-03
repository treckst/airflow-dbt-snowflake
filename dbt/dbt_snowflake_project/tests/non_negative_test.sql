SELECT
    *
FROM
    {{ ref('fact_table') }}
WHERE
    open_price < 0
    OR close_price < 0
    OR high_price < 0
    OR low_price < 0
    OR volume < 0