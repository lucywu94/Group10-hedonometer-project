import pandas as pd
import re

# 1. load datasets
nyt = pd.read_csv("data/nyt_economic_crisis/nyt_all_periods_clean.csv")
labmt = pd.read_csv("data/labmt_clean.csv")

print("Data loaded.")

# 2. create dictionary: word -> happiness score
word_scores = dict(zip(labmt["word"], labmt["happiness_average"]))

print("Dictionary built.")

# 3. tokenizer
def tokenize(text):
    if pd.isna(text):
        return []
    text = str(text).lower()
    return re.findall(r"[a-z]+", text)

# 4. compute happiness score
def compute_happiness(text):
    tokens = tokenize(text)

    scores = []
    for word in tokens:
        if word in word_scores:
            scores.append(word_scores[word])

    # OOV words are excluded
    if len(scores) == 0:
        return None

    return round(sum(scores) / len(scores), 2)

# 5. apply to dataset
nyt["happiness_score"] = nyt["headline"].apply(compute_happiness)

print("Happiness scores computed.")

# 6. count matched words
def count_matches(text):
    tokens = tokenize(text)
    return sum(1 for word in tokens if word in word_scores)

nyt["matched_words"] = nyt["headline"].apply(count_matches)

# 7. count total words
def count_total_words(text):
    return len(tokenize(text))

nyt["total_words"] = nyt["headline"].apply(count_total_words)

# 8. compute coverage ratio
nyt["coverage_ratio"] = (nyt["matched_words"] / nyt["total_words"]).round(1)

# 9. save result
nyt.to_csv("data/nyt_economic_crisis/nyt_all_periods_scored.csv", index=False)
print("Saved file: data/nyt_economic_crisis/nyt_all_periods_scored.csv")

# 10. preview
print("\nPreview:")
print(
    nyt[
        [
            "period",
            "year",
            "headline",
            "happiness_score",
            "matched_words",
            "total_words",
            "coverage_ratio",
        ]
    ].head()
)

print("\nAverage happiness by period:")
print(nyt.groupby("period")["happiness_score"].mean())

print("\nCurrent columns:")
print(nyt.columns.tolist())