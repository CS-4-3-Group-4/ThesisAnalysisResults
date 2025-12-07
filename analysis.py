import pandas as pd
import numpy as np
from scipy.stats import ttest_rel
import os
import sys


def analyze_metric(metric_type: str):
    """
    Analyzes a CSV comparison file for FA vs EFA results based on the given metric.
    Usage example:
        python analysis.py fitness
        python analysis.py memory
    Supported metrics: 'fitness', 'time', 'memory'.
    """

    # === FILE SELECTION ===
    base_path = "comparison"
    file_map = {
        "fitness": "FA-vs-EFA-fitness-comparison.csv",
        "time": "FA-vs-EFA-executionTime-comparison.csv",
        "memory": "FA-vs-EFA-memory-comparison.csv",
    }

    if metric_type not in file_map:
        print(f"❌ Invalid metric type: {metric_type}")
        print(f"Valid options: {list(file_map.keys())}")
        sys.exit(1)

    filename = os.path.join(base_path, file_map[metric_type])
    print(f"📂 Loading file: {filename}")

    # === LOAD CSV ===
    df = pd.read_csv(filename)
    df.columns = df.columns.str.strip()  # Clean column names

    # Auto-detect the two numeric columns
    col1, col2 = df.columns[:2]
    metric_name = col1.replace("FA ", "").replace("(ms)", "").strip()

    print(f"\nAnalyzing metric: {metric_name}")
    print(f"Comparing columns: {col1} vs {col2}\n")

    # === CALCULATIONS ===
    diff = df[col1] - df[col2]
    mean_diff = diff.mean()
    std_diff = diff.std(ddof=1)
    sem_diff = std_diff / np.sqrt(len(diff))
    t_stat_manual = mean_diff / sem_diff

    # Paired t-test
    t_stat, p_val = ttest_rel(df[col1], df[col2])

    # === OUTPUT ===
    print("=== FA vs EFA Comparison Results ===")
    print(f"Mean Difference: {mean_diff:.6f}")
    print(f"Standard Deviation: {std_diff:.6f}")
    print(f"Standard Error of Mean Difference: {sem_diff:.6f}")
    print(f"t-Statistic (manual): {t_stat_manual:.6f}")
    print(f"t-Statistic (scipy): {t_stat:.6f}")
    print(f"p-Value: {p_val:.6f} ({p_val:.2e})")

    # === SAVE SUMMARY ===
    output_dir = "results"
    os.makedirs(output_dir, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(filename))[0]
    summary_path = os.path.join(output_dir, f"{base_name}-summary.txt")

    with open(summary_path, "w") as f:
        f.write(f"Metric: {metric_name}\n")
        f.write(f"{col1} vs {col2}\n\n")
        f.write(f"Mean Difference: {mean_diff:.6f}\n")
        f.write(f"Standard Deviation: {std_diff:.6f}\n")
        f.write(f"Standard Error: {sem_diff:.6f}\n")
        f.write(f"t-Statistic: {t_stat_manual:.6f}\n")
        f.write(f"p-Value: {p_val:.6f}\n")

    print(f"\n📝 Summary saved to: {summary_path}")


# === MAIN ENTRYPOINT ===
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analysis.py <metric_type>")
        print("Example: python analysis.py fitness")
        sys.exit(1)

    metric_type = sys.argv[1].lower().strip()
    analyze_metric(metric_type)
