import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib as mpl
import pandas as pd
import numpy as np
import config
import os


def run():
    """Run the barangay-level aggregated analysis across all scenarios."""

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
    print("Barangay-Level Aggregated Analysis")
    print("=" * 50)

    # ==================== DATA LOADING ====================

    # Load barangay-level data
    data_path = config.get_data_path("barangay_solution_quality")
    df = pd.read_csv(data_path)

    # Get column names
    cols = config.get_columns("barangay_solution_quality")

    # Output directory setup
    output_dir = config.get_output_dir("sop1", "solution_quality_barangays")

    # ==================== DATA ANALYSIS ====================

    total_allocations = len(df)
    improved = len(df[df[cols["percentage_change"]] > 0])
    unchanged = len(df[df[cols["percentage_change"]] == 0])
    degraded = len(df[df[cols["percentage_change"]] < 0])

    improved_pct = (improved / total_allocations) * 100
    unchanged_pct = (unchanged / total_allocations) * 100
    degraded_pct = (degraded / total_allocations) * 100

    avg_improvement = df[cols["percentage_change"]].mean()
    median_improvement = df[cols["percentage_change"]].median()

    print(f"\nTotal barangay allocations analyzed: {total_allocations}")
    print(f"Improved: {improved} ({improved_pct:.1f}%)")
    print(f"Unchanged: {unchanged} ({unchanged_pct:.1f}%)")
    print(f"Degraded: {degraded} ({degraded_pct:.1f}%)")
    print(f"Average improvement: {avg_improvement:.2f}%")
    print(f"Median improvement: {median_improvement:.2f}%")

    # ==================== FIGURE 1: IMPROVEMENT DISTRIBUTION HISTOGRAM ====================

    print("\n" + "=" * 50)
    print("Creating Figure 1: Improvement Distribution Histogram...")

    fig1, ax1 = plt.subplots(figsize=(12, 6))

    # Create histogram
    n, bins, patches = ax1.hist(
        df[cols["percentage_change"]],
        bins=30,
        color=config.COLORS["efa"],
        alpha=0.7,
        edgecolor="black",
    )

    # Color bars: green for positive, red for negative
    for i, patch in enumerate(patches):
        if bins[i] < 0:
            patch.set_facecolor("#ff6b6b")  # Red for degraded
        elif bins[i] > 0:
            patch.set_facecolor("#51cf66")  # Green for improved
        else:
            patch.set_facecolor("#868e96")  # Gray for unchanged

    # Add vertical line at 0
    ax1.axvline(x=0, color="black", linestyle="--", linewidth=2, label="No Change")

    # Add mean and median lines
    ax1.axvline(
        x=avg_improvement,
        color=config.COLORS["efa"],
        linestyle="-",
        linewidth=2,
        label=f"Mean: {avg_improvement:.2f}%",
    )
    ax1.axvline(
        x=median_improvement,
        color=config.COLORS["fa"],
        linestyle="-",
        linewidth=2,
        label=f"Median: {median_improvement:.2f}%",
    )

    ax1.set_xlabel("Percentage Change (%)")
    ax1.set_ylabel("Number of Barangay Allocations")
    ax1.set_title("Distribution of EFA Improvement Across All Barangay Allocations")
    ax1.legend()
    ax1.grid(True, alpha=0.3, axis="y")

    fig1.tight_layout()

    output_path_1 = os.path.join(
        output_dir, config.OUTPUT_FILES["barangay_improvement_histogram"]
    )
    fig1.savefig(output_path_1, dpi=300, bbox_inches="tight")
    print(f"✓ Saved: {output_path_1}")

    # ==================== FIGURE 2: HAZARD LEVEL BOX PLOT ====================

    print("Creating Figure 2: Hazard Level Comparison...")

    fig2, ax2 = plt.subplots(figsize=(12, 6))

    # Group data by hazard level
    hazard_levels = df[cols["hazard_level"]].unique()
    hazard_order = ["High", "Medium", "Low", "None"]

    # Filter to only existing hazard levels in the correct order
    hazard_order = [h for h in hazard_order if h in hazard_levels]

    # Prepare data for box plot
    fa_data_by_hazard = []
    efa_data_by_hazard = []
    labels = []

    for hazard in hazard_order:
        hazard_df = df[df[cols["hazard_level"]] == hazard]
        fa_data_by_hazard.append(hazard_df[cols["fa_score"]].values)
        efa_data_by_hazard.append(hazard_df[cols["efa_score"]].values)
        labels.append(hazard)

    # Create positions for boxes
    positions_fa = np.arange(len(labels)) * 3
    positions_efa = positions_fa + 1

    # Create box plots
    bp_fa = ax2.boxplot(
        fa_data_by_hazard,
        positions=positions_fa,
        widths=0.6,
        patch_artist=True,
        labels=labels,
    )
    bp_efa = ax2.boxplot(
        efa_data_by_hazard,
        positions=positions_efa,
        widths=0.6,
        patch_artist=True,
        labels=[""] * len(labels),  # No labels for EFA
    )

    # Color the boxes
    for patch in bp_fa["boxes"]:
        patch.set_facecolor(config.COLORS["fa"])
        patch.set_alpha(0.7)

    for patch in bp_efa["boxes"]:
        patch.set_facecolor(config.COLORS["efa"])
        patch.set_alpha(0.7)

    # Set x-tick labels at the center of each pair
    ax2.set_xticks(positions_fa + 0.5)
    ax2.set_xticklabels(labels)
    ax2.set_xlabel("Hazard Level")
    ax2.set_ylabel("Solution Quality Score")
    ax2.set_title("FA vs EFA Performance by Hazard Level")
    ax2.grid(True, alpha=0.3, axis="y")

    # Add legend
    from matplotlib.patches import Patch

    legend_elements = [
        Patch(facecolor=config.COLORS["fa"], alpha=0.7, label="FA"),
        Patch(facecolor=config.COLORS["efa"], alpha=0.7, label="EFA"),
    ]
    ax2.legend(handles=legend_elements)

    fig2.tight_layout()

    output_path_2 = os.path.join(
        output_dir, config.OUTPUT_FILES["barangay_hazard_boxplot"]
    )
    fig2.savefig(output_path_2, dpi=300, bbox_inches="tight")
    print(f"✓ Saved: {output_path_2}")

    # ==================== FIGURE 3: SUMMARY BAR CHART ====================

    print("Creating Figure 3: Summary Bar Chart...")

    fig3, ax3 = plt.subplots(figsize=(10, 6))

    categories = ["Improved", "Unchanged", "Degraded"]
    counts = [improved, unchanged, degraded]
    colors_summary = ["#51cf66", "#868e96", "#ff6b6b"]

    bars = ax3.bar(categories, counts, color=colors_summary, alpha=0.7, width=0.6)

    # Add value labels on bars
    for bar, count, pct in zip(
        bars, counts, [improved_pct, unchanged_pct, degraded_pct]
    ):
        height = bar.get_height()
        ax3.text(
            bar.get_x() + bar.get_width() / 2.0,
            height,
            f"{count}\n({pct:.1f}%)",
            ha="center",
            va="bottom",
            fontsize=10,
        )

    ax3.set_ylabel("Number of Barangay Allocations")
    ax3.set_title(f"EFA Performance Summary (Total: {total_allocations} allocations)")
    ax3.set_ylim(0, max(counts) * 1.2)
    ax3.grid(True, alpha=0.3, axis="y")

    fig3.tight_layout()

    output_path_3 = os.path.join(
        output_dir, config.OUTPUT_FILES["barangay_summary_bars"]
    )
    fig3.savefig(output_path_3, dpi=300, bbox_inches="tight")
    print(f"✓ Saved: {output_path_3}")

    # ==================== FIGURE 4: TOP/BOTTOM PERFORMERS ====================

    print("Creating Figure 4: Top and Bottom Performers...")

    # Get top N performers setting
    top_n = config.SOLUTION_QUALITY_SETTINGS["top_n_performers"]

    # Find top improved and top degraded barangays
    # First, aggregate by barangay (average across all scenarios)
    barangay_avg = (
        df.groupby(cols["barangay_name"])[cols["percentage_change"]]
        .mean()
        .reset_index()
    )
    barangay_avg.columns = ["barangay_name", "avg_change"]

    top_improved = barangay_avg.nlargest(top_n, "avg_change")
    top_degraded = barangay_avg.nsmallest(top_n, "avg_change")

    fig4, (ax_top, ax_bottom) = plt.subplots(2, 1, figsize=(12, 10))

    # Top improved
    ax_top.barh(
        range(len(top_improved)),
        top_improved["avg_change"],
        color="#51cf66",
        alpha=0.7,
    )
    ax_top.set_yticks(range(len(top_improved)))
    ax_top.set_yticklabels(top_improved["barangay_name"])
    ax_top.set_xlabel("Average Percentage Change (%)")
    ax_top.set_title(f"Top {top_n} Most Improved Barangays (EFA vs FA)")
    ax_top.grid(True, alpha=0.3, axis="x")
    ax_top.invert_yaxis()

    # Add value labels
    for i, (idx, row) in enumerate(top_improved.iterrows()):
        ax_top.text(
            row["avg_change"],
            i,
            f" {row['avg_change']:.2f}%",
            va="center",
            fontsize=9,
        )

    # Top degraded
    ax_bottom.barh(
        range(len(top_degraded)),
        top_degraded["avg_change"],
        color="#ff6b6b",
        alpha=0.7,
    )
    ax_bottom.set_yticks(range(len(top_degraded)))
    ax_bottom.set_yticklabels(top_degraded["barangay_name"])
    ax_bottom.set_xlabel("Average Percentage Change (%)")
    ax_bottom.set_title(f"Top {top_n} Most Degraded Barangays (EFA vs FA)")
    ax_bottom.grid(True, alpha=0.3, axis="x")
    ax_bottom.invert_yaxis()

    # Add value labels
    for i, (idx, row) in enumerate(top_degraded.iterrows()):
        ax_bottom.text(
            row["avg_change"],
            i,
            f" {row['avg_change']:.2f}%",
            va="center",
            fontsize=9,
        )

    fig4.tight_layout()

    output_path_4 = os.path.join(
        output_dir, config.OUTPUT_FILES["barangay_top_performers"]
    )
    fig4.savefig(output_path_4, dpi=300, bbox_inches="tight")
    print(f"✓ Saved: {output_path_4}")

    # ==================== SAVE TEXT RESULTS ====================

    print("\nCreating barangay analysis results file...")
    results_path = os.path.join(
        output_dir, config.OUTPUT_FILES["barangay_analysis_results"]
    )

    with open(results_path, "w") as f:
        f.write("Barangay-Level Aggregated Analysis Results\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Total barangay allocations analyzed: {total_allocations}\n")
        f.write(
            f"  (Across {df[cols['scenario']].nunique()} scenarios × ~{len(df) // df[cols['scenario']].nunique()} barangays)\n\n"
        )
        f.write("Overall Summary:\n")
        f.write("-" * 60 + "\n")
        f.write(f"Improved allocations: {improved} ({improved_pct:.2f}%)\n")
        f.write(f"Unchanged allocations: {unchanged} ({unchanged_pct:.2f}%)\n")
        f.write(f"Degraded allocations: {degraded} ({degraded_pct:.2f}%)\n")
        f.write(f"\nAverage improvement: {avg_improvement:.4f}%\n")
        f.write(f"Median improvement: {median_improvement:.4f}%\n")
        f.write(f"Min change: {df[cols['percentage_change']].min():.4f}%\n")
        f.write(f"Max change: {df[cols['percentage_change']].max():.4f}%\n")
        f.write("\n" + "=" * 60 + "\n\n")

        # Hazard level breakdown
        f.write("Performance by Hazard Level:\n")
        f.write("-" * 60 + "\n")
        for hazard in hazard_order:
            hazard_df = df[df[cols["hazard_level"]] == hazard]
            hazard_improved = len(hazard_df[hazard_df[cols["percentage_change"]] > 0])
            hazard_total = len(hazard_df)
            hazard_avg = hazard_df[cols["percentage_change"]].mean()
            f.write(f"\n{hazard} Hazard:\n")
            f.write(f"  Total: {hazard_total}\n")
            f.write(
                f"  Improved: {hazard_improved} ({hazard_improved/hazard_total*100:.1f}%)\n"
            )
            f.write(f"  Avg change: {hazard_avg:.4f}%\n")

        f.write("\n" + "=" * 60 + "\n\n")

        # Top performers
        f.write(f"Top {top_n} Most Improved Barangays (by average):\n")
        f.write("-" * 60 + "\n")
        for i, (idx, row) in enumerate(top_improved.iterrows(), 1):
            f.write(f"{i}. {row['barangay_name']}: {row['avg_change']:.2f}%\n")

        f.write(f"\nTop {top_n} Most Degraded Barangays (by average):\n")
        f.write("-" * 60 + "\n")
        for i, (idx, row) in enumerate(top_degraded.iterrows(), 1):
            f.write(f"{i}. {row['barangay_name']}: {row['avg_change']:.2f}%\n")

    print(f"✓ Saved: {results_path}")

    # ==================== COMPLETION ====================

    print("=" * 50)
    print("All barangay analysis files saved successfully!")

    # Show plots
    plt.show()


if __name__ == "__main__":
    run()
