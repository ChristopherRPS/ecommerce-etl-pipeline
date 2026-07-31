select
    order_id,
    customer_id,
    order_status,
    order_purchase_timestamp::timestamp as order_purchase_timestamp,
    order_delivered_customer_date::timestamp as order_delivered_customer_date,
    order_estimated_delivery_date::timestamp as order_estimated_delivery_date,
    delivery_days
from {{ source('raw_dw', 'dim_orders') }}