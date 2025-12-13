import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib as mpl
import pandas as pd
import numpy as np
from scipy.stats import ttest_rel
import config
import os


def run():
    """Run the memory usage significance test (SOP 4)."""

    # ==================== SETUP ====================

    # Register the font with Matplotlib
    fm.fontManager.addfont(config.FONT_PATH)

    # Get the internal font name (required!)
    font_prop = fm.FontProperties(fname=config.FONT_PATH)
    font_name = font_prop.get_name()

    # Set globally
    mpl.rcParams["font.family"] = font_name

    plt.style.use(config.STYLE_PATH)

    print("=" * 50)
    print("SOP 4: Memory Usage Significance Test")
    print("=" * 50)

    # Output directory setup
    output_dir = config.get_output_dir("sop4", "memory")

    # ==================== DATA LOADING ====================

    # Load data
    data_path = config.get_data_path("memory")
    df = pd.read_csv(data_path)

    # Get column names
    cols = config.get_columns("memory")

    # ==================== STATISTICAL CALCULATIONS ====================

    # Calculate difference (FA - EFA)
    diff = df[cols["fa"]] - df[cols["efa"]]
    mean_diff = diff.mean()
    std_diff = diff.std(ddof=1)
    sem_diff = std_diff / np.sqrt(len(diff))
    t_stat_manual = mean_diff / sem_diff

    # Paired t-test
    t_stat, p_val = ttest_rel(df[cols["fa"]], df[cols["efa"]])

    # Calculate box plot statistics for both FA and EFA
    box_stats = {}
    for label, col in [("FA", cols["fa"]), ("EFA", cols["efa"])]:
        data = df[col]
        q1 = data.quantile(0.25)
        median = data.median()
        q3 = data.quantile(0.75)
        iqr = q3 - q1
        lower_fence = q1 - 1.5 * iqr
        upper_fence = q3 + 1.5 * iqr
        lower_whisker = data[data >= lower_fence].min()
        upper_whisker = data[data <= upper_fence].max()

        # Identify outliers
        outliers = data[(data < lower_fence) | (data > upper_fence)]

        box_stats[label] = {
            "min": data.min(),
            "q1": q1,
            "median": median,
            "q3": q3,
            "max": data.max(),
            "iqr": iqr,
            "lower_fence": lower_fence,
            "upper_fence": upper_fence,
            "lower_whisker": lower_whisker,
            "upper_whisker": upper_whisker,
            "outliers": outliers.tolist(),
            "n_outliers": len(outliers),
        }

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

    # ==================== SAVE STATISTICAL RESULTS ====================

    print("\nCreating results text file...")
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

    # ==================== BOX PLOT VISUALIZATION ====================

    print("\n" + "=" * 50)
    print("Creating Box Plot...")
    fig, ax = plt.subplots(figsize=(10, 6))

    # Prepare data for box plot
    data_to_plot = [df[cols["fa"]], df[cols["efa"]]]
    box_colors = [config.COLORS["fa"], config.COLORS["efa"]]

    bp = ax.boxplot(data_to_plot, labels=["FA", "EFA"], patch_artist=True, widths=0.6)

    # Color the boxes
    for patch, color in zip(bp["boxes"], box_colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    # Style the plot
    ax.set_ylabel("Memory Usage (bytes)")
    ax.set_title("FA vs EFA Memory Usage Distribution")
    ax.grid(True, alpha=1.0, axis="y")

    fig.tight_layout()

    # Save figure
    output_path = os.path.join(output_dir, "memory_boxplot.png")
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"✓ Saved: {output_path}")

    # ==================== SAVE BOX PLOT STATISTICS ====================

    print("Creating box plot statistics file...")
    boxplot_stats_path = os.path.join(output_dir, config.OUTPUT_FILES["boxplot_stats"])

    with open(boxplot_stats_path, "w") as f:
        f.write("Box Plot Statistics - Memory Usage (SOP 4)\n")
        f.write("=" * 60 + "\n\n")

        for label in ["FA", "EFA"]:
            stats = box_stats[label]
            f.write(f"{label} Statistics:\n")
            f.write("-" * 60 + "\n")
            f.write(f"Minimum:        {stats['min']:.6f} bytes\n")
            f.write(f"Lower Fence:    {stats['lower_fence']:.6f} bytes\n")
            f.write(f"Lower Whisker:  {stats['lower_whisker']:.6f} bytes\n")
            f.write(f"Q1 (25th):      {stats['q1']:.6f} bytes\n")
            f.write(f"Median (50th):  {stats['median']:.6f} bytes\n")
            f.write(f"Q3 (75th):      {stats['q3']:.6f} bytes\n")
            f.write(f"Upper Whisker:  {stats['upper_whisker']:.6f} bytes\n")
            f.write(f"Upper Fence:    {stats['upper_fence']:.6f} bytes\n")
            f.write(f"Maximum:        {stats['max']:.6f} bytes\n")
            f.write(f"IQR:            {stats['iqr']:.6f} bytes\n")
            f.write(f"\nOutliers:       {stats['n_outliers']} detected\n")

            if stats["n_outliers"] > 0:
                f.write("Outlier values (bytes):\n")
                for i, outlier in enumerate(stats["outliers"], 1):
                    f.write(f"  {i}. {outlier:.6f}\n")
            else:
                f.write("  (No outliers detected)\n")

            f.write("\n" + "=" * 60 + "\n\n")

    print(f"✓ Saved: {boxplot_stats_path}")

    # ==================== COMPLETION ====================

    print("=" * 50)
    print("Analysis complete! All files saved successfully!")

    # Show plot
    plt.show()


if __name__ == "__main__":
    run()
