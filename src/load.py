import pandas as pd
from sqlalchemy import create_engine

# Conexión a Postgres (mismos datos que pusimos en docker-compose.yml)
engine = create_engine("postgresql+psycopg2://etl_user:etl_pass@postgres:5432/ecommerce_dw")

# Cargar los CSVs procesados
dim_orders = pd.read_csv("data/processed/dim_orders.csv")
dim_customers = pd.read_csv("data/processed/dim_customers.csv")
dim_products = pd.read_csv("data/processed/dim_products.csv")
fact_order_items = pd.read_csv("data/processed/fact_order_items.csv")

# Cargar cada tabla a Postgres
# if_exists="replace" recrea la tabla cada vez que corres el script (útil mientras desarrollas)
dim_customers.to_sql("dim_customers", engine, if_exists="replace", index=False)
dim_products.to_sql("dim_products", engine, if_exists="replace", index=False)
dim_orders.to_sql("dim_orders", engine, if_exists="replace", index=False)
fact_order_items.to_sql("fact_order_items", engine, if_exists="replace", index=False)

print("✅ Datos cargados en PostgreSQL")