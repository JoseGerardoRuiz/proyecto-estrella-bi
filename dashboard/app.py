from pathlib import Path
import duckdb
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "processed" / "ventas.duckdb"

st.set_page_config(page_title="Proyecto Estrella BI", layout="wide")
st.title("📊 Proyecto Estrella BI – Ventas")

@st.cache_data
def load_data():
    con = duckdb.connect(str(DB_PATH), read_only=True)

    kpis = con.execute("""
        SELECT
          STRFTIME(CAST(order_date AS DATE), '%Y-%m') AS year_month,
          COUNT(DISTINCT order_id) AS orders,
          COUNT(DISTINCT customer_id) AS customers,
          ROUND(SUM(revenue), 2) AS revenue,
          ROUND(SUM(revenue) / NULLIF(COUNT(DISTINCT order_id), 0), 2) AS aov
        FROM ventas
        GROUP BY 1
        ORDER BY 1;
    """).df()

    top = con.execute("""
        SELECT
          product_name,
          category,
          SUM(quantity) AS units,
          ROUND(SUM(revenue), 2) AS revenue
        FROM ventas
        GROUP BY 1,2
        ORDER BY revenue DESC
        LIMIT 10;
    """).df()

    detalle = con.execute("""
        SELECT
          CAST(order_date AS DATE) AS order_date,
          customer_id,
          product_name,
          category,
          quantity,
          unit_price,
          revenue,
          city,
          channel
        FROM ventas;
    """).df()

    return kpis, top, detalle

kpis, top, detalle = load_data()

# KPIs principales
c1, c2, c3, c4 = st.columns(4)
c1.metric("Revenue total", f"${detalle['revenue'].sum():,.0f}")
c2.metric("Órdenes", f"{detalle['customer_id'].count():,}")
c3.metric("Clientes únicos", f"{detalle['customer_id'].nunique():,}")
c4.metric("AOV", f"${(detalle['revenue'].sum()/detalle.shape[0]):,.0f}")

st.divider()

st.subheader("📈 KPIs por mes")
st.dataframe(kpis, use_container_width=True)
st.line_chart(kpis.set_index("year_month")[["revenue", "orders", "customers"]])

st.divider()

st.subheader("🏆 Top 10 productos por revenue")
st.dataframe(top, use_container_width=True)
st.bar_chart(top.set_index("product_name")[["revenue"]])

st.divider()

st.subheader("🔎 Detalle de ventas (filtros)")
city = st.selectbox("Ciudad", ["Todas"] + sorted(detalle["city"].unique()))
channel = st.selectbox("Canal", ["Todos"] + sorted(detalle["channel"].unique()))

f = detalle.copy()
if city != "Todas":
    f = f[f["city"] == city]
if channel != "Todos":
    f = f[f["channel"] == channel]

st.dataframe(
    f.sort_values("order_date", ascending=False).head(200),
    use_container_width=True
)
