# scripts/run_report.py
import sqlite3
import pandas as pd
from pathlib import Path

# Path to DB
db_path = Path("ecom.db")

# Path to SQL file
sql_path = Path("queries/customer_spend_top_products.sql")

# Read SQL query from file
query = sql_path.read_text()

# Connect to the database and execute the query
conn = sqlite3.connect(db_path)
df = pd.read_sql_query(query, conn)
conn.close()

# Print first 20 rows so you can see the output
print(df.head(20).to_string(index=False))

# Also save the full report to a CSV file
df.to_csv("customer_spend_top_products_output.csv", index=False)
print("Saved: customer_spend_top_products_output.csv")
