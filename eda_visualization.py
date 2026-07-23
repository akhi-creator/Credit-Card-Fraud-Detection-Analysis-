import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def generate_eda_plots(csv_path, output_dir):
    print(f"Generating Seaborn Visual Reports from '{csv_path}'...")
    os.makedirs(output_dir, exist_ok=True)

    # Set Seaborn theme
    sns.set_theme(style="darkgrid", palette="muted")
    plt.rcParams.update({'font.sans-serif': 'DejaVu Sans', 'font.family': 'sans-serif'})

    df = pd.read_csv(csv_path)

    # 1. Correlation Heatmap
    plt.figure(figsize=(10, 8))
    numeric_cols = [
        'amount', 'distance_from_home', 'ratio_to_median_price',
        'repeat_retailer', 'used_chip', 'used_pin', 'is_online_order',
        'hour_of_day', 'is_night_transaction', 'high_risk_amount_flag',
        'distance_anomaly_flag', 'risk_severity_score', 'is_fraud'
    ]
    corr = df[numeric_cols].corr()
    
    mask = np.triu(np.ones_like(corr, dtype=bool))
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.8, center=0,
                square=True, linewidths=.5, annot=True, fmt=".2f",
                cbar_kws={"shrink": .8})
    plt.title("Feature Correlation Heatmap with Fraud Indicator", fontsize=14, fontweight='bold', pad=15)
    plt.tight_layout()
    plot1_path = os.path.join(output_dir, "correlation_heatmap.png")
    plt.savefig(plot1_path, dpi=300)
    plt.close()
    print(f" Saved: '{plot1_path}'")

    # 2. Transaction Amount Distribution (Legitimate vs Fraudulent)
    plt.figure(figsize=(12, 6))
    df['log_amount'] = np.log1p(df['amount'])
    
    palette = {0: "#2ecc71", 1: "#e74c3c", "0": "#2ecc71", "1": "#e74c3c"}
    df['is_fraud_num'] = df['is_fraud'].astype(int)
    ax = sns.boxplot(x='is_fraud_num', y='log_amount', data=df, palette=palette, width=0.4)
    ax.set_xticklabels(['Legitimate (0)', 'Fraudulent (1)'], fontsize=12, fontweight='bold')
    plt.title("Transaction Amount Distribution (Log Scale)", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Transaction Type", fontsize=12, labelpad=10)
    plt.ylabel("Log(Amount + 1)", fontsize=12, labelpad=10)
    
    # Annotate median values
    medians = df.groupby(['is_fraud'])['amount'].median()
    ax.text(0, np.log1p(medians[0]), f"Median: ${medians[0]:.2f}", horizontalalignment='center', size=11, color='black', weight='semibold')
    ax.text(1, np.log1p(medians[1]), f"Median: ${medians[1]:.2f}", horizontalalignment='center', size=11, color='white', weight='semibold')

    plt.tight_layout()
    plot2_path = os.path.join(output_dir, "transaction_amount_dist.png")
    plt.savefig(plot2_path, dpi=300)
    plt.close()
    print(f" Saved: '{plot2_path}'")

    # 3. Fraud Rate by Merchant Category
    plt.figure(figsize=(12, 6))
    cat_summary = df.groupby('merchant_category').agg(
        total=('is_fraud', 'count'),
        frauds=('is_fraud', 'sum')
    ).reset_index()
    cat_summary['fraud_rate'] = (cat_summary['frauds'] / cat_summary['total']) * 100
    cat_summary = cat_summary.sort_values(by='fraud_rate', ascending=False)

    ax = sns.barplot(x='fraud_rate', y='merchant_category', data=cat_summary, palette="flare")
    plt.title("Fraud Rate (%) by Merchant Category", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Fraud Rate (%)", fontsize=12)
    plt.ylabel("Merchant Category", fontsize=12)

    for p in ax.patches:
        width = p.get_width()
        ax.annotate(f"{width:.1f}%",
                    (width + 0.3, p.get_y() + p.get_height() / 2.),
                    ha='left', va='center', fontsize=10, fontweight='bold')

    plt.tight_layout()
    plot3_path = os.path.join(output_dir, "fraud_by_category.png")
    plt.savefig(plot3_path, dpi=300)
    plt.close()
    print(f" Saved: '{plot3_path}'")

    # 4. Spending Velocity & Distance Anomaly Scatter Plot
    plt.figure(figsize=(11, 7))
    sample_df = df.sample(n=min(5000, len(df)), random_state=42) # Sample for clean visual
    
    sns.scatterplot(
        x='distance_from_home', y='ratio_to_median_price',
        hue='is_fraud', style='is_fraud',
        data=sample_df, palette={0: '#3498db', 1: '#e74c3c'},
        alpha=0.7, s=60
    )
    plt.axhline(y=3.0, color='r', linestyle='--', alpha=0.7, label='3x Median Ratio Threshold')
    plt.axvline(x=100.0, color='orange', linestyle='--', alpha=0.7, label='100 Mile Distance Threshold')
    
    plt.title("Unusual Spending Pattern Analysis (Distance vs. Ratio to Median Price)", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Distance From Home (Miles)", fontsize=12)
    plt.ylabel("Ratio to Median Purchase Price", fontsize=12)
    plt.legend(title="Transaction Status", labels=['100 Mile Limit', '3x Price Ratio', 'Legitimate', 'Fraudulent'])
    plt.yscale('log')

    plt.tight_layout()
    plot4_path = os.path.join(output_dir, "spending_velocity_anomaly.png")
    plt.savefig(plot4_path, dpi=300)
    plt.close()
    print(f" Saved: '{plot4_path}'")

    # 5. Hourly Fraud Trend
    plt.figure(figsize=(12, 5))
    hourly = df.groupby('hour_of_day')['is_fraud'].agg(['count', 'mean']).reset_index()
    hourly['fraud_pct'] = hourly['mean'] * 100

    ax = sns.lineplot(x='hour_of_day', y='fraud_pct', data=hourly, marker='o', color='#e74c3c', linewidth=2.5, markersize=8)
    plt.fill_between(hourly['hour_of_day'], hourly['fraud_pct'], color='#e74c3c', alpha=0.15)
    
    plt.title("Fraud Probability Trend by Hour of Day", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Hour of Day (0 - 23)", fontsize=12)
    plt.ylabel("Fraud Rate (%)", fontsize=12)
    plt.xticks(range(0, 24))
    
    # Highlight night risk zone
    plt.axvspan(1, 4, color='red', alpha=0.1, label='High-Risk Night Window (1 AM - 4 AM)')
    plt.legend(loc='upper right')

    plt.tight_layout()
    plot5_path = os.path.join(output_dir, "fraud_by_hour.png")
    plt.savefig(plot5_path, dpi=300)
    plt.close()
    print(f" Saved: '{plot5_path}'")

    print("All 5 Seaborn EDA Visualizations Generated Successfully!")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(__file__))
    csv_file = os.path.join(base_dir, "data", "cleaned_transactions.csv")
    out_dir = os.path.join(base_dir, "visual_reports")
    
    generate_eda_plots(csv_file, out_dir)
