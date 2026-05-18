"""
Loads Period A and all Period B scenario CSVs into local DuckDB dtabase.
"""

import duckdb
import os

DB_PATH = "data/reliability.duckdb"

def main():
    os.makedirs("data", exist_ok=True)
    con = duckdb.connect(DB_PATH)

    con.execute("DROP TABLE IF EXISTS period_a")
    con.execute("CREATE TABLE period_a as SELECT * FROM read_csv('data/period_a.csv')")
    count = con.execute("SELECT COUNT(*) FROM period_a").fetchone()[0]
    print(f"period_a_loaded: {count} rows")

    for scenario in ["baseline", "mild_drift", "moderate_drift", "severe_drift"]:
        table = f"period_b_{scenario}"
        path = f"data/{table}.csv"
        con.execute(f"DROP TABLE IF EXISTS {table}")
        con.execute(f"CREATE TABLE {table} as SELECT * FROM read_csv('{path}')")
        count = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"{table}_loaded: {count} rows")
    
    con.close()
    print(f"\nDatabase ready at {DB_PATH}")

if __name__ == "__main__":
    main()