# 📊Hedonometer Project📊
This repository contains two mini-projects that explore how emotional tone in language can be measured using the labMT hedonometer. The first project examines the structure of the labMT lexicon itself, while the second project applies the lexicon to analyze the emotional tone of New York Times headlines across different years.



<br><br>

# Mini-Project 1️⃣: Exploring the labMT Lexicon  
### Introduction
In this mini-project, we analyses the labMT 1.0 dataset, a collection of English words rated for happiness by crowd workers. We use Python to clean the data and explore patterns in happiness scores and word usage across several text corpora. We then combine quantitative plots with qualitative interpretation to examine how emotional meaning in language depends on context and cultural perspective.

## Dataset
### Source
We use the labMT 1.0 dataset (Dodds et al., 2011), which includes 10,222 English words rated for happiness.

Each word has:
- An average happiness score
- A standard deviation of ratings
- Frequency ranks in four corpora:
  - Twitter
  - Google Books
  - New York Times
  - Lyrics

### Data Dictionary
Below is a description of each column in the dataset, including its meaning, data type, and notes on missing values.
| Column | Type | Meaning | Missing Values |
|------|------|------|------|
| word | string | The English word being evaluated in the dataset | None |
| happiness_rank | integer | Rank of the word based on its average happiness score (1 = highest happiness score) | None |
| happiness_average | float | Average happiness score assigned by Mechanical Turk raters on a 1–9 scale | None |
| happiness_standard_deviation | float | Standard deviation of happiness ratings, indicating disagreement among raters | None |
| twitter_rank | float | Frequency rank of the word in the Twitter corpus | 5,222 missing values (words not in the top 5,000) |
| google_rank | float | Frequency rank of the word in the Google Books corpus | 5,222 missing values (words not in the top 5,000) |
| nyt_rank | float | Frequency rank of the word in the New York Times corpus | 5,222 missing values (words not in the top 5,000) |
| lyrics_rank | float | Frequency rank of the word in the song lyrics corpus | 5,222 missing values (words not in the top 5,000) |



## Methods
```mermaid
flowchart TD
    A[Load dataset] --> B[Remove metadata rows]
    B --> C[Replace missing values with NaN]
    C --> D[Convert data to numeric]
    D --> E[Check data quality]
    E --> F[Handle missing rank values]
    F --> G[Save cleaned data]
    G --> H[Set analysis choices]
    H --> I[Define scope of analysis]
```


## Results
### 1. Distribution of Happiness Scores
![Distribution of Happiness Scores](figures/hist_happiness_average.png)

To understand the overall structure of the dataset, we examine the distribution of happiness scores using both summary statistics and a histogram. The mean happiness score is approximately 5.38, and the median is very close to this value, indicating that the distribution is centered around the middle of the scale. The standard deviation is about 1.08, suggesting a moderate spread in the data.

The range of values extends from approximately 1.3 to 8.5, showing that the lexicon includes both very negative and very positive words. However, the 5th and 95th percentiles (around 3.18 and 7.08) indicate that most words fall within a narrower central interval, with relatively few extreme values.

Visually, the histogram shows that the distribution is not perfectly symmetric. While it is roughly bell-shaped, there is a slight skew toward higher (more positive) values, meaning that moderately positive words are more common than strongly negative ones. The right tail extends into high happiness scores, but both tails are relatively thin, indicating that extreme values are less frequent.

Overall, the distribution suggests that language in the labMT lexicon is concentrated around neutral to moderately positive emotional values, with fewer words expressing strong negativity or extreme positivity. This pattern implies a bias toward mildly positive expression in commonly used language.

### 2. Happiness vs Disagreement
![Happiness vs Disagreement](figures/scatter_avg_vs_sd.png)

We examine the relationship between happiness scores and disagreement (standard deviation) using a scatterplot. While one might initially expect that words with very high or very low happiness scores would have more consistent evaluations, the plot suggests the opposite pattern.

The scatterplot shows a clear fan-shaped distribution. Words near the neutral midpoint (around a happiness score of 5) tend to have lower disagreement, while words further away from neutrality—either more positive or more negative—exhibit higher levels of disagreement. This indicates that variability in ratings increases as words become more emotionally extreme.

To make this pattern more interpretable, we label several key words directly on the plot. For example, suicide (the most negative word, happiness ≈ 1.3) and laughter (the most positive word, happiness ≈ 8.5) both lie toward the edges of the distribution, where disagreement begins to increase. More strikingly, words such as fucking and fuckin have some of the highest disagreement values (standard deviation ≈ 2.9 and 2.74), despite not being the most extreme in terms of happiness. These words are likely interpreted differently depending on context, tone, or speaker intention.

The presence of such outliers highlights that disagreement is not driven solely by positivity or negativity, but also by ambiguity, slang usage, and cultural factors. Words with multiple meanings or strong emotional connotations tend to produce less consistent evaluations across annotators.

The plot suggests that emotional intensity and contextual variability are closely linked: as words become more emotionally charged or context-dependent, agreement between raters decreases. This demonstrates that affective meaning in language is not fixed, but shaped by interpretation and usage.

### 3. Corpus Comparison
![Corpus comparison](figures/heatmap_corpus_overlap.png)

To better understand how “common language” varies across contexts, we compare the overlap between the top 5000 words in four corpora: Twitter, Google Books, the New York Times (NYT), and song lyrics. Because each corpus is constructed from its own top-5000 list, raw counts are not informative; instead, we examine how many words overlap between corpora.

The heatmap shows that overlap varies substantially across pairs. Google Books and NYT share the highest overlap (3414 words), suggesting that both corpora reflect more formal, written language. In contrast, NYT and Lyrics have the lowest overlap (2241 words), indicating a strong difference in register: news language is more formal and informational, while lyrics tend to be more emotional and stylistically expressive.

Twitter occupies an intermediate position. Its overlap with Lyrics (3127 words) is relatively high, reflecting shared informal and conversational elements, while its overlap with NYT (2881 words) is lower but still substantial. This suggests that Twitter contains a mix of informal expression and informational language.

Overall, the results demonstrate that what counts as “common language” depends strongly on the corpus. Even when each corpus includes 5000 high-frequency words, the overlap between them is far from complete, highlighting differences in style, context, and usage across domains.



## Qualitative “Exhibit” of Words
| category                           | word       |   happiness_average |   happiness_standard_deviation |
|:-----------------------------------|:-----------|--------------------:|-------------------------------:|
| Very positive                      | laughter   |                8.5  |                         0.9313 |
| Very positive                      | happiness  |                8.44 |                         0.9723 |
| Very positive                      | love       |                8.42 |                         1.1082 |
| Very positive                      | happy      |                8.3  |                         0.9949 |
| Very positive                      | laughed    |                8.26 |                         1.1572 |
| Very negative                      | terrorist  |                1.3  |                         0.9091 |
| Very negative                      | suicide    |                1.3  |                         0.8391 |
| Very negative                      | rape       |                1.44 |                         0.7866 |
| Very negative                      | terrorism  |                1.48 |                         0.9089 |
| Very negative                      | murder     |                1.48 |                         1.015  |
| Highly contested (high SD)         | fucking    |                4.64 |                         2.926  |
| Highly contested (high SD)         | fuckin     |                3.86 |                         2.7405 |
| Highly contested (high SD)         | fucked     |                3.56 |                         2.7117 |
| Highly contested (high SD)         | pussy      |                4.8  |                         2.665  |
| Highly contested (high SD)         | whiskey    |                5.72 |                         2.6422 |
| Weird / culturally loaded (chosen) | christ     |                6.16 |                         2.3067 |
| Weird / culturally loaded (chosen) | capitalism |                5.16 |                         2.4524 |
| Weird / culturally loaded (chosen) | islam      |                4.68 |                         2.325  |
| Weird / culturally loaded (chosen) | porn       |                4.18 |                         2.4302 |
| Weird / culturally loaded (chosen) | zombies    |                4    |                         2.3733 |

This twenty word table we have created shows that the LabMT happiness score collects culturally situated judgments rather than fixed emotional meanings. The words that scored with the highest happiness scores (e.g., laughter = 8.50, happiness = 8.44, love = 8.42) are strongly associated with joy, affection, social bonding, and are consistently interpreted as something positive. The very negative words on the other hand (e.g., terrorist = 1.30, suicide = 1.30, rape = 1.44) have a very low score because they are connected to themes such as death, harm and violence, and are understood to be very negative regardless of what the context usually is. 

The “highly contested” words (e.g., fucking SD = 2.93, fuckin SD = 2.74, fucked SD = 2.71) show how disagreement can occur when the words used are too taboo, context dependent or slang, since slang can be used refering to sexual, humourous or insult, which leads to variation in how they are interpreted. For example, whiskey (mean = 5.72, SD = 2.64) may be associated with celebration and social bonding for some, but when it comes to religion (mostly prohibition) addiction or harm to others, can explain its high level of disagreement.

And lastly, the weird/culturally loaded words (e.g., Christ mean = 6.16, SD = 2.3; capitalism mean = 5.16, SD = 2.45; Islam mean = 4.68, SD = 2.33; porn mean = 4.18, SD = 2.43; Zombies mean = 4 SD = 2.37) show how schools of thought, religion and certain aspects of media may shape someone’s interpretations. Religious words and conversations on social media platforms usually bring conflict or stigma to a conversation more than a positive shared experience, whereas for other words, it may be a form of identity or comfort. The word “Capitalism” may be signal opportunity or exploitation depending on an individuals political stance, since its in the mid mean range it could mean that a mix of individuals with different political stances about capitalism. Lastly words that are popular within pop culture, like “zombies”, can be used for either entertainment in a playful manner, to express fear for them, disgust or refering to someone as a "zombie" based on their attitude or behaviour. Hence a difference between these categories can show how the happiness score can be dependent on contextual and community based meanings as much as the disctionary meaning of certain terms. 

Overall the patterns we noticed show that higher disagreement (standard deviation) is linked to words with more ambiguity and context, whereas words that are universally understood tend to either have both extreme scores and/or lower variability. Suggesting that the emotional meaning of words within the dataset is shaped by the words but also by the perspectives of the people who used/ranked them. Since the ratings that were collected and we are using are from Mechanical Turk workers, so the dataset most likely reflects the cultural and ideological biases of the specific group of raters rather than a universal measure of these words.



## Critial Reflection
### Dataset Provenance
The labMT 1.0 dataset (“language assessment by Mechanical Turk”) was created by Dodds et al. (2011) as part of their "hedonometer" work. The "hedonometer" is a tool that was designed to measure the average happiness of text collected from places like Twitter. The first thing the authors did was they selected 10,000 of the most frequently used English words and they were chosen based on how often they were used, not based on specialized words. Each word after that got rated by a few workers on Amazon Mechanical Turk on a scale from 1-9, 1 being very unhappy and 9 being very happy. Then they got these few ratings and calculated the average in order to produce a single happiness score by word. The standard deviation was then used to show the difference between the ratings. Then this word list was used to calculate the average happiness of collections of large texts by calculating an average happiness score where words that appear more often count more. In this way the dataset works as a word-based tool that measures how positive or negative large texts are.

### Limitations and Consequences
Through the labMT dataset it's possible to analyze big texts of emotional language but there are a few important things that decide what it can and cannot do. The happiness ratings were collected from Mechanical Turk workers which is a specific demographic and culture. That means that the scores are a reflection of understanding of emotion that’s not the same across the different cultures. Second, they were rated without context. Normally emotional meanings on words depend on tone, the context they were used at. The dataset simplifies emotional meaning. Third, the method uses a single numerical scale to measure a complex emotional expression. However, the design also makes the analysis easier in some ways. The dataset makes it possible for researchers to see general patterns in large positive or negative large texts, and also to compare across different texts and time periods. At the same time the limitation is that it’s difficult to capture deeper meaning, who is speaking, or how culture influences the language. Therefore, the labMT dataset is a useful but simplified measurement tool. It allows us to analyze emotional language in very large texts, but we need to question the assumptions it makes on language and emotion.



## Team Roles
**Repo & workflow lead (Yiran Wu)**
- Creates the GitHub repo and folder structure.
- Manages branches / merges (or coordinates who edits which files).
- Ensures the README stays organized and readable.
- Ensures the README reads smoothly and makes a clear argument.

**Data wrangler (Yimai Liu)**
- Loads the dataset, handles missing values, converts data types.
- Produces the data dictionary and “what each column means” section.

**Quantitative analyst (Chaeyun Kim)**
- Leads descriptive statistics and at least 2 core plots.
- Makes sure plots have labels and captions.
- Checks results for sanity and reproducibility.

**Qualitative / close-reading lead (Duaa Khan)**
- Leads careful interpretation of selected words (examples, ambiguity, cultural meaning).
- Connects qualitative observations back to patterns in the plots.

**Provenance & critique lead (Maya Yonkova)**
- Reconstructs how the dataset was generated (pipeline).
- Writes the “critical reflection” sections: consequences, bias, limitations, and what the dataset makes easy/hard to see.





<br><br>

# Mini-Project 2️⃣: Inferring Happiness in NYT Headlines  
### Introduction
In this mini-project, we use the labMT 1.0 hedonometer as a measurement instrument to analyze the emotional tone of New York Times headlines. Headlines are collected through the NYT Article Search API, and their happiness scores are computed by matching words with the labMT lexicon. We then compare the average happiness scores of headlines across the selected years to examine how their emotional tone changes over time.


## Research Question
How did the overall emotional tone of New York Times headlines evolve during the financial crisis period (2006–2011)?


## Data Acquisition and Dataset Preparation

Our research question for this project is: *How did the overall emotional tone of New York Times headlines evolve during the financial crisis period (2006–2011)?* To address this question, we constructed a dataset of New York Times headlines that could later be analyzed using the Hedonometer (labMT) word list. 

### Data Source

The headline data was collected from the New York Times Archive API. The Archive API provides article metadata on a monthly basis, making it particularly suitable for collecting large volumes of articles across specific time periods. After obtaining an API key from the New York Times Developer portal, the connection was first tested using small requests to ensure that the key and request structure were functioning correctly.

Once the API connection was verified, data collection was automated using a Python script (*`nyt_headlines.py`*). This script uses the *`requests`* library to retrieve monthly archive data and extract the relevant fields from the returned JSON structure. For each article, the script extracts the main headline (*`headline.main`*) and the publication date (*`pub_date`*). The extracted data is then written to CSV files for further processing.

To run this script, you must obtain your own New York Times API key from the NYT Developer Portal and replace "*YOUR_API_KEY*" in the script. The script uses the NYT Archive API to retrieve article data. For security reasons, API keys are not included in this repository.

### Data Collection Process

The data collection process was carried out month-by-month across three defined periods surrounding the 2008 financial crisis. The crisis period was defined as September 2008 to June 2009, corresponding to the period following the collapse of Lehman Brothers. To enable a balanced comparison, two 24-month windows were defined before and after the crisis period.

The final time ranges are summarized below:

| Period | Time Range          | Duration  |
| ------ | ------------------- | --------- |
| Before | Sep 2006 – Aug 2008 | 24 months |
| During | Sep 2008 – Jun 2009 | 10 months |
| After  | Jul 2009 – Jun 2011 | 24 months |

For each month within these periods, all available headlines were retrieved via the API. From this pool, a random sample of up to 500 headlines per month was selected. Sampling was performed independently for each month in order to maintain temporal consistency across the dataset.

Because the NYT API imposes rate limits, requests were spaced using time delays, and retry logic was implemented to handle temporary quota violations. When a rate limit error occurred, the script paused and retried the same request to ensure that no monthly data was skipped. The collection process was first tested on a small subset of months to ensure that API calls, parsing, and file writing were functioning correctly before running the full data acquisition.

### Dataset Construction

All datasets included in this repository are processed data rather than raw data. The original data was obtained from the New York Times Archive API in structured JSON format, but during collection, the data was transformed by selecting relevant fields, applying random sampling, and assigning period labels. As a result, the repository does not contain raw API outputs, but instead provides structured datasets prepared for analysis.

The collected data for each period was initially stored in separate CSV files (*`nyt_before.csv`*, *`nyt_during.csv`*, and *`nyt_after.csv`*). These files were then combined into a single dataset (*`nyt_all_periods.csv`*) containing all sampled headlines across the three periods.

Each row in the dataset includes the headline text, publication date, and corresponding time period (Before, During, After), along with the year and month of publication. This structure allows for straightforward grouping and comparison across time.

Below is an example row from the dataset:
```
period,year,month,headline,pub_date
After,2011,4,Woman Killed When Cab Crashes Into Bronx Store,2011-04-22T02:37:22+0000
```

### Duplicate Handling

During the dataset preparation stage, duplicate entries were identified and examined. Duplicates were defined as rows with identical headline text and identical publication date, which indicates that the same article was included more than once during the collection or merging process.

A total of 88 exact duplicate rows were identified in the combined dataset. These duplicates were removed to produce a cleaned dataset (*`nyt_all_periods_clean.csv`*). Importantly, headlines that appeared multiple times on different dates were retained, as these represent valid and distinct observations in the dataset.

After duplicate removal, some months contain slightly fewer than 500 headlines. This is expected and reflects the elimination of repeated entries rather than a loss of unique data.

### Data Validation

Basic validation checks were performed to ensure the integrity of the dataset. This included verifying the number of headlines collected per month and confirming that the data was correctly labeled by period. The dataset was also inspected for structural consistency after merging and cleaning.

The final cleaned dataset contains approximately 28,900 headlines sampled across all periods. A summary of the dataset is shown below:

| Metric                    | Value     |
| ------------------------- | --------- |
| Total headlines (cleaned) | 28,934   |
| Sampling size per month   | Up to 500 |
| Duplicate rows removed    | 88        |
| Number of periods         | 3         |

### Final Dataset

The final dataset used for analysis is stored as: *`data/nyt_economic_crisis/nyt_all_periods_clean.csv`*

This dataset forms the basis for the next stage of the project, where the emotional tone of headlines will be measured using the Hedonometer word list and compared across different phases of the financial crisis.




## Measurement
This project measures the overall emotional tone of New York Times headlines across 2008 financial crisis. We implement a hedonometer-based approach using the labMT lexicon to assign a happiness score to each headline.

### Method
The emotional tone of each headline is computed using the following pipeline:

```mermaid
flowchart TD
A[NYT Headline] --> B[Tokenized Into Lowercase Words]
B --> C[Match with LabMT Lexicon]
C --> D[Assign Happiness Scores]
D --> E[Average Score = Headline Happiness]

C --> F[Count Matched Words]
B --> G[Count Total Words]
F --> H[Coverage Ratio = Matched Words divided by Total Words]
G --> H
```

### Coverage Ratio
To evaluate how much of each headline is represented in the lexicon, we compute a coverage ratio: overage ratio = matched words / total words. This metric indicates the proportion of words that contribute to the happiness score.

### Output

The processed dataset is saved as *data/nyt_economic_crisis/nyt_all_periods_scored.csv*.

This dataset contains the following variables:

| Column | Description |
|--------|------------|
| period | Time period relative to the 2008 economic crisis (before / during / after) |
| year | Extracted year from the publication date |
| month | Extracted month from the publication date |
| headline | NYT article headline |
| pub_date | Original publication date |
| happiness_score | Average labMT happiness score of matched words in the headline |
| matched_words | Number of words in the headline found in the labMT lexicon |
| total_words | Total number of words in the headline |
| coverage_ratio | Proportion of words matched with the lexicon (matched_words / total_words) |

### Notes on Measurement

- The **happiness_score** is computed only from words that exist in the labMT lexicon.  
- Words not found in the lexicon (out-of-vocabulary, OOV) are excluded from the calculation.  
- If a headline contains no matched words, its happiness score is recorded as missing (`None`).  

The **coverage_ratio** serves as a diagnostic indicator of how representative the computed sentiment is:
- Higher coverage suggests more reliable sentiment estimation  
- Lower coverage indicates that many words are not captured by the lexicon  


### Usage

This dataset will be used in the next stage of the project to:

- Compare emotional tone across crisis periods   
- Design sampling strategies  
- Compute uncertainty measures (e.g., confidence intervals, bootstrapping)  
- Produce statistical inference plots  




## Results

### Average Happiness by Year
![Average Happiness by Year](figures/happiness_by_decade_ci.png)
This figure shows the average happiness score of New York Times headlines for 2000, 2010, and 2020. The mean happiness score is 5.357 for 2000, 5.429 for 2010, and 5.367 for 2020. The 2000s and 2020s have a lower average happiness score, while the 2010s have the highest average happiness score. The largest difference is only about 0.07 points on the 1–9 hedonometer scale. The difference between the decades is relatively small, which shows that the emotional tone of New York Times headline has remained stable over time, and stays close to the neutral middle of the scale.

### Bootstrap Distributions
![Bootstrap 2000](figures/bootstrap_distribution_2000s.png)

![Bootstrap 2010](figures/bootstrap_distribution_2010s.png)

![Bootstrap 2020](figures/bootstrap_distribution_2020s.png)
We applied bootstrap resampling with 2,000 iterations to estimate the mean happiness score for each year and to calculate 95% confidence intervals.

These figures show the bootstrap distributions of the mean happiness score for New York Times headlines in 2000, 2010, and 2020. Bootstrapping resamples the data repeatedly to create an estimation for how stable the average happiness score is for each year, and to estimate how much the mean happiness score could vary. The symmetric shapes of these distributions indicate that the estimated happiness scores are stable and reliable.

While the 2000 and 2020 distributions are positioned closely and show some overlap, the 2010 distribution is completely separate from the others. This lack of overlap with the 2010 suggests that the increase in happiness during that year is a statistically significant shift rather than a random fluctuation.

Overall, the plots confirm that the emotional tone of New York Times headlines remains relatively stable and close to the neutral middle. However, the clear separation of the 2010 distribution proves there was a small but measurable change in the journalistic tone during that year.

### Summary Table
| Decade | Mean Happiness | CI Lower | CI Upper | n      |
|--------|----------------|----------|----------|--------|
| 2000s  | 5.357          | 5.353    | 5.361    | 55,417 |
| 2010s  | 5.429          | 5.424    | 5.433    | 55,417 |
| 2020s  | 5.367          | 5.364    | 5.371    | 55,417 |

The summary table presents the mean happiness score, confidence interval, and sample size for each decade. To ensure a fair comparison, an equal sample size of 55,417 headlines was used for each decade.


## Team Roles
**Repo & workflow lead (Yiran Wu)**
- Manages branches/merges.
- Keeps the README readable.
- Enforces folder conventions.

**Data acquisition lead (Chaeyun Kim)**
- Downloads via API or dataset source.
- Writes fetch script.
- Documents provenance and ethics.

**Measurement lead (Yimai Liu)**
- Implements and tests hedonometer scoring (tokenization, matching to labMT, handling OOV words).

**Stats & sampling lead (Duaa Khan)**
- Designs sampling plan.
- Computes uncertainty (CI/bootstraps).
- Produces inference plots.

**Visualisation lead (Maya Yonkova)**
- Designs and implements optimal visualisations to back-up data-driven claims.


<br><br>

# How To Run The Code
**1) Create A Virtual Environment**  
macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
```
Windows (PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
```
**2) Install Dependencies**
```bash
python3 -m pip install -r requirements.txt
```
**3) Run Mini-Project 1: Exploring the labMT Lexicon**  
Run the scripts in the following order:
```bash
python3 src/01_load_clean.py
python3 src/02_quant_analysis.py
python3 src/03_word_exhibit.py
```
**4) Run Mini-Project 2: Inferring Happiness in NYT Headlines**  
Run the scripts in the following order:
```bash
python3 04_nyt_headline_collector.py
python3 05_add_year_column.py
python3 06_check_duplicates.py
python3 07_check_data.py
python3 08_compute_happiness.py
python3 09_stats_sampling.py
```

<br>

# Citation
Dodds, P. S., Harris, K. D., Kloumann, I. M., Bliss, C. A., & Danforth, C. M. (2011). Temporal patterns of happiness and information in a global social network: Hedonometrics and Twitter. PLOS ONE, 6(12), e26752.  

The New York Times. (n.d.). *Article Search API*. https://developer.nytimes.com/docs/articlesearch-product/1/overview.

<br>

# AI Disclosure
- AI was used to clarify the assignment instructions and to help us understand the responsibilities of different roles.
- AI tools were used to help interpret terminal error messages and identify possible fixes.
- AI tools were occasionally used to explain Git workflows.
- AI helped us with drafting code and explanations, but we ensured we understood the meaning of each line after carefully reading and reviewing the scripts.
