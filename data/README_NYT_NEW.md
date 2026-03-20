# Data Acquisition and Dataset Preparation

Our research question for this project is: *How did the emotional tone of New York Times headlines change before, during, and after the 2008 financial crisis?* To address this question, we constructed a dataset of New York Times headlines that could later be analyzed using the Hedonometer (labMT) word list. 

## Data Source

The headline data was collected from the New York Times Archive API. The Archive API provides article metadata on a monthly basis, making it particularly suitable for collecting large volumes of articles across specific time periods. After obtaining an API key from the New York Times Developer portal, the connection was first tested using small requests to ensure that the key and request structure were functioning correctly.

Once the API connection was verified, data collection was automated using a Python script (`nyt_headlines.py`). This script uses the `requests` library to retrieve monthly archive data and extract the relevant fields from the returned JSON structure. For each article, the script extracts the main headline (`headline.main`) and the publication date (`pub_date`). The extracted data is then written to CSV files for further processing.

To run this script, you must obtain your own New York Times API key from the NYT Developer Portal and replace "YOUR_API_KEY" in the script. The script uses the NYT Archive API to retrieve article data. For security reasons, API keys are not included in this repository.

## Data Collection Process

The data collection process was carried out month-by-month across three defined periods surrounding the 2008 financial crisis. The crisis period was defined as September 2008 to June 2009, corresponding to the period following the collapse of Lehman Brothers. To enable a balanced comparison, two 24-month windows were defined before and after the crisis period.

The final time ranges are summarized below:

| Period | Time Range          | Duration  |
| ------ | ------------------- | --------- |
| Before | Sep 2006 – Aug 2008 | 24 months |
| During | Sep 2008 – Jun 2009 | 10 months |
| After  | Jul 2009 – Jun 2011 | 24 months |

For each month within these periods, all available headlines were retrieved via the API. From this pool, a random sample of up to 500 headlines per month was selected. Sampling was performed independently for each month in order to maintain temporal consistency across the dataset.

Because the NYT API imposes rate limits, requests were spaced using time delays, and retry logic was implemented to handle temporary quota violations. When a rate limit error occurred, the script paused and retried the same request to ensure that no monthly data was skipped. The collection process was first tested on a small subset of months to ensure that API calls, parsing, and file writing were functioning correctly before running the full data acquisition.

## Dataset Construction

All datasets included in this repository are processed data rather than raw data. The original data was obtained from the New York Times Archive API in structured JSON format, but during collection, the data was transformed by selecting relevant fields, applying random sampling, and assigning period labels. As a result, the repository does not contain raw API outputs, but instead provides structured datasets prepared for analysis.

The collected data for each period was initially stored in separate CSV files (`nyt_before.csv`, `nyt_during.csv`, and `nyt_after.csv`). These files were then combined into a single dataset (`nyt_all_periods.csv`) containing all sampled headlines across the three periods.

Each row in the dataset includes the headline text, publication date, and corresponding time period (Before, During, After), along with the year and month of publication. This structure allows for straightforward grouping and comparison across time.

Below is an example row from the dataset:
```
period,year,month,headline,pub_date
After,2011,4,Woman Killed When Cab Crashes Into Bronx Store,2011-04-22T02:37:22+0000
```

## Duplicate Handling

During the dataset preparation stage, duplicate entries were identified and examined. Duplicates were defined as rows with identical headline text and identical publication date, which indicates that the same article was included more than once during the collection or merging process.

A total of 88 exact duplicate rows were identified in the combined dataset. These duplicates were removed to produce a cleaned dataset (`nyt_all_periods_clean.csv`). Importantly, headlines that appeared multiple times on different dates were retained, as these represent valid and distinct observations in the dataset.

After duplicate removal, some months contain slightly fewer than 500 headlines. This is expected and reflects the elimination of repeated entries rather than a loss of unique data.

## Data Validation

Basic validation checks were performed to ensure the integrity of the dataset. This included verifying the number of headlines collected per month and confirming that the data was correctly labeled by period. The dataset was also inspected for structural consistency after merging and cleaning.

The final cleaned dataset contains approximately 28,900 headlines sampled across all periods. A summary of the dataset is shown below:

| Metric                    | Value     |
| ------------------------- | --------- |
| Total headlines (cleaned) | 28,934   |
| Sampling size per month   | Up to 500 |
| Duplicate rows removed    | 88        |
| Number of periods         | 3         |

## Final Dataset

The final dataset used for analysis is stored as:

data/nyt_economic_crisis/nyt_all_periods_clean.csv

This dataset forms the basis for the next stage of the project, where the emotional tone of headlines will be measured using the Hedonometer word list and compared across different phases of the financial crisis.
