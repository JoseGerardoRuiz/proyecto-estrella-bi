WITH base AS (
  SELECT
    customer_id,
    CAST(order_date AS DATE) AS order_date
  FROM ventas
),
primera_compra AS (
  SELECT customer_id, MIN(order_date) AS first_date
  FROM base
  GROUP BY 1
),
con_mes AS (
  SELECT
    b.customer_id,
    DATE_TRUNC('month', p.first_date) AS cohort_month,
    DATE_TRUNC('month', b.order_date) AS order_month
  FROM base b
  JOIN primera_compra p USING (customer_id)
)
SELECT
  cohort_month,
  DATE_DIFF('month', cohort_month, order_month) AS month_n,
  COUNT(DISTINCT customer_id) AS customers
FROM con_mes
GROUP BY 1,2
ORDER BY 1,2;
