select
    order_id,
    product_id,
    seller_id,
    price,
    freight_value,
    total_paid
from {{ source('raw_dw', 'fact_order_items') }}