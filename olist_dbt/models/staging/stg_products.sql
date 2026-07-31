select
    product_id,
    product_category_name
from {{ source('raw_dw', 'dim_products') }}