SELECT
  product_id,
  product_name,
  category,
  SUM(quantity) AS units,
  ROUND(SUM(revenue), 2) AS revenue
FROM ventas
GROUP BY 1,2,3
ORDER BY revenue DESC
LIMIT 10;
