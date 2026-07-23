import os
import csv
from datetime import datetime

def preprocess_credit_card_data(raw_csv_path, cleaned_csv_path, power_bi_csv_path):
    print("Beginning Data Preprocessing and Cleaning...")
    
    if not os.path.exists(raw_csv_path):
        raise FileNotFoundError(f"Raw dataset not found at '{raw_csv_path}'. Please run generate_dataset.py first.")

    records = []
    headers = []

    with open(raw_csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        for row in reader:
            records.append(row)

    print(f"Loaded {len(records)} raw records for processing.")

    # Data Quality & Cleaning
    cleaned_records = []
    duplicate_ids = set()
    seen_ids = set()
    null_count = 0

    total_amount = 0.0
    fraud_amount = 0.0
    total_fraud = 0

    processed_headers = headers + [
        "hour_of_day", "day_of_week", "is_night_transaction",
        "high_risk_amount_flag", "distance_anomaly_flag", "risk_severity_score"
    ]

    for row in records:
        txn_id = row['transaction_id']
        
        # Check duplicate
        if txn_id in seen_ids:
            duplicate_ids.add(txn_id)
            continue
        seen_ids.add(txn_id)

        # Type conversion & sanity checks
        try:
            amount = float(row['amount'])
            distance = float(row['distance_from_home'])
            ratio = float(row['ratio_to_median_price'])
            is_fraud = int(row['is_fraud'])
            used_chip = int(row['used_chip'])
            used_pin = int(row['used_pin'])
            is_online = int(row['is_online_order'])
            dt = datetime.strptime(row['timestamp'], "%Y-%m-%d %H:%M:%S")
        except (ValueError, KeyError):
            null_count += 1
            continue

        hour = dt.hour
        day_of_week = dt.strftime("%A")
        is_night = 1 if hour in [22, 23, 0, 1, 2, 3, 4, 5] else 0
        high_risk_amount = 1 if ratio >= 3.0 else 0
        distance_anomaly = 1 if distance >= 100.0 else 0

        # Heuristic Risk Severity Score (0.0 to 100.0)
        risk_score = 0.0
        if ratio >= 3.0: risk_score += 35.0
        if distance_anomaly: risk_score += 25.0
        if is_night: risk_score += 15.0
        if is_online and not used_pin: risk_score += 15.0
        if row['merchant_category'] in ["Electronics", "Luxury Goods", "Online Retail"]: risk_score += 10.0
        risk_score = min(100.0, risk_score)

        row_copy = dict(row)
        row_copy['hour_of_day'] = hour
        row_copy['day_of_week'] = day_of_week
        row_copy['is_night_transaction'] = is_night
        row_copy['high_risk_amount_flag'] = high_risk_amount
        row_copy['distance_anomaly_flag'] = distance_anomaly
        row_copy['risk_severity_score'] = f"{risk_score:.1f}"

        cleaned_records.append(row_copy)

        total_amount += amount
        if is_fraud:
            total_fraud += 1
            fraud_amount += amount

    # Write cleaned dataset
    os.makedirs(os.path.dirname(cleaned_csv_path), exist_ok=True)
    with open(cleaned_csv_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=processed_headers)
        writer.writeheader()
        writer.writerows(cleaned_records)

    # Write Power BI optimized export
    os.makedirs(os.path.dirname(power_bi_csv_path), exist_ok=True)
    with open(power_bi_csv_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=processed_headers)
        writer.writeheader()
        writer.writerows(cleaned_records)

    print(f"Data Cleaning Completed!")
    print(f" - Retained Valid Records: {len(cleaned_records)}")
    print(f" - Duplicate Records Removed: {len(duplicate_ids)}")
    print(f" - Null/Corrupt Records Dropped: {null_count}")
    print(f" - Total Transaction Volume: ${total_amount:,.2f}")
    print(f" - Total Fraudulent Volume: ${fraud_amount:,.2f} ({total_fraud} transactions)")
    print(f" - Cleaned output saved to '{cleaned_csv_path}'")
    print(f" - Power BI export saved to '{power_bi_csv_path}'")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(__file__))
    raw_path = os.path.join(base_dir, "data", "raw_transactions.csv")
    cleaned_path = os.path.join(base_dir, "data", "cleaned_transactions.csv")
    pbi_path = os.path.join(base_dir, "data", "power_bi_export.csv")
    
    preprocess_credit_card_data(raw_path, cleaned_path, pbi_path)
