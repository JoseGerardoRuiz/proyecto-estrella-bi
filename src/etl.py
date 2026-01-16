from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta
import random

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"

if not RAW.exists():
    RAW.mkdir(parents=True)

if not PROCESSED.exists():
    PROCESSED.mkdir(parents=True)


def generar_datos_ejemplo(n=500, seed=42):
    random.seed(seed)

    productos = [
        ("P001", "Audífonos", "Electrónica"),
        ("P002", "Teclado", "Electrónica"),
        ("P003", "Mouse", "Electrónica"),
        ("P004", "Café", "Alimentos"),
        ("P005", "Playera", "Ropa"),
        ("P006", "Tenis", "Ropa"),
    ]

    ciudades = ["CDMX", "GDL", "MTY", "QRO"]
    canales = ["Web", "Marketplace", "Tienda"]

    filas = []
    start = datetime(2024, 1, 1)

    for i in range(n):
        prod = random.choice(productos)
        qty = random.randint(1, 4)
        precio = random.randint(100, 1500)

        filas.append({
            "order_id": 100000 + i,
            "order_date": (start + timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d"),
            "customer_id": f"C{random.randint(1, 200):04d}",
            "product_id": prod[0],
            "product_name": prod[1],
            "category": prod[2],
            "quantity": qty,
            "unit_price": precio,
            "revenue": qty * precio,
            "channel": random.choice(canales),
            "city": random.choice(ciudades),
        })

    return pd.DataFrame(filas)

def main():
    df = generar_datos_ejemplo()

    raw_path = RAW / "ventas_raw.csv"
    clean_path = PROCESSED / "ventas_limpias.csv"

    raw_path.parent.mkdir(parents=True, exist_ok=True)
    clean_path.parent.mkdir(parents=True, exist_ok=True)


    df.to_csv(raw_path, index=False)
    df.to_csv(clean_path, index=False)

    print("✅ ETL ejecutado correctamente")
    print(clean_path)

if __name__ == "__main__":
    main()
