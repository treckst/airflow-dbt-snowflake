{% macro clean(column_name) %}
    UPPER(
        REPLACE(
            SPLIT_PART(  
                {{column_name}}, ' ', 1), 
        '.com', '')
    )
{% endmacro %}