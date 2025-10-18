import os
from datetime import date
import pandas as pd
import matplotlib.pyplot as plt
import psycopg2

# ---------- DB CONNECTION ----------
CONN = psycopg2.connect(
    host="localhost",
    database="sales_report",   # <- your DB name from pgAdmin
    user="postgres",           # <- your PG user
    password="Xabuba2007"   # <- your PG password
)

# ---------- QUERIES ----------
SQL_DAILY = """
SELECT o.order_date,
       SUM(oi.quantity * oi.unit_price) AS revenue
FROM orders o
JOIN order_items oi USING(order_id)
WHERE o.status = 'paid'
GROUP BY o.order_date
ORDER BY o.order_date;
"""

SQL_BY_CAT = """
SELECT p.category,
       SUM(oi.quantity * oi.unit_price) AS revenue
FROM orders o
JOIN order_items oi USING(order_id)
JOIN products p USING(product_id)
WHERE o.status = 'paid'
GROUP BY p.category
ORDER BY revenue DESC;
"""

SQL_TOP = """
SELECT p.product_name,
       SUM(oi.quantity) AS qty,
       SUM(oi.quantity * oi.unit_price) AS revenue
FROM orders o
JOIN order_items oi USING(order_id)
JOIN products p USING(product_id)
WHERE o.status = 'paid'
GROUP BY p.product_name
ORDER BY revenue DESC
LIMIT 5;
"""

SQL_BY_REGION = """
SELECT c.region,
       SUM(oi.quantity * oi.unit_price) AS revenue
FROM orders o
JOIN order_items oi USING(order_id)
JOIN customers c USING(customer_id)
WHERE o.status = 'paid'
GROUP BY c.region
ORDER BY revenue DESC;
"""

SQL_REFUND = """
SELECT
  SUM(CASE WHEN status='refunded' THEN 1 ELSE 0 END)::decimal
  / NULLIF(COUNT(*),0) AS refund_rate
FROM orders;
"""

# ---------- RUN QUERIES ----------
daily   = pd.read_sql(SQL_DAILY, CONN)
by_cat  = pd.read_sql(SQL_BY_CAT, CONN)
topprod = pd.read_sql(SQL_TOP, CONN)
by_reg  = pd.read_sql(SQL_BY_REGION, CONN)
ref_rate= float(pd.read_sql(SQL_REFUND, CONN).iloc[0,0] or 0.0)

CONN.close()

# ---------- OUTPUT FOLDER ----------
out_dir = os.path.join(os.path.dirname(__file__), "..", "output")
os.makedirs(out_dir, exist_ok=True)

# ---------- CHARTS ----------
# 1) Daily revenue
if not daily.empty:
    daily.plot(x="order_date", y="revenue", kind="line", marker="o")
    plt.title("Daily Revenue")
    plt.xlabel("Date"); plt.ylabel("Revenue")
    plt.tight_layout(); plt.savefig(os.path.join(out_dir, "daily_revenue.png")); plt.clf()

# 2) Revenue by category
if not by_cat.empty:
    by_cat.plot(x="category", y="revenue", kind="bar")
    plt.title("Revenue by Category")
    plt.xlabel("Category"); plt.ylabel("Revenue")
    plt.tight_layout(); plt.savefig(os.path.join(out_dir, "revenue_by_category.png")); plt.clf()

# 3) Top products by revenue
if not topprod.empty:
    topprod.plot(x="product_name", y="revenue", kind="bar")
    plt.title("Top Products by Revenue")
    plt.xlabel("Product"); plt.ylabel("Revenue")
    plt.tight_layout(); plt.savefig(os.path.join(out_dir, "top_products.png")); plt.clf()

# 4) Revenue by region
if not by_reg.empty:
    by_reg.plot(x="region", y="revenue", kind="bar")
    plt.title("Revenue by Region")
    plt.xlabel("Region"); plt.ylabel("Revenue")
    plt.tight_layout(); plt.savefig(os.path.join(out_dir, "revenue_by_region.png")); plt.clf()

# ---------- EXCEL REPORT ----------
excel_path = os.path.join(out_dir, f"sales_report_{date.today()}.xlsx")
with pd.ExcelWriter(excel_path) as xls:
    daily.to_excel(xls,      sheet_name="DailyRevenue", index=False)
    by_cat.to_excel(xls,     sheet_name="ByCategory",   index=False)
    topprod.to_excel(xls,    sheet_name="TopProducts",  index=False)
    by_reg.to_excel(xls,     sheet_name="ByRegion",     index=False)
    pd.DataFrame({"refund_rate":[round(ref_rate,4)]}).to_excel(xls, sheet_name="KPIs", index=False)

print(f"Report ready: {excel_path}")
print(f"Refund rate: {round(ref_rate*100,2)}%")
