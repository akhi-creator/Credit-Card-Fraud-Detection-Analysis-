import os
import sys
import time

def run_project_pipeline():
    print("=" * 75)
    print(" CREDIT CARD FRAUD DETECTION ANALYSIS - END-TO-END WORKFLOW ORCHESTRATOR")
    print("=" * 75)
    
    start_time = time.time()
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # 1. Dataset Generation
    print("\n--- STEP 1: Synthetic Dataset Generation ---")
    gen_script = os.path.join(base_dir, "src", "generate_dataset.py")
    raw_csv = os.path.join(base_dir, "data", "raw_transactions.csv")
    from src.generate_dataset import generate_credit_card_dataset
    generate_credit_card_dataset(raw_csv, num_records=50000)

    # 2. Data Cleaning & Preprocessing
    print("\n--- STEP 2: Data Cleaning & Preprocessing ---")
    cleaned_csv = os.path.join(base_dir, "data", "cleaned_transactions.csv")
    pbi_csv = os.path.join(base_dir, "data", "power_bi_export.csv")
    from src.data_preprocessing import preprocess_credit_card_data
    preprocess_credit_card_data(raw_csv, cleaned_csv, pbi_csv)

    # 3. SQLite Database Setup & Queries
    print("\n--- STEP 3: SQLite Database Setup & SQL Query Suite ---")
    db_file = os.path.join(base_dir, "database", "credit_card_fraud.db")
    sql_script = os.path.join(base_dir, "database", "fraud_analysis_queries.sql")
    from database.setup_database import setup_and_query_database
    setup_and_query_database(db_file, cleaned_csv, sql_script)

    # 4. Seaborn EDA Visual Reports
    print("\n--- STEP 4: Seaborn & Matplotlib EDA Visualization Suite ---")
    out_dir = os.path.join(base_dir, "visual_reports")
    try:
        from src.eda_visualization import generate_eda_plots
        generate_eda_plots(cleaned_csv, out_dir)
    except Exception as e:
        print(f"Note on EDA plots (checking Python plotting environment): {e}")

    elapsed = time.time() - start_time
    print("\n" + "=" * 75)
    print(f" PIPELINE COMPLETED SUCCESSFULLY IN {elapsed:.2f} SECONDS!")
    print("=" * 75)
    print("Output Artifacts Ready:")
    print(f" - Cleaned Data CSV : {cleaned_csv}")
    print(f" - Power BI CSV     : {pbi_csv}")
    print(f" - SQLite Database  : {db_file}")
    print(f" - Visual Reports   : {out_dir}")
    print(f" - Web Dashboard    : {os.path.join(base_dir, 'web_dashboard', 'index.html')}")
    print("=" * 75)

if __name__ == "__main__":
    run_project_pipeline()
