-- queries/customer_spend_top_products.sql
WITH item_revenue AS (
  SELECT
    oi.order_id,
    o.customer_id,
    oi.product_id,
    p.name AS product_name,
    (oi.quantity * oi.unit_price) AS revenue
  FROM order_items oi
  JOIN orders o ON oi.order_id = o.order_id
  JOIN products p ON oi.product_id = p.product_id
),
customer_product_rev AS (
  SELECT
    customer_id,
    product_id,
    product_name,
    SUM(revenue) AS product_revenue
  FROM item_revenue
  GROUP BY customer_id, product_id
),
top_products_ranked AS (
  SELECT
    customer_id,
    product_name || ':' || printf('%.2f', product_revenue) AS prod_rev,
    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY product_revenue DESC) AS rn
  FROM customer_product_rev
),
top3 AS (
  SELECT customer_id,
    GROUP_CONCAT(prod_rev, ', ') AS top_products
  FROM top_products_ranked
  WHERE rn <= 3
  GROUP BY customer_id
)
SELECT
  c.customer_id,
  c.first_name || ' ' || c.last_name AS customer_name,
  c.email,
  COUNT(DISTINCT o.order_id) AS number_of_orders,
  printf('%.2f', COALESCE(SUM(o.total_amount),0.0)) AS total_spent,
  MAX(o.order_date) AS last_order_date,
  COALESCE(t.top_products, '') AS top_products
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
LEFT JOIN top3 t ON c.customer_id = t.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name, c.email, t.top_products
ORDER BY total_spent DESC
LIMIT 100;
