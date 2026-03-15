import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("Loading data...")
df = pd.read_csv("data/nyt_headlines_scored_v2.csv", low_memory=False)
print("Columns:", df.columns.tolist())
print("Shape:", df.shape)

score_col = "happiness_score"

if "year" in df.columns:
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
elif "pub_date" in df.columns:
    df["year"] = pd.to_datetime(df["pub_date"], errors="coerce").dt.year
else:
    raise ValueError("No 'year' or 'pub_date' column found.")

df[score_col] = pd.to_numeric(df[score_col], errors="coerce")
df = df.dropna(subset=["year", score_col]).copy()
print("After dropping missing year/score:", df.shape)

def assign_decade(year):
    if 2000 <= year <= 2009:
        return "2000s"
    elif 2010 <= year <= 2019:
        return "2010s"
    elif 2020 <= year <= 2024:
        return "2020s"
    return np.nan

df["decade"] = df["year"].apply(assign_decade)
df = df.dropna(subset=["decade"]).copy()

print("Counts by decade:")
print(df["decade"].value_counts())

sample_size = df["decade"].value_counts().min()
print("Sample size per decade:", sample_size)

sampled_df = (
    df.groupby("decade", group_keys=False)
    .sample(n=sample_size, random_state=42)
    .reset_index(drop=True)
)


if "decade" not in sampled_df.columns:
    sampled_df["decade"] = df.loc[sampled_df.index, "decade"].values

def bootstrap_ci(data, n_boot=1000, ci=95):
    data = np.array(data)
    boot_means = []
    for _ in range(n_boot):
        sample = np.random.choice(data, size=len(data), replace=True)
        boot_means.append(np.mean(sample))
    lower = np.percentile(boot_means, (100 - ci) / 2)
    upper = np.percentile(boot_means, 100 - (100 - ci) / 2)
    return np.mean(data), lower, upper, boot_means

results = []
bootstrap_distributions = {}

for decade in ["2000s", "2010s", "2020s"]:
    scores = sampled_df.loc[sampled_df["decade"] == decade, score_col]
    mean_score, ci_lower, ci_upper, boot_means = bootstrap_ci(scores)

    results.append({
        "decade": decade,
        "mean_happiness": mean_score,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "n": len(scores)
    })

    bootstrap_distributions[decade] = boot_means

results_df = pd.DataFrame(results)
print(results_df)

results_df.to_csv("tables/decade_happiness_summary.csv", index=False)
print("Saved tables/decade_happiness_summary.csv")

plt.figure(figsize=(8, 5))

means = results_df["mean_happiness"]
lower_errors = results_df["mean_happiness"] - results_df["ci_lower"]
upper_errors = results_df["ci_upper"] - results_df["mean_happiness"]

x = range(len(results_df))

plt.errorbar(
    x,
    means,
    yerr=[lower_errors, upper_errors],
    fmt="o",
    capsize=5
)

plt.xticks(x, results_df["decade"])


ymin = results_df["ci_lower"].min() - 0.02
ymax = results_df["ci_upper"].max() + 0.02
plt.ylim(ymin, ymax)


for i, v in enumerate(means):
    plt.text(i, v + 0.002, f"{v:.3f}", ha="center")

plt.title("Average Happiness of NYT Headlines by Decade")
plt.xlabel("Decade")
plt.ylabel("Mean Happiness Score")

plt.tight_layout()
plt.savefig("figures/happiness_by_decade_ci.png", dpi=300)
plt.close()
print("Saved figures/happiness_by_decade_ci.png")

for decade, boot_means in bootstrap_distributions.items():
    plt.figure(figsize=(8, 5))
    plt.hist(boot_means, bins=30)
    plt.title(f"Bootstrap Distribution of Mean Happiness ({decade})")
    plt.xlabel("Bootstrapped Mean Happiness")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(f"figures/bootstrap_distribution_{decade}.png", dpi=300)
    plt.close()
    print(f"Saved figures/bootstrap_distribution_{decade}.png")