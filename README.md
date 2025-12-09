# FA vs EFA Data Analysis

Quick analysis tool to compare Firefly Algorithm (FA) vs Enhanced Firefly Algorithm (EFA) performance and perform statistical analysis.

## Setup

### 1. Clone the project

```bash
git clone <your-repo-url>
cd <project-folder>
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

Run any of these scripts to generate comparison graphs:

```bash
python pc_time.py      # Execution time analysis
python pc_fitness.py   # Fitness score analysis
python pc_memory.py    # Memory usage analysis
```

## Input Data

Place your CSV files in the `comparison/` folder:

-   `FA-vs-EFA-executionTime-comparison.csv`
-   `FA-vs-EFA-fitness-comparison.csv`
-   `FA-vs-EFA-memory-comparison.csv`

## That's it!

When done, deactivate the virtual environment:

```bash
deactivate
```
