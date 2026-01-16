from pathlib import Path
import duckdb
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "processed" / "ventas_limpias.csv"
DB_PATH = ROOT / "data" / "processed" / "ventas.duckdb"

def main():
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"No existe: {CSV_PATH}")

    df = pd.read_csv(CSV_PATH)

    con = duckdb.connect(str(DB_PATH))
    con.execute("DROP TABLE IF EXISTS ventas;")
    con.register("df", df)
    con.execute("CREATE TABLE ventas AS SELECT * FROM df;")

    rows = con.execute("SELECT COUNT(*) FROM ventas;").fetchone()[0]
    print("✅ DB creada")
    print(f"Ruta: {DB_PATH}")
    print(f"Filas: {rows}")

if __name__ == "__main__":
    main()
