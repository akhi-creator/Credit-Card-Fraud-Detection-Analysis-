# Power BI Setup & Dashboard Building Guide

This guide outlines how to build an executive-grade **Credit Card Fraud Analytics Dashboard** in Power BI Desktop using the preprocessed data and DAX measures.

---

## 1. Import Data into Power BI

### Option A: Import CSV Direct (Recommended)
1. Open **Power BI Desktop**.
2. Click **Get Data** -> **Text/CSV**.
3. Select `data/power_bi_export.csv` from the project workspace.
4. Set encoding to **UTF-8** and click **Load**.

### Option B: Import via SQLite Database
1. Click **Get Data** -> **ODBC** / **SQLite ODBC Driver**.
2. Connect to `database/credit_card_fraud.db`.
3. Select table `transactions` or views (`vw_category_fraud_summary`, `vw_hourly_fraud_risk`).

---

## 2. Load DAX Measures

1. In the Fields pane on the right, right-click table `power_bi_export` and select **New Measure**.
2. Open `power_bi/power_bi_dax_measures.dax`.
3. Copy and paste each DAX measure (e.g. `Total Transactions`, `Total Fraud Cases`, `Overall Fraud Rate %`, `Total Fraud Loss ($)`).

---

## 3. Recommended Visual Layout (3-Tab Architecture)

### Page 1: Executive Fraud Overview
- **Header Card Strip**:
  - Card 1: `Total Transactions`
  - Card 2: `Total Fraud Loss ($)` (Formatted as Currency)
  - Card 3: `Overall Fraud Rate %` (Formatted as Percentage)
  - Card 4: `Risk Status Indicator` (Dynamic Alert Color)
- **Bar Chart**: `Total Fraud Loss ($)` by `merchant_category`.
- **Donut Chart**: Fraud volume breakdown by `is_online_order` (Card Present vs. CNP).
- **Slicer Controls**: Date Range, Merchant Category, Day of Week.

### Page 2: Spending Anomalies & Behavioral Analytics
- **Line Chart**: `Overall Fraud Rate %` vs `hour_of_day` (0 - 23).
- **Scatter Plot**: X-Axis `distance_from_home`, Y-Axis `ratio_to_median_price`, Legend `is_fraud`.
- **Matrix Visual**: Merchant Category vs. Security Type (`used_chip`, `used_pin`).

### Page 3: Real-Time Fraud Monitoring & High-Risk Transaction Table
- **Table Visual**: Listing transactions filtered by `risk_severity_score >= 50.0`.
  - Columns: `transaction_id`, `timestamp`, `customer_id`, `amount`, `merchant_category`, `risk_severity_score`, `is_fraud`.
  - Apply Conditional Formatting: Background color gradient on `risk_severity_score` (Yellow to Deep Red).

---

## 4. Format & Theme Recommendations
- **Background**: Dark Navy (`#0b0f19` or `#1a1d24`).
- **Accent Palette**:
  - Legitimate: Emerald Green (`#2ecc71`)
  - Fraud / High Risk: Crimson Red (`#e74c3c`)
  - Warning / Spikes: Vibrant Amber (`#f39c12`)
