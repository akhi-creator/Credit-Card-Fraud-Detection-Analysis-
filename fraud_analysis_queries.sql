-- =========================================================================
-- CREDIT CARD FRAUD DETECTION ANALYSIS - SQL QUERY SUITE
-- Database: SQLite (credit_card_fraud.db)
-- Table: transactions
-- =========================================================================

-- 1. EXECUTIVE SUMMARY KPI METRICS
SELECT 
    COUNT(*) AS total_transactions,
    SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) AS total_fraud_transactions,
    ROUND(SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS overall_fraud_rate_pct,
    ROUND(SUM(amount), 2) AS total_transaction_volume_usd,
    ROUND(SUM(CASE WHEN is_fraud = 1 THEN amount ELSE 0 END), 2) AS total_fraud_loss_usd,
    ROUND(AVG(CASE WHEN is_fraud = 1 THEN amount ELSE NULL END), 2) AS avg_fraud_transaction_val
FROM transactions;

-- 2. FRAUD DISTRIBUTION BY MERCHANT CATEGORY
SELECT 
    merchant_category,
    COUNT(*) AS total_txns,
    SUM(is_fraud) AS fraud_count,
    ROUND(SUM(is_fraud) * 100.0 / COUNT(*), 2) AS fraud_rate_pct,
    ROUND(SUM(CASE WHEN is_fraud = 1 THEN amount ELSE 0 END), 2) AS category_fraud_loss_usd
FROM transactions
GROUP BY merchant_category
ORDER BY category_fraud_loss_usd DESC;

-- 3. HOURLY FRAUD RISK ANALYSIS (TEMPORAL PATTERNS)
SELECT 
    hour_of_day,
    COUNT(*) AS volume,
    SUM(is_fraud) AS fraud_count,
    ROUND(SUM(is_fraud) * 100.0 / COUNT(*), 2) AS hourly_fraud_rate_pct
FROM transactions
GROUP BY hour_of_day
ORDER BY hour_of_day ASC;

-- 4. CHANNEL & CARD SECURITY RISK ANALYSIS (Online vs In-Store Chip/PIN)
SELECT 
    CASE WHEN is_online_order = 1 THEN 'Online (Card Not Present)' ELSE 'In-Store (Card Present)' END AS channel,
    used_chip,
    used_pin,
    COUNT(*) AS txn_count,
    SUM(is_fraud) AS fraud_count,
    ROUND(SUM(is_fraud) * 100.0 / COUNT(*), 2) AS fraud_rate_pct
FROM transactions
GROUP BY is_online_order, used_chip, used_pin
ORDER BY fraud_rate_pct DESC;

-- 5. UNUSUAL SPENDING ANOMALY DETECTION (Ratio > 3.0x Median Price)
SELECT 
    transaction_id,
    customer_id,
    amount,
    ratio_to_median_price,
    distance_from_home,
    merchant_category,
    is_fraud
FROM transactions
WHERE ratio_to_median_price > 3.0
ORDER BY ratio_to_median_price DESC
LIMIT 15;

-- 6. GEOGRAPHIC & NIGHT TIME COMBINED HIGH-RISK ANOMALIES
SELECT 
    customer_id,
    COUNT(*) AS total_high_risk_attempts,
    SUM(is_fraud) AS confirmed_frauds,
    ROUND(AVG(amount), 2) AS avg_amount,
    ROUND(AVG(distance_from_home), 2) AS avg_distance
FROM transactions
WHERE is_night_transaction = 1 AND distance_anomaly_flag = 1
GROUP BY customer_id
HAVING confirmed_frauds > 0
ORDER BY confirmed_frauds DESC
LIMIT 10;

-- 7. REUSABLE SQL VIEWS FOR POWER BI & REPORTING

-- View A: Merchant Category Risk Overview
CREATE VIEW IF NOT EXISTS vw_category_fraud_summary AS
SELECT 
    merchant_category,
    COUNT(*) AS total_transactions,
    SUM(is_fraud) AS fraud_transactions,
    ROUND(SUM(is_fraud) * 100.0 / COUNT(*), 2) AS fraud_rate_pct,
    ROUND(SUM(amount), 2) AS total_volume_usd,
    ROUND(SUM(CASE WHEN is_fraud = 1 THEN amount ELSE 0 END), 2) AS total_fraud_loss_usd
FROM transactions
GROUP BY merchant_category;

-- View B: Hourly Fraud Velocity
CREATE VIEW IF NOT EXISTS vw_hourly_fraud_risk AS
SELECT 
    hour_of_day,
    COUNT(*) AS total_txns,
    SUM(is_fraud) AS fraud_txns,
    ROUND(SUM(is_fraud) * 100.0 / COUNT(*), 2) AS fraud_rate_pct
FROM transactions
GROUP BY hour_of_day;

-- View C: High Risk Transaction Queue
CREATE VIEW IF NOT EXISTS vw_high_risk_transactions AS
SELECT 
    transaction_id,
    timestamp,
    customer_id,
    amount,
    merchant_category,
    distance_from_home,
    ratio_to_median_price,
    risk_severity_score,
    is_fraud
FROM transactions
WHERE risk_severity_score >= 50.0
ORDER BY risk_severity_score DESC;
