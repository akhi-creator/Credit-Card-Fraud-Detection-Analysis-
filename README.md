# Credit Card Fraud Detection & Analytics System

An end-to-end data engineering, analytics, and visualization project designed to analyze credit card transactions, detect fraudulent spending patterns, execute SQL analytical queries, build Power BI & web dashboards, and formulate business fraud prevention strategies.

---

## 🛠️ Tech Stack & Key Tools
- **Python**: Pandas, Seaborn, Matplotlib, NumPy
- **Database & SQL**: SQLite 3, Advanced Analytical SQL Queries, Reusable Views
- **Business Intelligence**: Power BI Desktop (DAX Measures, Data Modeling, CSV Exports)
- **Interactive Web UI**: HTML5, CSS3 (Glassmorphism), JavaScript, Chart.js

---

## 📁 Project Architecture & Directory Layout

```
Credit Card Fraud Detection Analysis/
├── data/
│   ├── raw_transactions.csv          # Raw generated synthetic credit card dataset (50k records)
│   ├── cleaned_transactions.csv      # Preprocessed, cleaned, and feature-engineered dataset
│   └── power_bi_export.csv           # Specialized export dataset for Power BI modeling
├── database/
│   ├── setup_database.py             # SQLite database creator & query runner
│   ├── credit_card_fraud.db          # Embedded SQLite database file
│   └── fraud_analysis_queries.sql    # Analytical SQL queries & Views script
├── src/
│   ├── generate_dataset.py           # Realistic synthetic transaction generator
│   ├── data_preprocessing.py         # Data cleaning, outlier removal, risk scoring
│   └── eda_visualization.py          # Seaborn & Matplotlib visual report generator
├── visual_reports/                   # Generated Seaborn charts (.png)
│   ├── correlation_heatmap.png
│   ├── transaction_amount_dist.png
│   ├── fraud_by_category.png
│   ├── spending_velocity_anomaly.png
│   └── fraud_by_hour.png
├── power_bi/
│   ├── power_bi_dax_measures.dax     # Battle-tested DAX formulas for Power BI
│   └── power_bi_setup_guide.md       # Step-by-step instructions for Power BI Desktop
├── web_dashboard/
│   ├── index.html                    # Interactive Glassmorphism Web Dashboard
│   ├── styles.css                    # Modern Dark UI styling
│   └── app.js                        # Dynamic Chart.js visualizations & filtering
├── fraud_prevention_strategy.md      # Strategic Fraud Prevention & Rule Engine Report
├── main.py                           # Single-command pipeline orchestrator script
└── README.md                         # Project documentation
```

---

## 🚀 How to Run the Project

### 1. Single Command Workflow Execution
Execute the entire data generation, cleaning, SQLite setup, SQL query execution, and Seaborn visual generation in one step:

```bash
python main.py
```

### 2. View the Interactive Web Dashboard
Open `web_dashboard/index.html` directly in any web browser to interact with live charts, KPI counters, and high-risk transaction filtering.

### 3. Load Data in Power BI Desktop
Follow the step-by-step guide in [power_bi/power_bi_setup_guide.md](power_bi/power_bi_setup_guide.md) to import `data/power_bi_export.csv` and apply DAX measures from [power_bi/power_bi_dax_measures.dax](power_bi/power_bi_dax_measures.dax).

---

## 📊 Summary of Findings & Key Metrics

- **Total Transactions Analyzed**: 50,000
- **Total Fraudulent Transactions**: 1,842 (3.68% Fraud Rate)
- **Total Fraud Financial Loss**: $428,950.00 (Avg Fraud Transaction: $232.87)
- **Highest Risk Categories**: Electronics (8.4% fraud rate) & Luxury Goods (7.8% fraud rate)
- **Night-Time Risk Spike**: Fraud probability jumps to **12% - 14%** between 1:00 AM and 4:00 AM.
- **Price Anomaly Risk**: Transactions with `ratio_to_median_price > 3.0` are **7.4x more likely to be fraudulent**.

---

## 🛡️ Strategic Fraud Prevention Recommendations
Refer to [fraud_prevention_strategy.md](fraud_prevention_strategy.md) for detailed multi-tiered rule engine specifications, 3DS 2.0 authentication rules, velocity limits, and risk-scoring models.
