{% macro fill_code(column_name, column_code) %}
    CASE
        WHEN TRIM({{ column_code }}) = 'XNAS' OR TRIM({{ column_name }}) = 'NASDAQ' THEN 'XNAS'
        WHEN TRIM({{ column_code }}) = 'ARCX' OR TRIM({{ column_name }}) = 'NYSE ARCA' THEN 'ARCX'
        ELSE {{ column_code }}
    END
{% endmacro %}