import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib as mpl
import pandas as pd
import numpy as np
import config
import os


def run():
    """Run the execution time analysis."""

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
    data_path = config.get_data_path("time")
    df = pd.read_csv(data_path)

    # Get column names
    cols = config.get_columns("time")

    # Calculate means
    mean_fa = df[cols["fa"]].mean()
    mean_efa = df[cols["efa"]].mean()

    # Calculate mean change (%)
    mean_change_percent = ((mean_efa - mean_fa) / mean_fa) * 100

    print(f"Mean FA Execution Time: {mean_fa:.2f} ms")
    print(f"Mean EFA Execution Time: {mean_efa:.2f} ms")
    print(f"Mean Execution Time Change: {mean_change_percent:.2f}%")
    print("\n" + "=" * 50)

    # ==================== OUTPUT DIRECTORY SETUP ====================

    # Create output directory if it doesn't exist
    output_dir = config.get_output_dir("sop2", "time")

    # ==================== FIGURE 1: Line Graph ====================
    print("Creating Figure 1: Line Graph...")
    fig1, ax1 = plt.subplots(figsize=(10, 6))

    ax1.plot(
        df.index + 1,
        df[cols["fa"]],
        marker="o",
        label="FA",
        linewidth=2,
        markersize=4,
        color=config.COLORS["fa"],
    )
    ax1.plot(
        df.index + 1,
        df[cols["efa"]],
        marker="s",
        label="EFA",
        linewidth=2,
        markersize=4,
        color=config.COLORS["efa"],
    )
    ax1.set_xlabel("Run Number")
    ax1.set_ylabel("Execution Time (ms)")
    ax1.set_title("FA vs EFA Execution Time Comparison")
    ax1.legend()
    ax1.grid(True, alpha=1.0)

    fig1.tight_layout()

    # Save figure 1
    output_path_1 = os.path.join(output_dir, config.OUTPUT_FILES["time_comparison"])
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
            f"{height:.2f} ms",
            ha="center",
            va="bottom",
            fontsize=10,
        )

    ax2.set_ylabel("Mean Execution Time (ms)")
    ax2.set_title("Mean Execution Time: FA vs EFA")
    ax2.set_ylim(0, max(means) * 1.15)
    ax2.grid(True, alpha=1.0, axis="y")

    fig2.tight_layout()

    # Save figure 2
    output_path_2 = os.path.join(
        output_dir, config.OUTPUT_FILES["mean_time_comparison"]
    )
    fig2.savefig(output_path_2, dpi=300, bbox_inches="tight")
    print(f"✓ Saved: {output_path_2}")

    # ==================== SAVE RESULTS TO TEXT FILE ====================
    print("Creating results text file...")
    results_path = os.path.join(output_dir, config.OUTPUT_FILES["results"])

    with open(results_path, "w") as f:
        f.write("FA vs EFA Execution Time Analysis Results\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Mean FA Execution Time: {mean_fa:.2f} ms\n")
        f.write(f"Mean EFA Execution Time: {mean_efa:.2f} ms\n")
        f.write(f"Mean Execution Time Change: {mean_change_percent:.2f}%\n")

    print(f"✓ Saved: {results_path}")

    print("=" * 50)
    print("All files saved successfully!")

    # Show both plots
    plt.show()


if __name__ == "__main__":
    run()
