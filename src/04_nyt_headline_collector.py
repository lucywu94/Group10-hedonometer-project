import csv
import time
import requests

API_KEY = "9NGpEaAxMGbhoVdWsOjb9GkwiDoARf2enjv10DkqzeSktg64"

with open("data/nyt_headlines_2020_all.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["headline", "pub_date"])

    for month in range(1, 13):  
        url = f"https://api.nytimes.com/svc/archive/v1/2020/{month}.json?api-key={API_KEY}"
        print(f"Collecting 2020-{month:02d}...")

        response = requests.get(url)
        data = response.json()

        if "response" in data and "docs" in data["response"]:
            articles = data["response"]["docs"]

            for article in articles:
                headline = article.get("headline", {}).get("main", "")
                pub_date = article.get("pub_date", "")

                if headline and pub_date:
                    writer.writerow([headline, pub_date])
        else:
            print("API error:", data)

        time.sleep(10)

print("Data collection complete.")
