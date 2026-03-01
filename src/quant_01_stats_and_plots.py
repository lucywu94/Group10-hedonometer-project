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


