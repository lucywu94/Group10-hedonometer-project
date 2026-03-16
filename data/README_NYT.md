# Data Acquisition and Dataset Preparation

Our research question for this project is: **How has the emotional tone of New York Times headlines changed (between 2000, 2010, and 2020)?** To investigate this question, we first needed to construct a dataset of New York Times headlines that could later be analyzed using the Hedonometer (labMT) word list. My role in the project focused on **data acquisition and dataset preparation**, which included collecting headline data from the New York Times API, organizing the files, and preparing a labeled dataset for analysis.

## Data Source

The headline data was collected from the **New York Times Archive API**. The Archive API provides article metadata for each month of a given year, which makes it well suited for collecting large numbers of articles across different time periods. After obtaining an API key from the New York Times Developer portal, the API connection was first tested using small requests to confirm that the key was functioning properly.

Once the connection was verified, data collection was automated using a Python script called **`nyt_headline_collector.py`**. This script uses the `requests` library to send API requests month by month and extract the relevant fields from the JSON responses returned by the API.

For each article, the script extracted the following fields:

* **headline** (`headline.main`) – the main article headline
* **pub_date** – the article publication date

The script saved the collected data as CSV files, allowing the data to be easily inspected and processed later.

## Data Collection Process

The collection process was first tested on a small subset of the data to ensure that the API requests, parsing, and file writing were functioning correctly. Because the NYT API applies rate limits, requests were spaced using time delays to avoid exceeding the allowed quota.

For this project, headlines were collected for **three comparison years: 2000, 2010, and 2020**. These years were chosen as representative points in time across two decades. Rather than collecting every year within each decade, selecting one year from each period allowed us to observe long-term changes while keeping the dataset manageable.

During the data acquisition stage, the API returned article data month by month. These monthly results were written to CSV files and later combined into yearly datasets. After collecting the data for each target year, the yearly files were merged into a single dataset containing headlines from all three years.

## Dataset Size and Balancing

After the data collection process was completed, we examined the number of headlines available for each year. The datasets were not identical in size, largely due to API limitations and variations in the available data returned by the archive endpoint.

The number of collected headlines for each year was approximately:

| Year | Number of Headlines |
| ---- | ------------------- |
| 2000 | ~102,800            |
| 2010 | ~112,440            |
| 2020 | **55,421**          |

Because our research question involves comparing emotional tone across years, it is important that each year contributes a similar amount of data. If one year contained significantly more headlines than another, the analysis results could be biased toward that larger dataset.

To ensure a fair comparison, we standardized the dataset size across all three years. Since **2020 contained the smallest number of headlines (55,421)**, we used this number as the reference value. For the years 2000 and 2010, which originally contained larger datasets, we will use only **55,421 headlines from each year** in the analysis. This ensures that all three time periods contribute an equal number of observations.

Balancing the dataset in this way prevents one year from disproportionately influencing the overall sentiment measurements.

## Creating the Labeled Dataset

In addition to balancing the dataset, we created a **labeled version of the dataset** to support later analysis steps. The initial collected files contained only the headline text and publication date. However, in order to compare the emotional tone of headlines across years, it is necessary to explicitly identify which year each headline belongs to.

To accomplish this, an additional column called **`year`** was added to the dataset using the script **`add_year_column.py`**. This script extracts the year from the publication date and assigns it to a new column.

The final labeled dataset contains three columns:

| Column   | Description                                                |
| -------- | ---------------------------------------------------------- |
| headline | The New York Times article headline                        |
| pub_date | The publication date of the article                        |
| year     | The labeled year used for comparison (2000, 2010, or 2020) |

Below is an example row from the labeled dataset:

```
headline,pub_date,year
A Look Back: The Defining Performances,2010-02-28T23:16:30+0000,2010
```

This labeled dataset allows the analysis scripts to easily group headlines by year and compute metrics such as average happiness scores for each time period.

## Data Validation

Before proceeding to the analysis stage, basic checks were performed to ensure that the dataset had been correctly assembled. The script **`check_duplicates.py`** was used to identify potential duplicate entries in the dataset. This step helped confirm that the combined dataset did not contain a large number of repeated headlines resulting from the merging process.

Although minor irregularities such as repeated header rows occurred during early file merging, these did not significantly affect the dataset. The final dataset still contains hundreds of thousands of headlines and provides a sufficiently large corpus for sentiment analysis.

## Final Dataset

The final dataset used for analysis is stored as:

```
data/nyt_headlines_labeled.csv
```

This file contains approximately **270,000 headlines in total**, drawn from the three comparison years. After balancing the dataset for fairness, **55,421 headlines from each year** will be used for the emotional tone analysis.

This dataset forms the foundation for the later stages of the project, where the emotional tone of headlines will be measured using the Hedonometer word list and compared across different years.