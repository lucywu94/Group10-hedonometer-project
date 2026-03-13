import pandas as pd
import matplotlib.pyplot as plt

# load dataset (adjust filename if needed)
df = pd.read_csv(
    "data/raw/Data_Set_S1.txt",
    sep="\t",
    skiprows=3,
    na_values="--"
)

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

# plot 1: histogram
plt.figure()
df["happiness_average"].hist(bins=40)
plt.title("Distribution of Happiness Scores")
plt.xlabel("Happiness average")
plt.ylabel("Number of words")
plt.tight_layout()
plt.savefig("figures/hist_happiness_average.png")
plt.close()

# plot 2: scatter
plt.figure()
plt.scatter(
    df["happiness_average"],
    df["happiness_standard_deviation"],
    s=10,
    alpha=0.5
)
plt.title("Happiness Average vs Disagreement")
plt.xlabel("Happiness average")
plt.ylabel("Happiness standard deviation")
plt.tight_layout()
plt.savefig("figures/scatter_avg_vs_sd.png")
plt.close()


# -------------------------
# 2.3 Corpus comparison
# -------------------------

rank_cols = {
    "Twitter": "twitter_rank",
    "Google Books": "google_rank",
    "NYT": "nyt_rank",
    "Lyrics": "lyrics_rank",
}

# 2.3-1) Count how many words appear in each corpus top 5000 (rank not missing)
presence_counts = {}
for corpus, col in rank_cols.items():
    presence_counts[corpus] = df[col].notna().sum()

counts_df = (
    pd.DataFrame({"corpus": list(presence_counts.keys()),
                  "n_words_in_top5000": list(presence_counts.values())})
    .sort_values("n_words_in_top5000", ascending=False)
)

print("\n2.3 — Words present in top 5000 by corpus:")
print(counts_df.to_string(index=False))

# 2.3-2) Simple overlap counts (examples)
twitter_present = df[rank_cols["Twitter"]].notna()
google_present = df[rank_cols["Google Books"]].notna()
nyt_present = df[rank_cols["NYT"]].notna()
lyrics_present = df[rank_cols["Lyrics"]].notna()

overlap_twitter_nyt = (twitter_present & nyt_present).sum()
overlap_all_four = (twitter_present & google_present & nyt_present & lyrics_present).sum()

print("\n2.3 — Overlap counts:")
print("Twitter & NYT:", int(overlap_twitter_nyt))
print("All four corpora:", int(overlap_all_four))

# 2.3-3) Plot: bar chart of presence counts
plt.figure()
plt.bar(counts_df["corpus"], counts_df["n_words_in_top5000"])
plt.title("How many labMT words appear in each corpus top 5000")
plt.xlabel("Corpus")
plt.ylabel("Number of words (rank present)")
plt.tight_layout()
plt.savefig("figures/bar_corpus_presence.png")
plt.close()

# Example word: common in one corpus but missing in another
# (pick one automatically: in Twitter top 5000 but missing in NYT)
example = df.loc[twitter_present & ~nyt_present, "word"].head(1).tolist()
if example:
    print("\nExample word present in Twitter but missing in NYT:", example[0])

