import csv

input_file = "data/nyt_headlines_all.csv"
output_file = "data/nyt_headlines_labeled.csv"

with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", newline="", encoding="utf-8") as outfile:
    reader = csv.DictReader(infile)
    fieldnames = ["headline", "pub_date", "year"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)

    writer.writeheader()

    for row in reader:
        pub_date = row["pub_date"]
        year = pub_date[:4]
        writer.writerow({
            "headline": row["headline"],
            "pub_date": pub_date,
            "year": year
        })

print("Labeled file created successfully.")