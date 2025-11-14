import random, datetime, csv
from pathlib import Path

random.seed(42)
data_dir = Path("data")
data_dir.mkdir(parents=True, exist_ok=True)

first_names = ["Liam","Olivia","Noah","Emma","Ava","Sophia","Isabella","Mia","Charlotte","Amelia","Lucas","Mason","Ethan","Logan","Jacob","Elijah","James","Benjamin","Sebastian","Jack","Harper","Evelyn","Abigail","Emily","Elizabeth","Sofia","Avery","Ella","Scarlett","Grace","Chloe","Victoria","Riley","Zoey","Nora"]
last_names = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Rodriguez","Martinez","Hernandez","Lopez","Gonzalez","Wilson","Anderson","Thomas","Taylor","Moore","Jackson","Martin","Lee","Perez","Thompson","White","Harris","Sanchez","Clark","Ramirez","Lewis","Robinson","Walker","Young","Allen","King","Wright"]
cities = ["Austin","Seattle","Denver","Chicago","Miami","Portland","Boston","Houston","Phoenix","Atlanta","San Diego","Dallas","San Jose","Orlando","Nashville"]
states = ["TX","WA","CO","IL","FL","OR","MA","TX","AZ","GA","CA","TX","CA","FL","TN"]

# Customers (30)
customers = []
for cid in range(1,31):
    fn = first_names[cid % len(first_names)]
    ln = last_names[(cid * 2) % len(last_names)]
    email = f"{fn.lower()}.{ln.lower()}{cid}@example.com"
    phone = f"+1-512-555-{cid:04d}"
    city = cities[cid % len(cities)]
    state = states[cid % len(states)]
    signup = (datetime.date(2022,1,1) + datetime.timedelta(days=cid*7)).isoformat()
    customers.append([cid, fn, ln, email, phone, city, state, signup])

# Products (30)
categories = ["Electronics","Home","Beauty","Fashion","Outdoors","Toys"]
products = []
for pid in range(1,31):
    name = f"Product {pid:03d}"
    category = categories[pid % len(categories)]
    price = round(random.uniform(15,250),2)
    stock = random.randint(20,200)
    created = (datetime.date(2023,1,1) + datetime.timedelta(days=pid*3)).isoformat()
    products.append([pid, name, category, f"{price:.2f}", stock, created])

# Orders (30)
orders = []
statuses = ["processing","shipped","delivered","cancelled"]
for oid in range(1,31):
    customer_id = (oid % 30) + 1
    order_date = (datetime.date(2024,1,5) + datetime.timedelta(days=oid*2)).isoformat()
    status = statuses[oid % len(statuses)]
    orders.append([oid, customer_id, order_date, status, 0.0])

# Order items (one item per order here)
order_items = []
order_item_id = 1
for oid in range(1,31):
    product_id = ((oid * 3) % 30) + 1
    quantity = (oid % 4) + 1
    unit_price = float(next(p[3] for p in products if p[0]==product_id))
    order_items.append([order_item_id, oid, product_id, quantity, f"{unit_price:.2f}"])
    orders[oid-1][4] = round(orders[oid-1][4] + quantity * unit_price,2)
    order_item_id += 1

# Reviews (30)
reviews = []
for rid in range(1,31):
    customer_id = ((rid * 2) % 30) + 1
    product_id = ((rid * 5) % 30) + 1
    rating = (rid % 5) + 1
    review_date = (datetime.date(2024,3,1) + datetime.timedelta(days=rid)).isoformat()
    title = f"Review {rid:03d}"
    reviews.append([rid, customer_id, product_id, rating, review_date, title])

def write_csv(path: Path, header, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        import csv
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
    print(f"Wrote {path} ({len(rows)} rows)")

write_csv(data_dir / "customers.csv",
          ["customer_id","first_name","last_name","email","phone","city","state","signup_date"],
          customers)

write_csv(data_dir / "products.csv",
          ["product_id","name","category","price","stock","created_at"],
          products)

write_csv(data_dir / "orders.csv",
          ["order_id","customer_id","order_date","status","total_amount"],
          orders)

write_csv(data_dir / "order_items.csv",
          ["order_item_id","order_id","product_id","quantity","unit_price"],
          order_items)

write_csv(data_dir / "reviews.csv",
          ["review_id","customer_id","product_id","rating","review_date","title"],
          reviews)

print("All CSVs created in the data/ folder.")
