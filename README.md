# Seminars 3 & 4 — Hedonometer (Project Folder)

This folder provides an **example project structure** (and an instructor/demo script) for the Seminars 3 & 4 group project using the **labMT 1.0** dataset (Data Set S1 from the Hedonometer paper).

It includes:
- the labMT 1.0 dataset file (`data/raw/Data_Set_S1.txt`)
- a runnable demo analysis script (`src/hedonometer_labmt_demo.py`) that produces a *typical* set of outputs aligned to the assignment
- course documents in `docs/` (original paper + paper companion + assignment + project quickstart), provided as **.pdf**

## Folder layout (course convention)

- `src/` — Python scripts you run
- `data/raw/` — input data (treat as read-only)
- `figures/` — PNG plots (embed these in your GitHub README)
- `tables/` — CSV tables/summaries (optional to embed, but useful for analysis)
- `docs/` — assignment + paper companion + quickstart handout

## Setup + run (from the project root)

### 1) Create a virtual environment

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
```

**Windows (PowerShell)**
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
```

### 2) Install dependencies
```bash
python3 -m pip install -r requirements.txt
```

### 3) Run the demo analysis
```bash
python3 src/run_analysis.py
```

### What gets generated?
After running, look in:
- `figures/` — PNG plots
- `tables/` — CSV summary tables







## Dataset
We use the labMT 1.0 dataset (Dodds et al., 2011), which includes 10,222 English words rated for happiness.

Each word has:
- An average happiness score
- A standard deviation of ratings
- Frequency ranks in four corpora:
  - Twitter
  - Google Books
  - New York Times
  - Lyrics


## Data Cleaning

The dataset was loaded as a tab-delimited file using pandas. The first two metadata rows were skipped. Missing values marked as "--" were converted to NaN.

The final dataset contains 10,222 rows and 8 columns.

We confirmed that:
- No duplicate words are present.
- All happiness-related variables are numeric.
- Rank columns contain 5,222 missing values each, indicating words not present in the top 5000 most frequent words of the respective corpus.

A cleaned dataset was saved as `data/labmt_clean.csv`.


## Data Dictionary

| Column | Type | Description | Missing Values |
|--------|------|------------|---------------|
| word | string | The English word being evaluated | 0 |
| happiness_rank | integer | Rank of the word by average happiness score (1 = happiest) | 0 |
| happiness_average | float | Mean happiness score (1–9 scale) assigned by Mechanical Turk raters | 0 |
| happiness_standard_deviation | float | Standard deviation of happiness ratings (degree of disagreement) | 0 |
| twitter_rank | float | Frequency rank of the word in Twitter (top 5000 words only) | 5222 |
| google_rank | float | Frequency rank in Google Books corpus (top 5000 words only) | 5222 |
| nyt_rank | float | Frequency rank in New York Times corpus (top 5000 words only) | 5222 |
| lyrics_rank | float | Frequency rank in song lyrics corpus (top 5000 words only) | 5222 |

The rank columns contain 5,222 missing values each. This indicates that only the top 5,000 most frequent words from each corpus were included. Words that do not appear in the top 5,000 for a given corpus are recorded as missing (NaN). These missing values therefore reflect corpus frequency thresholds rather than incomplete data collection.
