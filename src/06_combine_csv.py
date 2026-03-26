import pandas as pd

before = pd.read_csv("Group10-hedonometer-project/data/nyt_before.csv")
during = pd.read_csv("Group10-hedonometer-project/data/nyt_during.csv")
after = pd.read_csv("Group10-hedonometer-project/data/nyt_after.csv")

df = pd.concat([before, during, after], ignore_index=True)

df.to_csv("Group10-hedonometer-project/data/nyt_all_periods.csv", index=False)