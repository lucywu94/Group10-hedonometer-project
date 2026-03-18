import pandas as pd

df = pd.read_csv("Group10-hedonometer-project/data/nyt_all_periods.csv")

# check number of duplicates
print("Duplicates:", df.duplicated(subset=["headline", "pub_date"]).sum())

# delete duplicates
df_clean = df.drop_duplicates(subset=["headline", "pub_date"])

# save
df_clean.to_csv("Group10-hedonometer-project/data/nyt_all_periods_clean.csv", index=False)