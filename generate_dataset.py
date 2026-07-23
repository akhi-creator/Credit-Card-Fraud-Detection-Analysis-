import os
import csv
import random
import math
from datetime import datetime, timedelta

def generate_credit_card_dataset(output_path, num_records=50000, seed=42):
    random.seed(seed)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    categories = [
        "Online Retail", "Electronics", "Grocery", "Dining",
        "Travel & Hotels", "Luxury Goods", "Gas Station", "Entertainment"
    ]
    
    # Category baseline fraud propensity multipliers
    category_fraud_weight = {
        "Online Retail": 1.8,
        "Electronics": 2.2,
        "Luxury Goods": 2.5,
        "Travel & Hotels": 1.5,
        "Entertainment": 1.1,
        "Dining": 0.6,
        "Gas Station": 0.7,
        "Grocery": 0.4
    }

    customers = [f"CUST_{i:04d}" for i in range(1, 2001)]
    # Pre-generate customer median spending baselines ($15 to $180)
    customer_medians = {c: round(random.uniform(15.0, 180.0), 2) for c in customers}

    start_date = datetime.now() - timedelta(days=90)
    
    headers = [
        "transaction_id", "timestamp", "customer_id", "amount",
        "merchant_category", "distance_from_home", "ratio_to_median_price",
        "repeat_retailer", "used_chip", "used_pin", "is_online_order", "is_fraud"
    ]

    print(f"Generating {num_records} realistic credit card transactions...")
    
    fraud_count = 0

    with open(output_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for i in range(1, num_records + 1):
            txn_id = f"TXN_{i:06d}"
            customer_id = random.choice(customers)
            c_median = customer_medians[customer_id]

            # Timestamp over 90 days
            random_minutes = random.randint(0, 90 * 24 * 60)
            txn_time = start_date + timedelta(minutes=random_minutes)
            hour = txn_time.hour

            is_online = 1 if random.random() < 0.45 else 0
            merchant_cat = random.choice(categories)
            repeat_retailer = 1 if random.random() < 0.65 else 0

            # Card technology
            if is_online:
                used_chip = 0
                used_pin = 0
            else:
                used_chip = 1 if random.random() < 0.85 else 0
                used_pin = 1 if random.random() < 0.70 else 0

            # Distance from home (miles)
            if random.random() < 0.90:
                distance = round(random.exponential(scale=8.0) if hasattr(random, 'exponential') else random.uniform(0.1, 25.0), 2)
            else:
                distance = round(random.uniform(50.0, 850.0), 2)

            # Amount & Ratio to median
            # Determine if this transaction triggers fraud characteristics
            base_risk = category_fraud_weight[merchant_cat] * 0.015
            
            # Risk amplification conditions
            if hour in [1, 2, 3, 4]:
                base_risk *= 2.5
            if is_online and not used_pin:
                base_risk *= 1.8
            if distance > 100:
                base_risk *= 2.2
            
            # Decide fraud status probabilistically based on combined risk score
            is_fraud = 1 if random.random() < min(base_risk, 0.45) else 0

            if is_fraud:
                fraud_count += 1
                # Fraudulent transactions often exhibit abnormal spending ratios and distances
                ratio_to_median = round(random.uniform(3.2, 14.5), 2)
                amount = round(c_median * ratio_to_median, 2)
                if random.random() < 0.4:
                    distance = round(random.uniform(120.0, 1500.0), 2)
            else:
                # Normal transactions cluster around customer median
                ratio_to_median = round(max(0.1, random.gauss(1.0, 0.45)), 2)
                amount = round(c_median * ratio_to_median, 2)

            amount = max(0.99, amount)

            writer.writerow([
                txn_id,
                txn_time.strftime("%Y-%m-%d %H:%M:%S"),
                customer_id,
                f"{amount:.2f}",
                merchant_cat,
                f"{distance:.2f}",
                f"{ratio_to_median:.2f}",
                repeat_retailer,
                used_chip,
                used_pin,
                is_online,
                is_fraud
            ])

    fraud_rate = (fraud_count / num_records) * 100
    print(f"Dataset successfully created at '{output_path}'!")
    print(f"Total Transactions: {num_records} | Fraudulent Cases: {fraud_count} ({fraud_rate:.2f}%)")

if __name__ == "__main__":
    target_csv = os.path.join(os.path.dirname(__file__), "..", "data", "raw_transactions.csv")
    generate_credit_card_dataset(target_csv, num_records=50000)
