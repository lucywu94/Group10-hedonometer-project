import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# make sure output folders exist
Path("figures").mkdir(exist_ok=True)
Path("tables").mkdir(exist_ok=True)

# load cleaned dataset from Section 1
df = pd.read_csv("data/labmt_clean.csv")

print("Shape:", df.shape)
print(df.columns)

# clean numeric columns
numeric_cols = [
    "happiness_average",
    "happiness_standard_deviation",
    "twitter_rank",
    "google_books_rank",
    "nyt_rank",
    "lyrics_rank",
]
# missing data
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col].replace("--", pd.NA), errors="coerce")

print(df.info())
print(df.isna().sum().sort_values(ascending=False))

# sanity checks
print("Duplicate words:", df["word"].duplicated().sum())
print(df.sample(15, random_state=0))

# descriptive statistics
stats = df["happiness_average"].describe(percentiles=[0.05, 0.95])
print(stats)

# -------------------------
# 2.1 Histogram (Distribution of Happiness Scores)
# -------------------------
plt.figure()

# histogram
df["happiness_average"].hist(bins=40)

# stats
mean_val = df["happiness_average"].mean()
median_val = df["happiness_average"].median()
std_val = df["happiness_average"].std()
p5 = df["happiness_average"].quantile(0.05)
p95 = df["happiness_average"].quantile(0.95)
min_val = df["happiness_average"].min()
max_val = df["happiness_average"].max()

# lines
plt.axvline(mean_val, color="red", linestyle="--", label=f"Mean: {mean_val:.2f}")
plt.axvline(median_val, color="blue", linestyle="-", label=f"Median: {median_val:.2f}")
plt.axvline(p5, color="green", linestyle=":", label=f"5th pct: {p5:.2f}")
plt.axvline(p95, color="green", linestyle=":", label=f"95th pct: {p95:.2f}")

# text box (std + range)
plt.text(
    0.02, 0.95,
    f"Std: {std_val:.2f}\nRange: {min_val:.2f}–{max_val:.2f}",
    transform=plt.gca().transAxes,
    verticalalignment="top"
)

plt.title("Distribution of Happiness Scores")
plt.xlabel("Happiness average")
plt.ylabel("Number of words")

plt.legend()
plt.tight_layout()
plt.savefig("figures/hist_happiness_average.png")
plt.close()

# -------------------------
# 2.2 Scatterplot (Happiness vs Disagreement)
# -------------------------
plt.figure()

# Plot all words in the dataset
plt.scatter(
    df["happiness_average"],
    df["happiness_standard_deviation"],
    s=10,
    alpha=0.3
)

plt.title("Happiness Average vs Disagreement")
plt.xlabel("Happiness average")
plt.ylabel("Happiness standard deviation")

# Select words to highlight and label
most_negative = df.loc[df["happiness_average"].idxmin()]
most_positive = df.loc[df["happiness_average"].idxmax()]
highest_disagreement = df.loc[df["happiness_standard_deviation"].idxmax()]

# Select one additional high-disagreement outlier
extra_outlier = df.sort_values(
    "happiness_standard_deviation", ascending=False
).iloc[1]

to_label = [most_negative, most_positive, highest_disagreement, extra_outlier]

# Highlight selected words in red
highlight_df = pd.DataFrame(to_label)
plt.scatter(
    highlight_df["happiness_average"],
    highlight_df["happiness_standard_deviation"],
    s=10,
    color="red",
    zorder=3
)

# Add text labels for the selected words
for row in to_label:
    x = row["happiness_average"]
    y = row["happiness_standard_deviation"]
    word = row["word"]
    plt.text(x + 0.03, y + 0.01, word, fontsize=8)

plt.tight_layout()
plt.savefig("figures/scatter_avg_vs_sd.png")
plt.close()

# -------------------------
# 2.3 Heatmap (Corpus comparison)
# -------------------------

rank_cols = {
    "Twitter": "twitter_rank",
    "Google Books": "google_rank",
    "NYT": "nyt_rank",
    "Lyrics": "lyrics_rank",
}

# 2.3-1) Simple overlap counts (examples)
twitter_present = df[rank_cols["Twitter"]].notna() & (df[rank_cols["Twitter"]] <= 5000)
google_present = df[rank_cols["Google Books"]].notna() & (df[rank_cols["Google Books"]] <= 5000)
nyt_present = df[rank_cols["NYT"]].notna() & (df[rank_cols["NYT"]] <= 5000)
lyrics_present = df[rank_cols["Lyrics"]].notna() & (df[rank_cols["Lyrics"]] <= 5000)

overlap_twitter_nyt = (twitter_present & nyt_present).sum()
overlap_all_four = (twitter_present & google_present & nyt_present & lyrics_present).sum()

print("\n2.3 — Overlap counts:")
print("Twitter & NYT:", int(overlap_twitter_nyt))
print("All four corpora:", int(overlap_all_four))

# -------------------------
# Heatmap: corpus overlap
# -------------------------

import numpy as np

tw = df["twitter_rank"].notna()
gb = df["google_rank"].notna()
nyt = df["nyt_rank"].notna()
ly = df["lyrics_rank"].notna()

corpora = {
    "Twitter": tw,
    "Google Books": gb,
    "NYT": nyt,
    "Lyrics": ly
}

names = list(corpora.keys())
n = len(names)

matrix = np.zeros((n, n))

for i, name1 in enumerate(names):
    for j, name2 in enumerate(names):
        overlap = (corpora[name1] & corpora[name2]).sum()
        matrix[i, j] = overlap

# plot heatmap
plt.figure()
plt.imshow(matrix, cmap="Blues")

plt.xticks(range(n), names, rotation=30, ha="right")
plt.yticks(range(n), names)

for i in range(n):
    for j in range(n):
        plt.text(j, i, int(matrix[i, j]),
                 ha="center", va="center", color="black")

plt.title("Overlap between corpora (top 5000 words)")
plt.colorbar(label="Number of overlapping words")

plt.tight_layout()
plt.savefig("figures/heatmap_corpus_overlap.png")
plt.close()

print("\nOverlap matrix:")
print(matrix)