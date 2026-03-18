import requests
import random
import time
import csv

API_KEY = "By2bafdhKiAcA0RTDtESL7Wbt4r0J8Tca0wxdQPCy9Ln34Sg"

def fetch_month(year, month):
    url = f"https://api.nytimes.com/svc/archive/v1/{year}/{month}.json"
    params = {"api-key": API_KEY}

    response = requests.get(url, params=params, timeout=30)

    if response.status_code == 429: # if there is an error (rate limit quota violation)
        print(f"Rate limit hit at {year}-{month:02d}, sleeping...")
        time.sleep(60)  # rest for 60 secs
        return fetch_month(year, month)  # try the same month again

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
    
    # random sampling
    if len(headlines) > sample_size:
        headlines = random.sample(headlines, sample_size)
    
    return headlines


# period
periods = [
    ("After", 2009, 7, 2011, 6)
]


# save CSV
with open("Group10-hedonometer-project/data/nyt_after.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["period", "year", "month", "headline", "pub_date"])

    for period_name, start_y, start_m, end_y, end_m in periods:
        year = start_y
        month = start_m

        while (year < end_y) or (year == end_y and month <= end_m):
            print(f"Fetching {year}-{month:02d}...")

            docs = fetch_month(year, month)
            sampled = sample_headlines(docs, 500)

            for headline, pub_date in sampled:
                writer.writerow([period_name, year, month, headline, pub_date])

            # next month
            month += 1
            if month > 12:
                month = 1
                year += 1

            time.sleep(10)  

print("DONE")