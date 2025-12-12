import pandas as pd
import numpy as np
from scipy.stats import ttest_rel
import config
import os


def run():
    """Run the memory usage significance test (SOP 4)."""

    print("=" * 50)
    print("SOP 4: Memory Usage Significance Test")
    print("=" * 50)

    # ==================== DATA LOADING ====================

    # Load data
    data_path = config.get_data_path("memory")
    df = pd.read_csv(data_path)

    # Get column names
    cols = config.get_columns("memory")

    # ==================== CALCULATIONS ====================

    # Calculate difference (FA - EFA)
    diff = df[cols["fa"]] - df[cols["efa"]]
    mean_diff = diff.mean()
    std_diff = diff.std(ddof=1)
    sem_diff = std_diff / np.sqrt(len(diff))
    t_stat_manual = mean_diff / sem_diff

    # Paired t-test
    t_stat, p_val = ttest_rel(df[cols["fa"]], df[cols["efa"]])

    # ==================== DISPLAY RESULTS ====================

    print(f"\nAnalyzing: {cols['fa']} vs {cols['efa']}")
    print(f"Number of paired samples: {len(df)}")
    print("\n" + "-" * 50)
    print("Statistical Results:")
    print("-" * 50)
    print(f"Mean Difference: {mean_diff:.6f} bytes")
    print(f"Standard Deviation: {std_diff:.6f} bytes")
    print(f"Standard Error of Mean: {sem_diff:.6f} bytes")
    print(f"t-Statistic (manual): {t_stat_manual:.6f}")
    print(f"t-Statistic (scipy): {t_stat:.6f}")
    print(f"p-Value: {p_val:.6f} ({p_val:.2e})")

    alpha = config.STATISTICAL_SETTINGS["alpha"]
    if p_val < alpha:
        print(f"\n✓ Result: SIGNIFICANT (p < {alpha})")
        print("  The difference between FA and EFA is statistically significant.")
    else:
        print(f"\n✗ Result: NOT SIGNIFICANT (p >= {alpha})")
        print("  The difference between FA and EFA is not statistically significant.")

    # ==================== OUTPUT DIRECTORY SETUP ====================

    output_dir = config.get_output_dir("sop4", "memory")

    # ==================== SAVE RESULTS TO TEXT FILE ====================

    print("\n" + "=" * 50)
    print("Saving results...")
    results_path = os.path.join(output_dir, config.OUTPUT_FILES["results"])

    with open(results_path, "w") as f:
        f.write("FA vs EFA Memory Usage Significance Test (SOP 4)\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Comparing: {cols['fa']} vs {cols['efa']}\n")
        f.write(f"Number of paired samples: {len(df)}\n\n")
        f.write("Statistical Results:\n")
        f.write("-" * 50 + "\n")
        f.write(f"Mean Difference: {mean_diff} bytes\n")
        f.write(f"Standard Deviation: {std_diff} bytes\n")
        f.write(f"Standard Error of Mean: {sem_diff} bytes\n")
        f.write(f"t-Statistic (manual): {t_stat_manual}\n")
        f.write(f"t-Statistic (scipy): {t_stat}\n")
        f.write(f"p-Value: {p_val} ({p_val:.2e})\n\n")

        if p_val < alpha:
            f.write(f"Result: SIGNIFICANT (p < {alpha})\n")
            f.write("The difference between FA and EFA is statistically significant.\n")
        else:
            f.write(f"Result: NOT SIGNIFICANT (p >= {alpha})\n")
            f.write(
                "The difference between FA and EFA is not statistically significant.\n"
            )

    print(f"✓ Saved: {results_path}")
    print("=" * 50)
    print("Analysis complete!")


if __name__ == "__main__":
    run()
