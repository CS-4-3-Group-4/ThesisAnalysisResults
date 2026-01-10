import json
import pandas as pd
import os


def json_to_csvs():
    """
    Convert solution_quality_comparison.json to 3 CSV files.
    Automatically looks in the comparison/ folder.
    """

    # Define paths
    json_file_path = os.path.join("comparison", "solution_quality_comparison.json")
    output_dir = "comparison"

    print("=" * 70)
    print("JSON to CSV Converter - Solution Quality Analysis")
    print("=" * 70)
    print(f"\nLooking for: {json_file_path}")

    # Check if file exists
    if not os.path.exists(json_file_path):
        print(f"❌ ERROR: File not found: {json_file_path}")
        print(
            f"\nPlease make sure 'solution_quality_comparison.json' exists in the 'comparison/' folder"
        )
        return

    with open(json_file_path, "r") as f:
        data = json.load(f)

    print("✓ JSON loaded successfully")

    # ==================== 1. SCENARIO DATA CSV ====================
    print("\nProcessing scenario-level data...")
    scenarios = []
    for scenario in data["scenarioComparisons"]:
        scenarios.append(
            {
                "Scenario": scenario["scenarioNumber"],
                "FA (Solution Quality)": round(scenario["faSolutionQuality"], 6),
                "EFA (Solution Quality)": round(scenario["efaSolutionQuality"], 6),
                "Percentage Change (%)": round(scenario["percentageChange"], 2),
            }
        )

    df_scenarios = pd.DataFrame(scenarios)
    df_scenarios = df_scenarios.sort_values("Scenario").reset_index(drop=True)

    scenario_data_path = os.path.join(
        output_dir, "FA-vs-EFA-solutionQuality-comparison.csv"
    )
    df_scenarios.to_csv(scenario_data_path, index=False)
    print(f"✓ 1/3 Scenario data CSV saved: {scenario_data_path}")

    # ==================== 2. SCENARIO SUMMARY CSV ====================
    print("Processing scenario summary...")
    scenario_summary = pd.DataFrame(
        [
            {"Metric": "FA Mean Solution Quality", "Value": round(data["faMeanSQ"], 6)},
            {
                "Metric": "EFA Mean Solution Quality",
                "Value": round(data["efaMeanSQ"], 6),
            },
            {
                "Metric": "Mean Percentage Change",
                "Value": round(data["meanPercentageChange"], 2),
            },
            {
                "Metric": "Min Percentage Change",
                "Value": round(data["minPercentageChange"], 2),
            },
            {
                "Metric": "Max Percentage Change",
                "Value": round(data["maxPercentageChange"], 2),
            },
            {"Metric": "Improved Scenarios", "Value": data["improvedScenarios"]},
            {"Metric": "Unchanged Scenarios", "Value": data["unchangedScenarios"]},
            {"Metric": "Degraded Scenarios", "Value": data["degradedScenarios"]},
        ]
    )

    scenario_summary_path = os.path.join(
        output_dir, "FA-vs-EFA-solutionQuality-summary.csv"
    )
    scenario_summary.to_csv(scenario_summary_path, index=False)
    print(f"✓ 2/3 Scenario summary CSV saved: {scenario_summary_path}")

    # ==================== 3. BARANGAY DATA CSV ====================
    print("Processing barangay-level data...")
    barangays = []
    for scenario in data["scenarioComparisons"]:
        for barangay in scenario["barangayComparisons"]:
            barangays.append(
                {
                    "Scenario": scenario["scenarioNumber"],
                    "Barangay_ID": barangay["barangayId"],
                    "Barangay_Name": barangay["barangayName"],
                    "Hazard_Level": barangay["barangayFAScore"]["hazardLevel"],
                    "FA_Allocated": barangay["barangayFAScore"]["allocated"],
                    "FA_Required": barangay["barangayFAScore"]["required"],
                    "EFA_Allocated": barangay["barangayEFAScore"]["allocated"],
                    "EFA_Required": barangay["barangayEFAScore"]["required"],
                    "FA_Score": round(barangay["barangayFAScore"]["score"], 6),
                    "EFA_Score": round(barangay["barangayEFAScore"]["score"], 6),
                    "Percentage_Change": round(barangay["percentageChange"], 2),
                }
            )

    df_barangays = pd.DataFrame(barangays)
    df_barangays = df_barangays.sort_values(["Scenario", "Barangay_ID"]).reset_index(
        drop=True
    )

    barangay_data_path = os.path.join(
        output_dir, "FA-vs-EFA-barangay-solutionQuality-comparison.csv"
    )
    df_barangays.to_csv(barangay_data_path, index=False)
    print(f"✓ 3/3 Barangay data CSV saved: {barangay_data_path}")

    # ==================== SUMMARY ====================
    print("\n" + "=" * 70)
    print("CONVERSION COMPLETE ✓")
    print("=" * 70)


if __name__ == "__main__":
    json_to_csvs()
