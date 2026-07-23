import os
import sqlite3
import csv

def setup_and_query_database(db_path, cleaned_csv_path, sql_script_path):
    print(f"Setting up SQLite Database at '{db_path}'...")
    
    if os.path.exists(db_path):
        os.remove(db_path)

    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create transactions table
    create_table_sql = """
    CREATE TABLE transactions (
        transaction_id TEXT PRIMARY KEY,
        timestamp DATETIME,
        customer_id TEXT,
        amount REAL,
        merchant_category TEXT,
        distance_from_home REAL,
        ratio_to_median_price REAL,
        repeat_retailer INTEGER,
        used_chip INTEGER,
        used_pin INTEGER,
        is_online_order INTEGER,
        is_fraud INTEGER,
        hour_of_day INTEGER,
        day_of_week TEXT,
        is_night_transaction INTEGER,
        high_risk_amount_flag INTEGER,
        distance_anomaly_flag INTEGER,
        risk_severity_score REAL
    );
    """
    cursor.execute(create_table_sql)

    # Insert cleaned records
    print(f"Loading cleaned transactions into SQLite database...")
    with open(cleaned_csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        to_db = [
            (
                r['transaction_id'], r['timestamp'], r['customer_id'],
                float(r['amount']), r['merchant_category'], float(r['distance_from_home']),
                float(r['ratio_to_median_price']), int(r['repeat_retailer']),
                int(r['used_chip']), int(r['used_pin']), int(r['is_online_order']),
                int(r['is_fraud']), int(r['hour_of_day']), r['day_of_week'],
                int(r['is_night_transaction']), int(r['high_risk_amount_flag']),
                int(r['distance_anomaly_flag']), float(r['risk_severity_score'])
            ) for r in reader
        ]

    insert_sql = """
    INSERT INTO transactions VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);
    """
    cursor.executemany(insert_sql, to_db)
    conn.commit()

    print(f"Successfully inserted {len(to_db)} records into database table 'transactions'.")

    # Read and execute SQL analysis queries script
    if os.path.exists(sql_script_path):
        print(f"Executing SQL Analysis queries script: '{sql_script_path}'...")
        with open(sql_script_path, mode='r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Split statements by semicolon
        queries = [q.strip() for q in sql_content.split(';') if q.strip()]
        
        for idx, query in enumerate(queries, 1):
            # Ignore comments-only blocks
            lines = [l for l in query.split('\n') if not l.strip().startswith('--')]
            clean_query = '\n'.join(lines).strip()
            if not clean_query:
                continue

            try:
                cursor.execute(clean_query)
                if clean_query.upper().startswith("SELECT"):
                    results = cursor.fetchall()
                    col_names = [description[0] for description in cursor.description]
                    print(f"\n--- SQL Query Results [{idx}] ---")
                    print(" | ".join(col_names))
                    print("-" * (len(col_names) * 15))
                    for row in results[:10]: # Print top 10 rows
                        print(" | ".join(str(val) for val in row))
                    if len(results) > 10:
                        print(f"... ({len(results) - 10} more rows)")
                else:
                    conn.commit()
            except sqlite3.Error as e:
                print(f"SQL Execution Note on Query [{idx}]: {e}")

    conn.close()
    print("\nSQLite Database setup and analytical query execution completed successfully!")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(__file__))
    db_file = os.path.join(base_dir, "database", "credit_card_fraud.db")
    csv_file = os.path.join(base_dir, "data", "cleaned_transactions.csv")
    sql_file = os.path.join(base_dir, "database", "fraud_analysis_queries.sql")
    
    setup_and_query_database(db_file, csv_file, sql_file)
