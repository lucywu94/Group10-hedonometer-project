import pandas as pd

nyt = pd.read_csv("data/nyt_headlines_labeled.csv")
labmt = pd.read_csv("data/labmt_clean.csv")

print("NYT columns:")
print(nyt.columns.tolist())
print(nyt.head())

print("\nlabMT columns:")
print(labmt.columns.tolist())
print(labmt.head())