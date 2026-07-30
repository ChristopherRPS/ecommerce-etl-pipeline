import pandas as pd

# Cargar las tablas principales
orders = pd.read_csv("data/raw/olist_orders_dataset.csv")
customers = pd.read_csv("data/raw/olist_customers_dataset.csv")
order_items = pd.read_csv("data/raw/olist_order_items_dataset.csv")
products = pd.read_csv("data/raw/olist_products_dataset.csv")
payments = pd.read_csv("data/raw/olist_order_payments_dataset.csv")

# Vistazo general
print("ORDERS:")
print(orders.shape)
print(orders.head())
print(orders.info())

print("\nCUSTOMERS:")
print(customers.shape)
print(customers.head())

print("\nORDER_ITEMS:")
print(order_items.shape)
print(order_items.head())

print("\nPRODUCTS:")
print(products.shape)
print(products.head())

print("\nPAYMENTS:")
print(payments.shape)
print(payments.head())