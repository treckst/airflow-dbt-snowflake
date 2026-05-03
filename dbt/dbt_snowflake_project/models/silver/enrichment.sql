
SELECT
    symbol,
    open::number(5, 2) AS open_price,
    close::number(5, 2) AS close_price,
    high::number(5, 2) AS high_price,
    low::number(5, 2) AS low_price,
    volume::number(10, 0) AS volume,
    {{ clean('name')}} as name,
    {{ fill_name('exchange_code','exchange') }}::varchar(9) as exchange_name,
    {{ fill_code('exchange_code','exchange') }}::varchar(4) as exchange_code,
    {{ fix_currency('price_currency')}}::varchar(3) as price_currency,
    date::date as trade_date

FROM
    {{ source('source', 'raw') }}
