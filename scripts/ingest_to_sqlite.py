# scripts/ingest_to_sqlite.py
import pandas as pd
import sqlite3
from pathlib import Path

project_root = Path(".")
data_dir = project_root / "data"
db_path = project_root / "ecom.db"

# Read CSVs (will raise a clear error if a file is missing)
customers = pd.read_csv(data_dir / "customers.csv")
products = pd.read_csv(data_dir / "products.csv")
orders = pd.read_csv(data_dir / "orders.csv")
order_items = pd.read_csv(data_dir / "order_items.csv")
reviews = pd.read_csv(data_dir / "reviews.csv")

# Connect to SQLite
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Create tables with basic schema and FKs
cur.executescript("""
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS customers (
  customer_id INTEGER PRIMARY KEY,
  first_name TEXT,
  last_name TEXT,
  email TEXT,
  phone TEXT,
  city TEXT,
  state TEXT,
  signup_date TEXT
);

CREATE TABLE IF NOT EXISTS products (
  product_id INTEGER PRIMARY KEY,
  name TEXT,
  category TEXT,
  price REAL,
  stock INTEGER,
  created_at TEXT
);

CREATE TABLE IF NOT EXISTS orders (
  order_id INTEGER PRIMARY KEY,
  customer_id INTEGER,
  order_date TEXT,
  status TEXT,
  total_amount REAL,
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE IF NOT EXISTS order_items (
  order_item_id INTEGER PRIMARY KEY,
  order_id INTEGER,
  product_id INTEGER,
  quantity INTEGER,
  unit_price REAL,
  FOREIGN KEY (order_id) REFERENCES orders(order_id),
  FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE IF NOT EXISTS reviews (
  review_id INTEGER PRIMARY KEY,
  customer_id INTEGER,
  product_id INTEGER,
  rating INTEGER,
  review_date TEXT,
  title TEXT,
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
  FOREIGN KEY (product_id) REFERENCES products(product_id)
);
""")
conn.commit()

# Write dataframes to the DB (replace existing tables)
customers.to_sql("customers", conn, if_exists="replace", index=False)
products.to_sql("products", conn, if_exists="replace", index=False)
orders.to_sql("orders", conn, if_exists="replace", index=False)
order_items.to_sql("order_items", conn, if_exists="replace", index=False)
reviews.to_sql("reviews", conn, if_exists="replace", index=False)

# Re-enable FK constraint at runtime and create helpful indexes
cur.execute("PRAGMA foreign_keys = ON;")
cur.executescript("""
CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_orderitems_order ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_orderitems_product ON order_items(product_id);
CREATE INDEX IF NOT EXISTS idx_reviews_product ON reviews(product_id);
""")
conn.commit()

# Print counts for verification
for tbl in ["customers","products","orders","order_items","reviews"]:
    count = cur.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]
    print(f"{tbl}: {count} rows")

conn.close()
print(f"Database written to: {db_path.resolve()}")
