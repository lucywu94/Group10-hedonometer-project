import pandas as pd
import re

# 1. load datasets
nyt = pd.read_csv("data/nyt_headlines_labeled.csv")
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

    if len(scores) == 0:
        return None

    return round(sum(scores) / len(scores),2)


# 5. apply to dataset
nyt["happiness_score"] = nyt["headline"].apply(compute_happiness)

print("Happiness scores computed.")

# 6. count matched words
def count_matches(text):
    tokens = tokenize(text)
    return sum(1 for word in tokens if word in word_scores)

nyt["matched_words"] = nyt["headline"].apply(count_matches)

def count_total_words(text):
    return len(tokenize(text))

nyt["total_words"] = nyt["headline"].apply(count_total_words)
nyt["coverage_ratio"] = (nyt["matched_words"] / nyt["total_words"]).round(1)
print("\nCurrent columns before saving:")
print(nyt.columns.tolist())


# 7. save result
nyt.to_csv("data/nyt_headlines_scored_v2.csv", index=False)

print("Saved file: data/nyt_headlines_scored_v2.csv")

# preview
print(nyt[["headline", "year", "happiness_score", "matched_words"]].head())

print("\nAverage happiness by year:")
print(nyt.groupby("year")["happiness_score"].mean())


print("\nCOLUMNS:")
print(nyt.columns.tolist())

print("\nHEAD PREVIEW:")
print(nyt[["headline", "year", "happiness_score", "matched_words", "total_words", "coverage_ratio"]].head())
