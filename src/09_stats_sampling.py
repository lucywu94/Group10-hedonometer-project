import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

DATA_PATH = "data/nyt_economic_crisis/nyt_all_periods_scored.csv"
SCORE_COL = "happiness_score"
MONTHLY_N = 500
N_BOOT = 1000
RANDOM_SEED = 42

os.makedirs("tables", exist_ok=True)
os.makedirs("figures", exist_ok=True)

print("Loading data...")
df = pd.read_csv(DATA_PATH, low_memory=False)
print("Columns:", df.columns.tolist())
print("Shape:", df.shape)

df["year"] = pd.to_numeric(df["year"], errors="coerce")
df["month"] = pd.to_numeric(df["month"], errors="coerce")
df[SCORE_COL] = pd.to_numeric(df[SCORE_COL], errors="coerce")


df = df.dropna(subset=["period", "year", "month", SCORE_COL]).copy()


df["period"] = df["period"].astype(str).str.strip().str.title()

valid_periods = ["Before", "During", "After"]
df = df[df["period"].isin(valid_periods)].copy()


n_dupes = df.duplicated().sum()
print(f"Exact duplicate rows: {n_dupes}")
df = df.drop_duplicates().copy()
print("Rows after removing exact duplicates:", len(df))

print("After dropping missing period/year/month/score:", df.shape)
print("\nCounts by period:")
print(df["period"].value_counts())

def sample_month(group: pd.DataFrame) -> pd.DataFrame:
    n = min(len(group), MONTHLY_N)
    sampled = group.sample(n=n, random_state=RANDOM_SEED).copy()
    sampled["period"] = group.name[0]
    sampled["year"] = group.name[1]
    sampled["month"] = group.name[2]
    return sampled

sampled_df = (
    df.groupby(["period", "year", "month"], group_keys=False)
      .apply(sample_month)
      .reset_index(drop=True)
)

print("\nSampled data shape:", sampled_df.shape)

monthly_counts = (
    sampled_df.groupby(["period", "year", "month"])
    .size()
    .reset_index(name="n")
    .sort_values(["year", "month"])
    .reset_index(drop=True)
)

print("\nMonthly sample counts:")
print(monthly_counts)

monthly_counts.to_csv("tables/monthly_sample_counts.csv", index=False)
print("Saved tables/monthly_sample_counts.csv")


monthly_summary = (
    sampled_df.groupby(["period", "year", "month"])
    .agg(
        n=(SCORE_COL, "size"),
        mean_happiness=(SCORE_COL, "mean"),
        median_happiness=(SCORE_COL, "median"),
        sd_happiness=(SCORE_COL, "std"),
        min_happiness=(SCORE_COL, "min"),
        max_happiness=(SCORE_COL, "max"),
    )
    .reset_index()
    .sort_values(["year", "month"])
    .reset_index(drop=True)
)
monthly_summary["time_index"] = range(len(monthly_summary))

r, p_value = pearsonr(
    monthly_summary["time_index"],
    monthly_summary["mean_happiness"]
)

print("\nPearson correlation results:")
print(f"Pearson r: {r:.6f}")
print(f"p-value: {p_value:.6f}")

monthly_summary.to_csv("tables/monthly_happiness_summary.csv", index=False)
print("Saved tables/monthly_happiness_summary.csv")


def bootstrap_mean_ci(data, n_boot=1000, ci=95, seed=42):
    rng = np.random.default_rng(seed)
    data = np.asarray(data, dtype=float)
    data = data[~np.isnan(data)]

    if len(data) == 0:
        return np.nan, np.nan, np.nan, np.array([])

    boot_means = np.empty(n_boot)
    for i in range(n_boot):
        sample = rng.choice(data, size=len(data), replace=True)
        boot_means[i] = np.mean(sample)

    alpha = (100 - ci) / 2
    lower = np.percentile(boot_means, alpha)
    upper = np.percentile(boot_means, 100 - alpha)

    return np.mean(data), lower, upper, boot_means


def bootstrap_difference(a, b, n_boot=1000, ci=95, seed=42):
    rng = np.random.default_rng(seed)
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)

    a = a[~np.isnan(a)]
    b = b[~np.isnan(b)]

    if len(a) == 0 or len(b) == 0:
        return np.nan, np.nan, np.nan, np.array([]), np.nan

    boot_diffs = np.empty(n_boot)
    for i in range(n_boot):
        a_sample = rng.choice(a, size=len(a), replace=True)
        b_sample = rng.choice(b, size=len(b), replace=True)
        boot_diffs[i] = np.mean(a_sample) - np.mean(b_sample)

    alpha = (100 - ci) / 2
    lower = np.percentile(boot_diffs, alpha)
    upper = np.percentile(boot_diffs, 100 - alpha)

    prop_gt_zero = np.mean(boot_diffs > 0)

    return np.mean(a) - np.mean(b), lower, upper, boot_diffs, prop_gt_zero

def bootstrap_correlation(x, y, n_boot=1000, ci=95, seed=42):
    rng = np.random.default_rng(seed)
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    valid = ~(np.isnan(x) | np.isnan(y))
    x = x[valid]
    y = y[valid]

    if len(x) == 0 or len(y) == 0:
        return np.nan, np.nan, np.nan, np.array([]), np.nan

    boot_rs = np.empty(n_boot)

    for i in range(n_boot):
        idx = rng.choice(len(x), size=len(x), replace=True)
        r_boot, _ = pearsonr(x[idx], y[idx])
        boot_rs[i] = r_boot

    alpha = (100 - ci) / 2
    lower = np.percentile(boot_rs, alpha)
    upper = np.percentile(boot_rs, 100 - alpha)

    prop_negative = np.mean(boot_rs < 0)

    return pearsonr(x, y)[0], lower, upper, boot_rs, prop_negative

r_obs, r_lower, r_upper, r_dist, prop_negative = bootstrap_correlation(
    monthly_summary["time_index"],
    monthly_summary["mean_happiness"],
    n_boot=N_BOOT,
    ci=95,
    seed=RANDOM_SEED
)

correlation_summary = pd.DataFrame([{
    "pearson_r": r_obs,
    "ci_lower": r_lower,
    "ci_upper": r_upper,
    "prop_negative": prop_negative
}])

correlation_summary.to_csv("tables/pearson_correlation_summary.csv", index=False)

print("\nBootstrap correlation summary:")
print(correlation_summary)
print("Saved tables/pearson_correlation_summary.csv")



period_results = []
bootstrap_means_by_period = {}

for period in valid_periods:
    scores = sampled_df.loc[sampled_df["period"] == period, SCORE_COL].dropna()
    mean_score, ci_lower, ci_upper, boot_means = bootstrap_mean_ci(
        scores, n_boot=N_BOOT, ci=95, seed=RANDOM_SEED
    )

    period_results.append({
        "period": period,
        "mean_happiness": mean_score,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "n": len(scores)
    })

    bootstrap_means_by_period[period] = boot_means

period_results_df = pd.DataFrame(period_results)
period_results_df.to_csv("tables/period_happiness_summary.csv", index=False)
print("\nPeriod summary:")
print(period_results_df)
print("Saved tables/period_happiness_summary.csv")


comparisons = [
    ("Before", "During"),
    ("During", "After"),
    ("Before", "After"),
]

diff_results = []
bootstrap_diffs = {}

for a_label, b_label in comparisons:
    a_scores = sampled_df.loc[sampled_df["period"] == a_label, SCORE_COL].dropna()
    b_scores = sampled_df.loc[sampled_df["period"] == b_label, SCORE_COL].dropna()

    diff_mean, ci_lower, ci_upper, boot_diffs_arr, prop_gt_zero = bootstrap_difference(
        a_scores, b_scores, n_boot=N_BOOT, ci=95, seed=RANDOM_SEED
    )

    comparison_name = f"{a_label} - {b_label}"
    diff_results.append({
        "comparison": comparison_name,
        "mean_difference": diff_mean,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "prop_gt_zero": prop_gt_zero
    })

    bootstrap_diffs[comparison_name] = boot_diffs_arr

diff_results_df = pd.DataFrame(diff_results)
diff_results_df.to_csv("tables/period_difference_summary.csv", index=False)
print("\nDifference summary:")
print(diff_results_df)
print("Saved tables/period_difference_summary.csv")


plt.figure(figsize=(8, 5), dpi=300)

x = period_results_df["period"]
means = period_results_df["mean_happiness"]
lower = period_results_df["ci_lower"]
upper = period_results_df["ci_upper"]

plt.bar(x, means)
plt.errorbar(
    x,
    means,
    yerr=[means - lower, upper - means],
    fmt="none",
    capsize=5
)

for i, v in enumerate(means):
    plt.text(
        i,
        v + 0.002,
        f"{v:.3f}",
        ha="center",
        fontsize=10,
        fontweight="bold",
        bbox=dict(facecolor="white", edgecolor="none", alpha=0.8)
    )

plt.title("Average Happiness of NYT Headlines by Crisis Period")
plt.xlabel("Period")
plt.ylabel("Mean Happiness Score")
plt.tight_layout()
plt.savefig("figures/happiness_by_period_ci.png", dpi=300)
plt.close()
print("Saved figures/happiness_by_period_ci.png")


filename_map = {
    "Before - During": "figures/bootstrap_diff_before_during.png",
    "During - After": "figures/bootstrap_diff_during_after.png",
    "Before - After": "figures/bootstrap_diff_before_after.png",
}

for comparison_name, diffs in bootstrap_diffs.items():
    if len(diffs) == 0:
        continue

    plt.figure(figsize=(8, 5), dpi=300)
    plt.hist(diffs, bins=30)
    plt.axvline(0, linestyle="--", linewidth=1)
    plt.title(f"Bootstrap Distribution of Mean Difference: {comparison_name}")
    plt.xlabel("Bootstrapped Mean Difference")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(filename_map[comparison_name], dpi=300)
    plt.close()
    print(f"Saved {filename_map[comparison_name]}")


monthly_summary["date"] = pd.to_datetime(
    dict(year=monthly_summary["year"], month=monthly_summary["month"], day=1)
)

plt.figure(figsize=(10, 5), dpi=300)
plt.plot(monthly_summary["date"], monthly_summary["mean_happiness"], marker="o")

plt.axvline(pd.Timestamp("2008-09-01"), linestyle="--", linewidth=1)
plt.axvline(pd.Timestamp("2009-07-01"), linestyle="--", linewidth=1)

plt.title("Monthly Mean Happiness of NYT Headlines")
plt.xlabel("Month")
plt.ylabel("Mean Happiness Score")
plt.tight_layout()
plt.savefig("figures/monthly_happiness_trend.png", dpi=300)
plt.close()
print("Saved figures/monthly_happiness_trend.png")
plt.figure(figsize=(8, 5), dpi=300)
plt.hist(r_dist, bins=30)
plt.axvline(0, linestyle="--", linewidth=1)
plt.axvline(r_obs, linestyle="-", linewidth=1)
plt.title("Bootstrap Distribution of Pearson Correlation")
plt.xlabel("Pearson r")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("figures/bootstrap_correlation.png", dpi=300)
plt.close()
print("Saved figures/bootstrap_correlation.png")