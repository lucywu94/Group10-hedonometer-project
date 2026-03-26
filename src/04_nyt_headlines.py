import requests
import random
import time
import csv

API_KEY = ("Your_API_Key")

random.seed(42)

def fetch_month(year, month):
    url = f"https://api.nytimes.com/svc/archive/v1/{year}/{month}.json"
    params = {"api-key": API_KEY}

    response = requests.get(url, params=params, timeout=30)

    if response.status_code == 429:
        print(f"Rate limit hit at {year}-{month:02d}, sleeping...")
        time.sleep(60)
        return fetch_month(year, month)

    data = response.json()

    if "response" not in data:
        print(f"Failed at {year}-{month:02d}")
        return []

    return data["response"]["docs"]


def sample_headlines(docs, sample_size=500):
    headlines = []

    for doc in docs:
        headline = doc.get("headline", {}).get("main")
        pub_date = doc.get("pub_date")

        if headline:
            headlines.append((headline, pub_date))

    if len(headlines) > sample_size:
        headlines = random.sample(headlines, sample_size)

    return headlines


def collect_period(period_name, start_y, start_m, end_y, end_m, output_file):
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["period", "year", "month", "headline", "pub_date"])

        year = start_y
        month = start_m

        while (year < end_y) or (year == end_y and month <= end_m):
            print(f"Fetching {period_name}: {year}-{month:02d}...")

            docs = fetch_month(year, month)
            sampled = sample_headlines(docs, 500)

            for headline, pub_date in sampled:
                writer.writerow([period_name, year, month, headline, pub_date])

            month += 1
            if month > 12:
                month = 1
                year += 1

            time.sleep(10)


collect_period(
    "Before", 2006, 9, 2008, 8,
    "Group10-hedonometer-project/data/nyt_before.csv"
)

collect_period(
    "During", 2008, 9, 2009, 6,
    "Group10-hedonometer-project/data/nyt_during.csv"
)

collect_period(
    "After", 2009, 7, 2011, 6,
    "Group10-hedonometer-project/data/nyt_after.csv"
)

print("DONE")