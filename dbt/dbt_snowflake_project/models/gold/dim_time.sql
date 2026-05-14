SELECT
    DISTINCT {{ dbt_utils.generate_surrogate_key(['trade_date']) }} AS id,
    trade_date as date,
    EXTRACT(month FROM trade_date) AS month,
    EXTRACT(quarter FROM trade_date) AS quarter,
    EXTRACT(year FROM trade_date) AS year
FROM
    {{ ref('enrichment') }}
{% if is_incremental() %}
WHERE
    trade_date > (
        SELECT COALESCE(MAX(date), '1900-01-01'::DATE)
        FROM {{ this }}
    )
{% endif %}