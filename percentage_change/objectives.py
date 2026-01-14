import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib as mpl
import pandas as pd
import numpy as np
import config
import os


def run():
    """Run the multi-objective analysis with scenario-by-scenario comparison."""

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

    # Load data
    data_path = config.get_data_path("objectives")
    df = pd.read_csv(data_path)

    # Get column names
    cols = config.get_columns("objectives")

    # ==================== OUTPUT DIRECTORY SETUP ====================

    # Create output directory if it doesn't exist
    output_dir = config.get_output_dir("objectives")

    # Get objective settings
    num_objectives = config.OBJECTIVE_SETTINGS["num_objectives"]
    y_limits = config.OBJECTIVE_SETTINGS["y_limits"]
    obj_names = config.OBJECTIVE_SETTINGS["objective_names"]
    obj_descriptions = config.OBJECTIVE_SETTINGS["objective_descriptions"]

    # ==================== CREATE PLOTS FOR EACH OBJECTIVE ====================

    results_summary = []

    for obj_num in range(1, num_objectives + 1):
        obj_key = f"objective{obj_num}"
        obj_cols = cols[obj_key]

        print(f"\n{'=' * 50}")
        print(f"Processing {obj_names[obj_num]}...")
        print("=" * 50)

        # Calculate means
        mean_fa = df[obj_cols["fa"]].mean()
        mean_efa = df[obj_cols["efa"]].mean()

        # Calculate mean change (%)
        mean_change_percent = (
            ((mean_efa - mean_fa) / mean_fa) * 100 if mean_fa != 0 else 0
        )

        print(f"Mean FA: {mean_fa:.6f}")
        print(f"Mean EFA: {mean_efa:.6f}")
        print(f"Mean Change: {mean_change_percent:.2f}%")

        # Store results
        results_summary.append(
            {
                "objective": obj_names[obj_num],
                "mean_fa": mean_fa,
                "mean_efa": mean_efa,
                "change_percent": mean_change_percent,
            }
        )

        # ==================== FIGURE 1: Line Graph ====================
        print(f"Creating line graph for {obj_names[obj_num]}...")
        fig1, ax1 = plt.subplots(figsize=(10, 6))

        ax1.plot(
            df.index + 1,
            df[obj_cols["fa"]],
            marker="o",
            label="FA",
            linewidth=2,
            markersize=4,
            color=config.COLORS["fa"],
        )
        ax1.plot(
            df.index + 1,
            df[obj_cols["efa"]],
            marker="s",
            label="EFA",
            linewidth=2,
            markersize=4,
            color=config.COLORS["efa"],
        )
        ax1.set_xlabel("Run Number")
        ax1.set_ylabel(f"{obj_names[obj_num]} Score")
        ax1.set_title(
            f"FA vs EFA: {obj_names[obj_num]} Comparison\n({obj_descriptions[obj_num]})"
        )
        ax1.legend()
        ax1.grid(True, alpha=1.0)

        fig1.tight_layout()

        # Save figure 1
        output_filename = config.OUTPUT_FILES["objective_comparison"].format(obj_num)
        output_path_1 = os.path.join(output_dir, output_filename)
        fig1.savefig(output_path_1, dpi=300, bbox_inches="tight")
        print(f"✓ Saved: {output_path_1}")

        # ==================== FIGURE 2: Mean Bar Graph ====================
        print(f"Creating mean bar graph for {obj_names[obj_num]}...")
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

        ax2.set_ylabel(f"Mean {obj_names[obj_num]} Score")
        ax2.set_title(
            f"FA vs EFA: Mean {obj_names[obj_num]}\n({obj_descriptions[obj_num]})"
        )
        ax2.set_ylim(0, max(means) * 1.15)
        ax2.grid(True, alpha=1.0, axis="y")

        fig2.tight_layout()

        # Save figure 2
        output_filename_2 = config.OUTPUT_FILES["mean_objective_comparison"].format(
            obj_num
        )
        output_path_2 = os.path.join(output_dir, output_filename_2)
        fig2.savefig(output_path_2, dpi=300, bbox_inches="tight")
        print(f"✓ Saved: {output_path_2}")

        # ==================== FIGURE 3: SCENARIO-BY-SCENARIO GROUPED BAR CHART ====================
        print(f"Creating scenario-by-scenario bar graph for {obj_names[obj_num]}...")

        num_scenarios = len(df)

        # Adjust figure width based on number of scenarios
        fig_width = max(12, num_scenarios * 0.4)
        fig3, ax3 = plt.subplots(figsize=(fig_width, 7))

        # Set up positions for grouped bars
        x_positions = np.arange(num_scenarios)
        bar_width = 0.35

        # Create bars for FA and EFA
        bars_fa = ax3.bar(
            x_positions - bar_width / 2,
            df[obj_cols["fa"]],
            bar_width,
            label="FA",
            color=config.COLORS["fa"],
            alpha=0.7,
        )

        bars_efa = ax3.bar(
            x_positions + bar_width / 2,
            df[obj_cols["efa"]],
            bar_width,
            label="EFA",
            color=config.COLORS["efa"],
            alpha=0.7,
        )

        # Customize the plot
        ax3.set_xlabel("Scenario Number")
        ax3.set_ylabel(f"{obj_names[obj_num]} Score")
        ax3.set_title(
            f"FA vs EFA: {obj_names[obj_num]} by Scenario\n({obj_descriptions[obj_num]})"
        )
        ax3.set_xticks(x_positions)
        ax3.set_xticklabels(df.index + 1, rotation=45 if num_scenarios > 15 else 0)
        ax3.legend()
        ax3.grid(True, alpha=0.3, axis="y")

        fig3.tight_layout()

        # Save figure 3
        output_filename_3 = f"objective_{obj_num}_scenario_comparison.png"
        output_path_3 = os.path.join(output_dir, output_filename_3)
        fig3.savefig(output_path_3, dpi=300, bbox_inches="tight")
        print(f"✓ Saved: {output_path_3}")

        # ==================== FIGURE 4: SEPARATE LINE GRAPHS (STACKED) ====================
        print(f"Creating stacked line graphs for {obj_names[obj_num]}...")

        fig4, (ax_top, ax_bottom) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

        # Top plot: FA
        ax_top.plot(
            df.index + 1,
            df[obj_cols["fa"]],
            marker="o",
            linewidth=2,
            markersize=4,
            color=config.COLORS["fa"],
            label="FA",
        )
        ax_top.set_ylabel(f"{obj_names[obj_num]} Score")
        ax_top.set_title(
            f"FA: {obj_names[obj_num]}\n({obj_descriptions[obj_num]})",
            fontweight="bold",
        )
        ax_top.legend(loc="upper right")
        ax_top.grid(True, alpha=1.0)

        # Bottom plot: EFA
        ax_bottom.plot(
            df.index + 1,
            df[obj_cols["efa"]],
            marker="s",
            linewidth=2,
            markersize=4,
            color=config.COLORS["efa"],
            label="EFA",
        )
        ax_bottom.set_xlabel("Run Number")
        ax_bottom.set_ylabel(f"{obj_names[obj_num]} Score")
        ax_bottom.set_title(
            f"EFA: {obj_names[obj_num]}\n({obj_descriptions[obj_num]})",
            fontweight="bold",
        )
        ax_bottom.legend(loc="upper right")
        ax_bottom.grid(True, alpha=1.0)

        # # Add overall title
        # fig4.suptitle(
        #     f"Separate Comparison: {obj_names[obj_num]}",
        #     fontsize=14,
        #     fontweight="bold",
        #     y=0.995,
        # )

        fig4.tight_layout()

        # Save figure 4
        output_filename_4 = f"objective_{obj_num}_separate_comparison.png"
        output_path_4 = os.path.join(output_dir, output_filename_4)
        fig4.savefig(output_path_4, dpi=300, bbox_inches="tight")
        print(f"✓ Saved: {output_path_4}")

        plt.close(fig1)
        plt.close(fig2)
        plt.close(fig3)
        plt.close(fig4)

    # ==================== SAVE RESULTS TO TEXT FILE ====================
    print(f"\n{'=' * 50}")
    print("Creating results text file...")
    results_path = os.path.join(output_dir, config.OUTPUT_FILES["results"])

    with open(results_path, "w") as f:
        f.write("FA vs EFA Multi-Objective Analysis Results\n")
        f.write("=" * 50 + "\n\n")

        for result in results_summary:
            f.write(f"{result['objective']}:\n")
            f.write("-" * 50 + "\n")
            f.write(f"Mean FA: {result['mean_fa']:.6f}\n")
            f.write(f"Mean EFA: {result['mean_efa']:.6f}\n")
            f.write(f"Mean Change: {result['change_percent']:.2f}%\n\n")

    print(f"✓ Saved: {results_path}")

    print("=" * 50)
    print("All files saved successfully!")


if __name__ == "__main__":
    run()
