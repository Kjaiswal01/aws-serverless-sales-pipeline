CREATE EXTERNAL TABLE IF NOT EXISTS sales_analytics_db.processed (
  order_id INT,
  order_date STRING,
  product STRING,
  category STRING,
  quantity INT,
  price DOUBLE,
  customer_id STRING,
  city STRING,
  total_amount DOUBLE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION 's3://cloud-sales-datalake-kshitij-2026/processed/'
TBLPROPERTIES ('skip.header.line.count'='1');


SELECT 
    city,
    COUNT(order_id) AS total_orders,
    SUM(quantity) AS total_units_sold,
    SUM(total_amount) AS total_revenue
FROM sales_analytics_db.processed
GROUP BY city
ORDER BY total_revenue DESC;


SELECT 
    category,
    COUNT(order_id) AS total_orders,
    SUM(total_amount) AS category_revenue,
    ROUND(AVG(total_amount), 2) AS avg_order_value
FROM sales_analytics_db.processed
GROUP BY category
ORDER BY category_revenue DESC;



SELECT 
    order_date,
    COUNT(order_id) AS daily_orders,
    SUM(total_amount) AS daily_revenue
FROM sales_analytics_db.processed
GROUP BY order_date
ORDER BY order_date ASC;
