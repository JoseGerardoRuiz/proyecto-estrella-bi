from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "processed" / "ventas.duckdb"
SQL_DIR = ROOT / "sql"

def run_file(con, filename):
    path = SQL_DIR / filename
    query = path.read_text(encoding="utf-8")
    print(f"\n--- {filename} ---")
    df = con.execute(query).df()
    print(df.head(20).to_string(index=False))

def main():
    if not DB_PATH.exists():
        raise FileNotFoundError(f"No existe DB: {DB_PATH}. Corre primero load_to_duckdb.py")

    con = duckdb.connect(str(DB_PATH))
    run_file(con, "01_kpis_mensuales.sql")
    run_file(con, "02_top_productos.sql")
    run_file(con, "03_retencion_basica.sql")

if __name__ == "__main__":
    main()
