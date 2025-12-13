import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib as mpl
import pandas as pd
import numpy as np
from scipy.stats import ttest_rel
import config
import os


def run():
    """Run the fitness score significance test (SOP 3)."""

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
    print("SOP 3: Fitness Score Significance Test")
    print("=" * 50)

    # ==================== DATA LOADING ====================

    # Load data
    data_path = config.get_data_path("fitness")
    df = pd.read_csv(data_path)

    # Get column names
    cols = config.get_columns("fitness")

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
    print(f"Mean Difference: {mean_diff:.6f}")
    print(f"Standard Deviation: {std_diff:.6f}")
    print(f"Standard Error of Mean: {sem_diff:.6f}")
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

    output_dir = config.get_output_dir("sop3")

    # ==================== FIGURE: Box Plot Comparison ====================
    print("\n" + "=" * 50)
    print("Creating Box Plot...")
    fig, ax = plt.subplots(figsize=(12, 6))

    # Prepare data for box plot
    data_to_plot = [df[cols["fa"]], df[cols["efa"]]]
    box_colors = [config.COLORS["fa"], config.COLORS["efa"]]

    bp = ax.boxplot(data_to_plot, labels=["FA", "EFA"], patch_artist=True, widths=0.6)

    # Color the boxes
    for patch, color in zip(bp["boxes"], box_colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    # Style the plot
    ax.set_ylabel("Fitness Score")
    ax.set_title("FA vs EFA Fitness Score Distribution")
    ax.grid(True, alpha=1.0, axis="y")

    # Add labels beside each box plot element
    for i, (data, label) in enumerate(zip(data_to_plot, ["FA", "EFA"])):
        x_pos = i + 1  # Box plot position (1 for FA, 2 for EFA)

        q1 = data.quantile(0.25)
        median = data.median()
        q3 = data.quantile(0.75)
        iqr = q3 - q1
        lower_whisker = data[data >= q1 - 1.5 * iqr].min()
        upper_whisker = data[data <= q3 + 1.5 * iqr].max()

        # Label each element to the right of the box
        offset = 0.35  # Distance from box center
        ax.text(
            x_pos + offset,
            upper_whisker,
            f"Upper: {upper_whisker:.6f}",
            va="center",
            fontsize=8,
        )
        ax.text(x_pos + offset, q3, f"Q3: {q3:.6f}", va="center", fontsize=8)
        ax.text(
            x_pos + offset,
            median,
            f"Median: {median:.6f}",
            va="center",
            fontsize=8,
            fontweight="bold",
        )
        ax.text(x_pos + offset, q1, f"Q1: {q1:.6f}", va="center", fontsize=8)
        ax.text(
            x_pos + offset,
            lower_whisker,
            f"Lower: {lower_whisker:.6f}",
            va="center",
            fontsize=8,
        )

    fig.tight_layout()

    # Save figure
    output_path = os.path.join(output_dir, "fitness_boxplot.png")
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"✓ Saved: {output_path}")

    # ==================== SAVE RESULTS TO TEXT FILE ====================

    print("Creating results text file...")
    results_path = os.path.join(output_dir, config.OUTPUT_FILES["results"])

    with open(results_path, "w") as f:
        f.write("FA vs EFA Fitness Score Significance Test (SOP 3)\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Comparing: {cols['fa']} vs {cols['efa']}\n")
        f.write(f"Number of paired samples: {len(df)}\n\n")
        f.write("Statistical Results:\n")
        f.write("-" * 50 + "\n")
        f.write(f"Mean Difference: {mean_diff}\n")
        f.write(f"Standard Deviation: {std_diff}\n")
        f.write(f"Standard Error of Mean: {sem_diff}\n")
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
    print("Analysis complete!, All files saved successfully!")

    # Show plot
    plt.show()


if __name__ == "__main__":
    run()
