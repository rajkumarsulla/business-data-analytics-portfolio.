-- SQLite: import data/raw/sales.csv into a table named sales.
-- Total revenue, profit, and order count
SELECT ROUND(SUM(quantity * unit_price), 2) AS total_revenue,
       ROUND(SUM(quantity * (unit_price - unit_cost)), 2) AS total_profit,
       COUNT(DISTINCT order_id) AS total_orders
FROM sales;

-- Monthly revenue and profit
SELECT strftime('%Y-%m', order_date) AS sales_month,
       ROUND(SUM(quantity * unit_price), 2) AS revenue,
       ROUND(SUM(quantity * (unit_price - unit_cost)), 2) AS profit
FROM sales
GROUP BY strftime('%Y-%m', order_date)
ORDER BY sales_month;

-- Revenue by category
SELECT category, ROUND(SUM(quantity * unit_price), 2) AS revenue
FROM sales
GROUP BY category
ORDER BY revenue DESC;
