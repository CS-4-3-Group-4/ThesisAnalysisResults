import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib as mpl
import pandas as pd
import numpy as np
import config
import os


def run():
    """Generate per-scenario barangay detail reports."""

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
    print("Per-Scenario Barangay Detail Analysis")
    print("=" * 50)

    # ==================== DATA LOADING ====================

    # Load barangay-level data
    data_path = config.get_data_path("barangay_solution_quality")
    df = pd.read_csv(data_path)

    # Get column names
    cols = config.get_columns("barangay_solution_quality")

    # Output directory setup
    output_dir = config.get_output_dir("sop1", "solution_quality_scenarios")

    # Get settings
    settings = config.SOLUTION_QUALITY_SETTINGS
    generate_all = settings["generate_all_scenarios"]
    selected_scenarios = settings["selected_scenarios"]
    height_per_barangay = settings["figure_height_per_barangay"]
    min_height = settings["min_scenario_figure_height"]
    sort_by = settings["sort_barangays_by"]
    show_names = settings["show_barangay_names"]

    # Determine which scenarios to process
    all_scenarios = sorted(df[cols["scenario"]].unique())
    scenarios_to_process = all_scenarios if generate_all else selected_scenarios

    print(f"\nProcessing {len(scenarios_to_process)} scenario(s)...")
    print(f"Scenarios: {scenarios_to_process}")

    # ==================== PROCESS EACH SCENARIO ====================

    scenario_stats = []  # Store stats for summary

    for scenario_num in scenarios_to_process:
        print(f"\n{'='*50}")
        print(f"Processing Scenario {scenario_num}...")
        print(f"{'='*50}")

        # Filter data for this scenario
        scenario_df = df[df[cols["scenario"]] == scenario_num].copy()

        if len(scenario_df) == 0:
            print(f"⚠ Warning: No data found for scenario {scenario_num}")
            continue

        num_barangays = len(scenario_df)
        print(f"Barangays in this scenario: {num_barangays}")

        # Sort barangays
        if sort_by == "hazard_level":
            # Sort by hazard level (High -> Medium -> Low -> None), then by name
            hazard_order = {"High": 0, "Medium": 1, "Low": 2, "None": 3}
            scenario_df["hazard_sort"] = scenario_df[cols["hazard_level"]].map(
                hazard_order
            )
            # Fill any unmapped values with a high number to sort them last
            scenario_df["hazard_sort"] = scenario_df["hazard_sort"].fillna(999)
            scenario_df = scenario_df.sort_values(
                ["hazard_sort", cols["barangay_name"]]
            ).reset_index(drop=True)
            scenario_df = scenario_df.drop("hazard_sort", axis=1)
        elif sort_by == "improvement":
            scenario_df = scenario_df.sort_values(
                cols["percentage_change"], ascending=False
            ).reset_index(drop=True)
        else:  # sort by name
            scenario_df = scenario_df.sort_values(cols["barangay_name"]).reset_index(
                drop=True
            )

        # Calculate statistics for this scenario
        improved = len(scenario_df[scenario_df[cols["percentage_change"]] > 0])
        unchanged = len(scenario_df[scenario_df[cols["percentage_change"]] == 0])
        degraded = len(scenario_df[scenario_df[cols["percentage_change"]] < 0])
        avg_change = scenario_df[cols["percentage_change"]].mean()

        print(f"  Improved: {improved} ({improved/num_barangays*100:.1f}%)")
        print(f"  Unchanged: {unchanged} ({unchanged/num_barangays*100:.1f}%)")
        print(f"  Degraded: {degraded} ({degraded/num_barangays*100:.1f}%)")
        print(f"  Avg change: {avg_change:.2f}%")

        # Store stats for summary
        scenario_stats.append(
            {
                "scenario": scenario_num,
                "num_barangays": num_barangays,
                "improved": improved,
                "unchanged": unchanged,
                "degraded": degraded,
                "avg_change": avg_change,
            }
        )

        # ==================== CREATE VISUALIZATION ====================

        # Calculate figure height based on number of barangays
        fig_height = max(min_height, num_barangays * height_per_barangay)

        fig, ax_main = plt.subplots(figsize=(14, fig_height))

        # ==================== MAIN CHART: HORIZONTAL GROUPED BARS ====================

        y_positions = np.arange(num_barangays)
        bar_height = 0.35

        # Create bars for FA and EFA
        bars_fa = ax_main.barh(
            y_positions - bar_height / 2,
            scenario_df[cols["fa_score"]],
            bar_height,
            label="FA Score",
            color=config.COLORS["fa"],
            alpha=0.7,
        )

        bars_efa = ax_main.barh(
            y_positions + bar_height / 2,
            scenario_df[cols["efa_score"]],
            bar_height,
            label="EFA Score",
            color=config.COLORS["efa"],
            alpha=0.7,
        )

        # Add background coloring based on improvement
        for i, (idx, row) in enumerate(scenario_df.iterrows()):
            pct_change = row[cols["percentage_change"]]
            if pct_change > 0:
                ax_main.axhspan(i - 0.5, i + 0.5, facecolor="#51cf66", alpha=0.1)
            elif pct_change < 0:
                ax_main.axhspan(i - 0.5, i + 0.5, facecolor="#ff6b6b", alpha=0.1)

        # Set y-axis labels
        if show_names:
            labels = []
            for idx, row in scenario_df.iterrows():
                hazard = row[cols["hazard_level"]]
                # Single letter for hazard levels
                if pd.isna(hazard) or hazard == "None" or str(hazard) == "None":
                    hazard_label = "N"
                elif hazard == "High":
                    hazard_label = "H"
                elif hazard == "Medium":
                    hazard_label = "M"
                elif hazard == "Low":
                    hazard_label = "L"
                else:
                    hazard_label = "?"
                labels.append(f"{row[cols['barangay_name']]} ({hazard_label})")
        else:
            labels = []
            for i, (idx, row) in enumerate(scenario_df.iterrows()):
                hazard = row[cols["hazard_level"]]
                # Single letter for hazard levels
                if pd.isna(hazard) or hazard == "None" or str(hazard) == "None":
                    hazard_label = "N"
                elif hazard == "High":
                    hazard_label = "H"
                elif hazard == "Medium":
                    hazard_label = "M"
                elif hazard == "Low":
                    hazard_label = "L"
                else:
                    hazard_label = "?"
                labels.append(f"Brgy {i+1} ({hazard_label})")

        ax_main.set_yticks(y_positions)
        ax_main.set_yticklabels(labels, fontsize=8)
        ax_main.set_xlabel("Score", fontsize=10)
        ax_main.set_title(
            f"Scenario {scenario_num}: Barangay-Level Score Comparison (FA vs EFA)",
            fontsize=12,
            fontweight="bold",
            pad=40,
        )
        ax_main.grid(True, alpha=0.3, axis="x")
        ax_main.set_xlim(
            0, scenario_df[[cols["fa_score"], cols["efa_score"]]].max().max()
        )
        ax_main.set_ylim(-0.5, num_barangays - 0.5)  # Remove extra padding on y-axis
        ax_main.invert_yaxis()  # Invert y-axis so High hazard is at top

        # Add legend at figure level (between title and chart)
        handles, labels_legend = ax_main.get_legend_handles_labels()
        fig.legend(
            handles,
            labels_legend,
            loc="upper center",
            bbox_to_anchor=(0.5, 0.9825),
            ncol=2,
            frameon=False,
            fontsize=9,
        )

        # Add percentage change annotations
        for i, (idx, row) in enumerate(scenario_df.iterrows()):
            pct_change = row[cols["percentage_change"]]
            max_score = max(row[cols["fa_score"]], row[cols["efa_score"]])

            # Determine arrow and color
            if pct_change > 0:
                arrow = "↑"
                color = "#2b8a3e"
            elif pct_change < 0:
                arrow = "↓"
                color = "#c92a2a"
            else:
                arrow = "="
                color = "#495057"

            # Add text annotation
            ax_main.text(
                max_score + 0.02,
                i,
                f"{pct_change:+.1f}% {arrow}",
                va="center",
                fontsize=7,
                color=color,
                fontweight="bold",
            )

        # ==================== SAVE FIGURE ====================

        output_filename = config.OUTPUT_FILES["scenario_detail"].format(scenario_num)
        output_path = os.path.join(output_dir, output_filename)

        fig.tight_layout()
        fig.savefig(output_path, dpi=300, bbox_inches="tight")
        print(f"✓ Saved: {output_path}")

        plt.close(fig)

    # ==================== COMPLETION ====================

    print("\n" + "=" * 50)
    print(
        f"Successfully generated {len(scenarios_to_process)} scenario detail report(s)!"
    )
    print(f"Output directory: {output_dir}")

    # ==================== CREATE OVERALL SUMMARY ====================

    print("\nCreating overall summary file...")
    summary_path = os.path.join(output_dir, "all_scenarios_summary.txt")

    with open(summary_path, "w") as f:
        f.write("Per-Scenario Barangay Detail Analysis - Overall Summary\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Total Scenarios Analyzed: {len(scenario_stats)}\n\n")

        # Calculate totals
        total_barangays = sum(s["num_barangays"] for s in scenario_stats)
        total_improved = sum(s["improved"] for s in scenario_stats)
        total_unchanged = sum(s["unchanged"] for s in scenario_stats)
        total_degraded = sum(s["degraded"] for s in scenario_stats)
        avg_change_overall = sum(s["avg_change"] for s in scenario_stats) / len(
            scenario_stats
        )

        f.write("Overall Statistics:\n")
        f.write("-" * 70 + "\n")
        f.write(f"Total Barangay Allocations: {total_barangays}\n")
        f.write(
            f"Improved: {total_improved} ({total_improved/total_barangays*100:.1f}%)\n"
        )
        f.write(
            f"Unchanged: {total_unchanged} ({total_unchanged/total_barangays*100:.1f}%)\n"
        )
        f.write(
            f"Degraded: {total_degraded} ({total_degraded/total_barangays*100:.1f}%)\n"
        )
        f.write(f"Average Change Across All Scenarios: {avg_change_overall:+.2f}%\n\n")

        f.write("Per-Scenario Breakdown:\n")
        f.write("-" * 70 + "\n")
        f.write(
            f"{'Scenario':<10} {'Barangays':<12} {'Improved':<12} {'Unchanged':<12} {'Degraded':<12} {'Avg Change':<12}\n"
        )
        f.write("-" * 70 + "\n")

        for stat in scenario_stats:
            f.write(
                f"{stat['scenario']:<10} "
                f"{stat['num_barangays']:<12} "
                f"{stat['improved']:<12} "
                f"{stat['unchanged']:<12} "
                f"{stat['degraded']:<12} "
                f"{stat['avg_change']:+.2f}%\n"
            )

    print(f"✓ Saved: {summary_path}")
    print("=" * 50)


if __name__ == "__main__":
    run()
