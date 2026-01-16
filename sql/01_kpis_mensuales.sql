SELECT
  STRFTIME(CAST(order_date AS DATE), '%Y-%m') AS year_month,
  COUNT(DISTINCT order_id) AS orders,
  COUNT(DISTINCT customer_id) AS customers,
  ROUND(SUM(revenue), 2) AS revenue,
  ROUND(SUM(revenue) / NULLIF(COUNT(DISTINCT order_id), 0), 2) AS aov
FROM ventas
GROUP BY 1
ORDER BY 1;
