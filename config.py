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
}

# ==================== DATA FILES ====================

# Comparison data files
DATA_FILES = {
    "time": "FA-vs-EFA-executionTime-comparison.csv",
    "fitness": "FA-vs-EFA-fitness-comparison.csv",
    "memory": "FA-vs-EFA-memory-comparison.csv",
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
}

# ==================== HELPER FUNCTIONS ====================


def get_data_path(data_type):
    """
    Get the full path to a data file.

    Parameters:
    -----------
    data_type : str
        Type of data ('time', 'fitness', 'memory')

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
        Name of the SOP ('sop1', 'sop2', 'sop3', 'sop4')
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
        Type of data ('time', 'fitness', 'memory')

    Returns:
    --------
    dict
        Dictionary with 'fa' and 'efa' column names
    """
    if data_type not in COLUMNS:
        raise ValueError(
            f"Unknown data type: {data_type}. Available: {list(COLUMNS.keys())}"
        )
    return COLUMNS[data_type]
