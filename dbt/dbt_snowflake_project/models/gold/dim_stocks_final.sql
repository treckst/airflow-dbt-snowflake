SELECT 
    *,
    (dbt_valid_to = to_date('9999-12-31')) AS is_valid
FROM
    {{ ref('golden_items') }}

