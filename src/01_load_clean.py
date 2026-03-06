import pandas as pd

file_path = "data/raw/Data_Set_S1.txt"

df = pd.read_csv(
    file_path,
    sep="\t",
    skiprows=2,      # 跳过前两行 metadata
    na_values="--"   # 自动把 -- 变成 NaN
)

print("Shape:", df.shape)
print(df.head())
print("\nData info:")
print(df.info())

print("\nMissing values per column:")
print(df.isna().sum())

print("\nDuplicated words:")
print(df["word"].duplicated().sum())

print("\nTop 10 happiest words:")
print(df.sort_values("happiness_average", ascending=False)
      [["word", "happiness_average"]].head(10))

print("\nTop 10 saddest words:")
print(df.sort_values("happiness_average")
      [["word", "happiness_average"]].head(10))
df.to_csv("data/labmt_clean.csv", index=False)
print("\nClean dataset saved.")
