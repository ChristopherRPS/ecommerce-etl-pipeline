import pandas as pd

# Cargar datos crudos
orders = pd.read_csv("data/raw/olist_orders_dataset.csv")
customers = pd.read_csv("data/raw/olist_customers_dataset.csv")
order_items = pd.read_csv("data/raw/olist_order_items_dataset.csv")
products = pd.read_csv("data/raw/olist_products_dataset.csv")
payments = pd.read_csv("data/raw/olist_order_payments_dataset.csv")

# Convertir columnas de fecha (estaban como texto) a tipo datetime real
date_cols = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]
for col in date_cols:
    orders[col] = pd.to_datetime(orders[col])

    dim_orders = orders[[
    "order_id", "customer_id", "order_status",
    "order_purchase_timestamp", "order_delivered_customer_date",
    "order_estimated_delivery_date"
]].copy()

# Métrica útil: días que tardó en entregarse (NaT si aún no se entregó)
dim_orders["delivery_days"] = (
    dim_orders["order_delivered_customer_date"] - dim_orders["order_purchase_timestamp"]
).dt.days

dim_customers = customers.copy()

dim_products = products[["product_id", "product_category_name"]].copy()
dim_products["product_category_name"] = dim_products["product_category_name"].fillna("unknown")

# Agregamos el total pagado por pedido (puede haber varios pagos por order_id)
payments_agg = payments.groupby("order_id")["payment_value"].sum().reset_index()
payments_agg = payments_agg.rename(columns={"payment_value": "total_paid"})

fact_order_items = order_items[[
    "order_id", "product_id", "seller_id", "price", "freight_value"
]].copy()

# Unimos con el total pagado del pedido
fact_order_items = fact_order_items.merge(payments_agg, on="order_id", how="left")

dim_orders.to_csv("data/processed/dim_orders.csv", index=False)
dim_customers.to_csv("data/processed/dim_customers.csv", index=False)
dim_products.to_csv("data/processed/dim_products.csv", index=False)
fact_order_items.to_csv("data/processed/fact_order_items.csv", index=False)

print("✅ Transformación completa. Archivos guardados en data/processed/")
print("dim_orders:", dim_orders.shape)
print("dim_customers:", dim_customers.shape)
print("dim_products:", dim_products.shape)
print("fact_order_items:", fact_order_items.shape)