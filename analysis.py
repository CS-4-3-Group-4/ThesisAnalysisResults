import pandas as pd
import numpy as np
from scipy.stats import ttest_rel
import os

# === CONFIG ===
# Just change the filename below when analyzing a new metric file
filename = "comparison/FA-vs-EFA-memory-comparison-1761647438438.csv"

# === LOAD CSV ===
df = pd.read_csv(filename)
df.columns = df.columns.str.strip()  # Clean column names

# Auto-detect the two numeric columns
col1, col2 = df.columns[:2]
metric_name = col1.replace("FA ", "").replace("(ms)", "").strip()

print(f"Analyzing metric: {metric_name}")
print(f"Comparing columns: {col1} vs {col2}\n")

# === CALCULATIONS ===
diff = df[col1] - df[col2]
mean_diff = diff.mean()
std_diff = diff.std(ddof=1)
sem_diff = std_diff / np.sqrt(len(diff))
t_statistic = mean_diff / sem_diff

# Paired t-test
t_stat, p_val = ttest_rel(df[col1], df[col2])

# === OUTPUT ===
print("=== FA vs EFA Comparison Results ===")
print(f"Mean Difference: {mean_diff:.5f}")
print(f"Standard Deviation: {std_diff:.5f}")
print(f"Standard Error of Mean Difference: {sem_diff:.5f}")
print(f"t-Statistic (manual): {t_statistic:.5f}")
print(f"t-Statistic (scipy): {t_stat:.5f}")
print(f"p-Value: {p_val:.5f} ({p_val:.2e})")


# Optional: save summary in 'results/' folder
output_dir = "results"
os.makedirs(output_dir, exist_ok=True)  # create if it doesn't exist

# Build the summary file path (same name but with -summary.txt)
base_name = os.path.splitext(os.path.basename(filename))[0]
summary_path = os.path.join(output_dir, f"{base_name}-summary.txt")

with open(summary_path, "w") as f:
    f.write(f"Metric: {metric_name}\n")
    f.write(f"{col1} vs {col2}\n\n")
    f.write(f"Mean Difference: {mean_diff:.5f}\n")
    f.write(f"Standard Deviation: {std_diff:.5f}\n")
    f.write(f"Standard Error: {sem_diff:.5f}\n")
    f.write(f"t-Statistic: {t_statistic:.5f}\n")
    f.write(f"p-Value: {p_val:.5f}\n")

print(f"\nSummary saved to: {summary_path}")
