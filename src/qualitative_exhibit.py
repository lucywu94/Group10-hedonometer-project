import pandas as pd
from pathlib import Path

# Correct dataset path (you confirmed this file exists)
DATASET = Path("data/raw/Data_Set_S1.txt")

if not DATASET.exists():
    raise FileNotFoundError(f"Dataset not found at: {DATASET}")

# labMT is tab-delimited
df = pd.read_csv(
    DATASET,
    sep="\t",
    skiprows=4,
    header=None,
    na_values=["--"]
)

df.columns = [
    "word",
    "rank",
    "happiness_average",
    "happiness_standard_deviation",
    "twitter_rank",
    "google_rank",
    "nyt_rank",
    "lyrics_rank",
]

# Check required columns exist
required = ["word", "happiness_average", "happiness_standard_deviation"]
missing = [c for c in required if c not in df.columns]
if missing:
    raise ValueError(f"Missing columns: {missing}\nFound columns: {list(df.columns)}")

# Clean numeric columns
df["happiness_average"] = pd.to_numeric(df["happiness_average"], errors="coerce")
df["happiness_standard_deviation"] = pd.to_numeric(df["happiness_standard_deviation"], errors="coerce")
df = df.dropna(subset=["word", "happiness_average", "happiness_standard_deviation"]).drop_duplicates(subset=["word"])

# 5 very positive
very_positive = df.sort_values("happiness_average", ascending=False).head(5).assign(category="Very positive")

# 5 very negative
very_negative = df.sort_values("happiness_average", ascending=True).head(5).assign(category="Very negative")

# 5 highly contested (highest disagreement)
contested = df.sort_values("happiness_standard_deviation", ascending=False).head(5).assign(category="Highly contested (high SD)")

# Suggestions for your weird/culturally loaded words
print("\nTop 30 highest disagreement words (for weird/culturally loaded picks):")
suggestions = df.sort_values("happiness_standard_deviation", ascending=False).head(30)[
    ["word", "happiness_average", "happiness_standard_deviation"]
]
print(suggestions.to_string(index=False))

# EDIT THESE AFTER FIRST RUN (choose 5 you can interpret)
WEIRD_WORDS = ["capitalism", "islam", "christ", "porn", "zombies"]

weird = df[df["word"].isin(WEIRD_WORDS)].copy().assign(category="Weird / culturally loaded (chosen)")
if len(weird) != 5:
    missing_weird = [w for w in WEIRD_WORDS if w not in set(weird["word"])]
    print(f"\n⚠ Your WEIRD_WORDS list didn't match 5 words. Missing: {missing_weird}")
    print("Pick 5 words from the suggestions list above and replace WEIRD_WORDS, then run again.")

# Combine all 20
exhibit = pd.concat([very_positive, very_negative, contested, weird], ignore_index=True)
exhibit = exhibit[["category", "word", "happiness_average", "happiness_standard_deviation"]]

# Save results
Path("figures").mkdir(exist_ok=True)
exhibit.to_csv("figures/word_exhibit.csv", index=False)
Path("figures/word_exhibit.md").write_text(exhibit.to_markdown(index=False), encoding="utf-8")

print("\n--- 20-word Exhibit table ---")
print(exhibit.to_markdown(index=False))
print("\nSaved: figures/word_exhibit.csv and figures/word_exhibit.md")
