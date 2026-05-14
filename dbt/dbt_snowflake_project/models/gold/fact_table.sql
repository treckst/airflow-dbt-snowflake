-- depends_on: {{ ref('dim_time') }}
SELECT
    {{ dbt_utils.generate_surrogate_key(['symbol','trade_date']) }} AS id,
    {{ dbt_utils.generate_surrogate_key(['symbol']) }} AS stock_id,
    {{ dbt_utils.generate_surrogate_key(['trade_date']) }} AS time_id,
    open_price,
    close_price,
    high_price,
    low_price,
    volume
FROM
    {{ ref('enrichment') }}
{% if is_incremental() %}
WHERE
    trade_date > (
        SELECT COALESCE(MAX(dim.date), '1900-01-01'::DATE)
    FROM {{ this }} as fact
    INNER JOIN {{ ref('dim_time') }} as dim
    ON fact.time_id = dim.id
    )
{% endif %}