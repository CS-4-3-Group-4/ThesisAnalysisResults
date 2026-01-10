"""
Configuration file for FA vs EFA comparison analysis.
Contains file paths, output directories, and comparison settings.
"""

import os

# Base directory (set this to your project root)
BASE_DIR = os.path.dirname(__file__)

# ==================== DIRECTORY PATHS ====================

# Input directories
COMPARISON_DIR = os.path.join(BASE_DIR, "comparison")
STYLES_DIR = os.path.join(BASE_DIR, "styles")

# Output directories
RESULTS_DIR = os.path.join(BASE_DIR, "results")
OUTPUT_DIRS = {
    "sop1": os.path.join(RESULTS_DIR, "sop1"),
    "sop2": os.path.join(RESULTS_DIR, "sop2"),
    "sop3": os.path.join(RESULTS_DIR, "sop3"),
    "sop4": os.path.join(RESULTS_DIR, "sop4"),
    "objectives": os.path.join(RESULTS_DIR, "objectives"),
}

# ==================== DATA FILES ====================

# Comparison data files
DATA_FILES = {
    "time": "FA-vs-EFA-executionTime-comparison.csv",
    "fitness": "FA-vs-EFA-fitness-comparison.csv",
    "memory": "FA-vs-EFA-memory-comparison.csv",
    "objectives": "FA-vs-EFA-objectives-comparison.csv",
    "solution_quality": "FA-vs-EFA-solutionQuality-comparison.csv",
    "solution_quality_summary": "FA-vs-EFA-solutionQuality-summary.csv",
    "barangay_solution_quality": "FA-vs-EFA-barangay-solutionQuality-comparison.csv",
}

# Full paths to data files
DATA_PATHS = {
    key: os.path.join(COMPARISON_DIR, filename) for key, filename in DATA_FILES.items()
}

# ==================== STYLE FILES ====================

FONT_PATH = os.path.join(STYLES_DIR, "fonts", "GeistMono-Regular.ttf")
STYLE_PATH = os.path.join(STYLES_DIR, "themes", "rose-pine-dawn.mplstyle")

# ==================== PLOT COLORS ====================

COLORS = {
    "fa": "#1f77b4",  # Blue
    "efa": "#ff7f0e",  # Orange
}

# ==================== COLUMN NAMES ====================

# Column names in CSV files
COLUMNS = {
    "time": {
        "fa": "FA (Execution Time (ms))",
        "efa": "EFA (Execution Time (ms))",
    },
    "fitness": {
        "fa": "FA (Fitness Score)",
        "efa": "EFA (Fitness Score)",
    },
    "memory": {
        "fa": "FA (Memory Usage (bytes))",
        "efa": "EFA (Memory Usage (bytes))",
    },
    "objectives": {
        "objective1": {"fa": "Objective1_FA", "efa": "Objective1_EFA"},
        "objective2": {"fa": "Objective2_FA", "efa": "Objective2_EFA"},
        "objective3": {"fa": "Objective3_FA", "efa": "Objective3_EFA"},
        "objective4": {"fa": "Objective4_FA", "efa": "Objective4_EFA"},
        "objective5": {"fa": "Objective5_FA", "efa": "Objective5_EFA"},
    },
    "solution_quality": {
        "fa": "FA (Solution Quality)",
        "efa": "EFA (Solution Quality)",
    },
    "barangay_solution_quality": {
        "scenario": "Scenario",
        "barangay_id": "Barangay_ID",
        "barangay_name": "Barangay_Name",
        "hazard_level": "Hazard_Level",
        "fa_allocated": "FA_Allocated",
        "fa_required": "FA_Required",
        "efa_allocated": "EFA_Allocated",
        "efa_required": "EFA_Required",
        "fa_score": "FA_Score",
        "efa_score": "EFA_Score",
        "percentage_change": "Percentage_Change",
    },
}

# ==================== OUTPUT FILE NAMES ====================

OUTPUT_FILES = {
    "time_comparison": "time_comparison.png",
    "mean_time_comparison": "mean_time_comparison.png",
    "fitness_comparison": "fitness_comparison.png",
    "mean_fitness_comparison": "mean_fitness_comparison.png",
    "memory_comparison": "memory_comparison.png",
    "mean_memory_comparison": "mean_memory_comparison.png",
    "results": "results.txt",
    "boxplot_stats": "boxplot_statistics.txt",
    # Objective-specific outputs
    "objective_comparison": "objective_{}_comparison.png",
    "mean_objective_comparison": "mean_objective_{}_comparison.png",
    # Solution Quality outputs
    "solution_quality_comparison": "solution_quality_comparison.png",
    "mean_solution_quality_comparison": "mean_solution_quality_comparison.png",
    # Barangay analysis outputs
    "barangay_improvement_histogram": "barangay_improvement_histogram.png",
    "barangay_hazard_boxplot": "barangay_hazard_boxplot.png",
    "barangay_summary_bars": "barangay_summary_bars.png",
    "barangay_top_performers": "barangay_top_performers.png",
    "barangay_analysis_results": "barangay_analysis_results.txt",
    # Scenario-specific outputs
    "scenario_detail": "scenario_{:02d}_barangay_detail.png",
}

# ==================== STATISTICAL SETTINGS ====================

STATISTICAL_SETTINGS = {
    "alpha": 0.01,  # Significance level
}

# ==================== OBJECTIVE SETTINGS ====================

OBJECTIVE_SETTINGS = {
    "num_objectives": 5,
    "y_limits": (0, 1),  # Y-axis range for objective plots
    "objective_names": {
        1: "Objective 1",
        2: "Objective 2",
        3: "Objective 3",
        4: "Objective 4",
        5: "Objective 5",
    },
    "objective_descriptions": {
        1: "Coverage Score",
        2: "Prioritization Fulfillment",
        3: "Distribution Imbalance Penalty",
        4: "Demand Satisfaction",
        5: "Displaced Population Index",
    },
}

# ==================== SOLUTION QUALITY SETTINGS ====================

SOLUTION_QUALITY_SETTINGS = {
    # Scenario detail generation settings
    "generate_all_scenarios": True,  # Generate all scenarios or only selected ones
    "selected_scenarios": [1, 15, 30],  # Used if generate_all_scenarios=False
    "figure_height_per_barangay": 0.2,  # Inches per barangay in scenario charts
    "min_scenario_figure_height": 20,  # Minimum height for scenario charts
    "sort_barangays_by": "hazard_level",  # Options: hazard_level, improvement, name
    "show_barangay_names": True,  # Show full names or just IDs
    # Top/bottom performer settings
    "top_n_performers": 10,  # Number of top/bottom barangays to highlight
}

# ==================== HELPER FUNCTIONS ====================


def get_data_path(data_type):
    """
    Get the full path to a data file.

    Parameters:
    -----------
    data_type : str
        Type of data ('time', 'fitness', 'memory', 'objectives', 'solution_quality', etc.)

    Returns:
    --------
    str
        Full path to the data file
    """
    if data_type not in DATA_PATHS:
        raise ValueError(
            f"Unknown data type: {data_type}. Available: {list(DATA_PATHS.keys())}"
        )
    return DATA_PATHS[data_type]


def get_output_dir(sop_name, subfolder=None):
    """
    Get the output directory path and create it if it doesn't exist.

    Parameters:
    -----------
    sop_name : str
        Name of the SOP ('sop1', 'sop2', 'sop3', 'sop4', 'objectives')
    subfolder : str, optional
        Subfolder name within the SOP directory (e.g., 'time', 'fitness', 'memory')

    Returns:
    --------
    str
        Full path to the output directory
    """
    if sop_name not in OUTPUT_DIRS:
        # If custom name, create it under results
        output_dir = os.path.join(RESULTS_DIR, sop_name)
    else:
        output_dir = OUTPUT_DIRS[sop_name]

    # Add subfolder if specified
    if subfolder:
        output_dir = os.path.join(output_dir, subfolder)

    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def get_columns(data_type):
    """
    Get the column names for a specific data type.

    Parameters:
    -----------
    data_type : str
        Type of data ('time', 'fitness', 'memory', 'objectives', 'solution_quality', etc.)

    Returns:
    --------
    dict
        Dictionary with column names
    """
    if data_type not in COLUMNS:
        raise ValueError(
            f"Unknown data type: {data_type}. Available: {list(COLUMNS.keys())}"
        )
    return COLUMNS[data_type]
