# FA vs EFA Data Analysis & Results

Quick analysis tool to compare Firefly Algorithm (FA) vs Enhanced Firefly Algorithm (EFA) performance and perform statistical analysis.

## Setup

### 1. Clone the project

```bash
git clone https://github.com/CS-4-3-Group-4/ThesisAnalysisResults.git
cd ThesisAnalysisResults
```

### 2. Create and activate virtual environment

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Usage

Run the interactive CLI to select and run analyses:

```bash
python main.py
```

### 4. Update dependencies

```bash
pip freeze > requirements.txt
```

The tool provides two analysis categories:

### 📊 Percentage Change Analysis (SOP 1 & 2)

-   Fitness Score % Change (SOP 1)
-   Execution Time % Change (SOP 2)
-   Memory Usage % Change (SOP 2)

### 📈 Statistical Significance Testing (SOP 3 & 4)

-   Fitness Score Significance Test (SOP 3)
-   Execution Time Significance Test (SOP 4)
-   Memory Usage Significance Test (SOP 4)

## Input Data

Place your CSV files in the `comparison/` folder with the following structure:

```
comparison/
├── FA-vs-EFA-fitness-comparison.csv
├── FA-vs-EFA-executionTime-comparison.csv
└── FA-vs-EFA-memory-comparison.csv
```

## Output

Results are saved in the `results/` directory:

```
results/
├── sop1/                          # Fitness analysis
│   ├── fitness_comparison.png
│   ├── mean_fitness_comparison.png
│   └── results.txt
├── sop2/
│   ├── time/                      # Time analysis
│   │   ├── time_comparison.png
│   │   ├── mean_time_comparison.png
│   │   └── results.txt
│   └── memory/                    # Memory analysis
│       ├── memory_comparison.png
│       ├── mean_memory_comparison.png
│       └── results.txt
├── sop3/                          # Fitness significance test
│   ├── fitness_boxplot.png
│   ├── boxplot_statistics.txt
│   └── results.txt
└── sop4/
    ├── time/                      # Execution time significance test
    │   ├── time_boxplot.png
    │   ├── boxplot_statistics.txt
    │   └── results.txt
    └── memory/                    # Memory usage significance test
        ├── memory_boxplot.png
        ├── boxplot_statistics.txt
        └── results.txt
```

## Project Structure

```

project/
├── main.py # Interactive CLI entry point
├── config.py # Configuration settings
├── percentage_change/ # SOP 1 & 2 analyses
│ ├── **init**.py
│ ├── fitness.py
│ ├── time.py
│ └── memory.py
├── significance/ # SOP 3 & 4 analyses
│ ├── **init**.py
│ ├── fitness.py
│ ├── time.py
│ └── memory.py
├── comparison/ # Input CSV files
├── results/ # Output graphs and results
├── styles/ # Matplotlib styling
│ ├── fonts/
│ │ └── GeistMono-Regular.ttf
│ └── themes/
│ ├── rose-pine-dawn.mplstyle
│ └── rose-pine.mplstyle
└── requirements.txt

```

## That's it!

When done, deactivate the virtual environment:

```bash
deactivate
```
