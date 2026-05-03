{%macro fix_currency(column_name)%}
    CASE
        WHEN TRIM({{column_name}}) = 'USD' THEN {{column_name}}
        ELSE 'USD'
    END
{% endmacro %}