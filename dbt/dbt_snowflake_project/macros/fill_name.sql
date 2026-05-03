{% macro fill_name(column_name, column_code) %}
    CASE
        WHEN TRIM({{column_code}}) = 'XNAS' THEN COALESCE(TRIM({{column_name}}), 'NASDAQ')
        WHEN TRIM({{column_code}}) = 'ARCX' THEN COALESCE(TRIM({{column_name}}), 'NYSE ARCA')
        ELSE {{ column_code }}
    END
{% endmacro %}