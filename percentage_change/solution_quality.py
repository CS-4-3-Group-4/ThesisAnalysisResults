import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib as mpl
import pandas as pd
import numpy as np
import config
import os


def run():
    """Run the solution quality analysis using pre-calculated summary."""

    # ==================== SETUP ====================

    # Register the font with Matplotlib
    fm.fontManager.addfont(config.FONT_PATH)

    # Get the internal font name (required!)
    font_prop = fm.FontProperties(fname=config.FONT_PATH)
    font_name = font_prop.get_name()

    # Set globally
    mpl.rcParams["font.family"] = font_name

    plt.style.use(config.STYLE_PATH)

    # ==================== DATA LOADING AND PREPARATION ====================

    # Load scenario-level data for line graph
    scenario_data_path = config.get_data_path("solution_quality")
    df_scenarios = pd.read_csv(scenario_data_path)

    # Load summary data for statistics
    summary_data_path = config.get_data_path("solution_quality_summary")
    df_summary = pd.read_csv(summary_data_path)

    # Get column names
    cols = config.get_columns("solution_quality")

    # Extract summary statistics from the summary CSV
    summary_dict = dict(zip(df_summary["Metric"], df_summary["Value"]))

    mean_fa = summary_dict["FA Mean Solution Quality"]
    mean_efa = summary_dict["EFA Mean Solution Quality"]
    mean_change_percent = summary_dict["Mean Percentage Change"]

    print(f"Mean FA Solution Quality: {mean_fa:.6f}")
    print(f"Mean EFA Solution Quality: {mean_efa:.6f}")
    print(f"Mean Solution Quality Change: {mean_change_percent:.2f}%")
    print("\n" + "=" * 50)

    # ==================== OUTPUT DIRECTORY SETUP ====================

    # Create output directory if it doesn't exist
    output_dir = config.get_output_dir("sop1", "solution_quality")

    # ==================== FIGURE 1: Line Graph ====================
    print("Creating Figure 1: Line Graph...")
    fig1, ax1 = plt.subplots(figsize=(10, 6))

    ax1.plot(
        df_scenarios.index + 1,
        df_scenarios[cols["fa"]],
        marker="o",
        label="FA",
        linewidth=2,
        markersize=4,
        color=config.COLORS["fa"],
    )
    ax1.plot(
        df_scenarios.index + 1,
        df_scenarios[cols["efa"]],
        marker="s",
        label="EFA",
        linewidth=2,
        markersize=4,
        color=config.COLORS["efa"],
    )
    ax1.set_xlabel("Scenario Number")
    ax1.set_ylabel("Solution Quality")
    ax1.set_title("FA vs EFA Solution Quality Comparison")
    ax1.legend()
    ax1.grid(True, alpha=1.0)

    fig1.tight_layout()

    # Save figure 1
    output_path_1 = os.path.join(
        output_dir, config.OUTPUT_FILES["solution_quality_comparison"]
    )
    fig1.savefig(output_path_1, dpi=300, bbox_inches="tight")
    print(f"✓ Saved: {output_path_1}")

    # ==================== FIGURE 2: Bar Graph ====================
    print("Creating Figure 2: Bar Graph...")
    fig2, ax2 = plt.subplots(figsize=(10, 6))

    algorithms = ["FA", "EFA"]
    means = [mean_fa, mean_efa]
    colors = [config.COLORS["fa"], config.COLORS["efa"]]

    bars = ax2.bar(algorithms, means, color=colors, alpha=0.7, width=0.5)

    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax2.text(
            bar.get_x() + bar.get_width() / 2.0,
            height,
            f"{height:.6f}",
            ha="center",
            va="bottom",
            fontsize=10,
        )

    ax2.set_ylabel("Mean Solution Quality")
    ax2.set_title("Mean Solution Quality: FA vs EFA")
    ax2.set_ylim(0, max(means) * 1.15)
    ax2.grid(True, alpha=1.0, axis="y")

    fig2.tight_layout()

    # Save figure 2
    output_path_2 = os.path.join(
        output_dir, config.OUTPUT_FILES["mean_solution_quality_comparison"]
    )
    fig2.savefig(output_path_2, dpi=300, bbox_inches="tight")
    print(f"✓ Saved: {output_path_2}")

    # ==================== SAVE RESULTS TO TEXT FILE ====================
    print("Creating results text file...")
    results_path = os.path.join(output_dir, config.OUTPUT_FILES["results"])

    with open(results_path, "w") as f:
        f.write("FA vs EFA Solution Quality Analysis Results\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Mean FA Solution Quality: {mean_fa:.6f}\n")
        f.write(f"Mean EFA Solution Quality: {mean_efa:.6f}\n")
        f.write(f"Mean Solution Quality Change: {mean_change_percent:.2f}%\n")
        f.write("\n" + "=" * 50 + "\n\n")
        f.write("Additional Statistics from Summary:\n")
        f.write("-" * 50 + "\n")
        if "Min Percentage Change" in summary_dict:
            f.write(
                f"Min Percentage Change: {summary_dict['Min Percentage Change']:.2f}%\n"
            )
        if "Max Percentage Change" in summary_dict:
            f.write(
                f"Max Percentage Change: {summary_dict['Max Percentage Change']:.2f}%\n"
            )
        if "Improved Scenarios" in summary_dict:
            f.write(f"Improved Scenarios: {int(summary_dict['Improved Scenarios'])}\n")
        if "Unchanged Scenarios" in summary_dict:
            f.write(
                f"Unchanged Scenarios: {int(summary_dict['Unchanged Scenarios'])}\n"
            )
        if "Degraded Scenarios" in summary_dict:
            f.write(f"Degraded Scenarios: {int(summary_dict['Degraded Scenarios'])}\n")

    print(f"✓ Saved: {results_path}")

    print("=" * 50)
    print("All files saved successfully!")

    # Show both plots
    plt.show()


if __name__ == "__main__":
    run()
