import pandas as pd

df = pd.read_csv("data/nyt_headlines_labeled.csv")

print("Total rows:")
print(len(df))

print("\nRows per year:")
print(df["year"].value_counts())

print("\nUnique rows by headline + pub_date:")
print(df.drop_duplicates(subset=["headline", "pub_date"]).shape[0])

print("\nUnique rows per year:")
print(
    df.drop_duplicates(subset=["headline", "pub_date"])["year"].value_counts()
)