# fake-news-bot

This is a machine learning project which runs on a Reddit bot. It scrapes a news article when called on a number of subreddits, and analyzes language patterns using machine learning packages for bias and reliability with roughly 80% accuracy on unseen articles. The Passive Aggressive Classifier runs on a training dataset of 20,799 articles found [here](https://www.kaggle.com/c/fake-news/data?select=train.csv).

### Built with:
#### Web Scraping
- BeautifulSoup4
- Requests

#### Machine Learning
- Pandas
- Scikit-learn (sklearn)
- Pickle

#### Reddit bot connection
- Praw

# Getting Started
### Prerequisites
- Pipenv

### Installation
```
$ git clone https://github.com/danielrshackleton/fake-news-bot.git
$ pipenv install
```

## Usage
### In Reddit
To call FakeNewsBot on a reddit post, just comment `!FakeNewsBot` within the specified subreddits (r/worldnews for now). *Important: this program is not currently running on a private server so will not currently reply*.

### To use custom URL links outside of Reddit

This program uses pickled Passive Aggressive Classifier and Vectorizer objects. If there is an issue with these, download train.csv from here and move to the data_set directory (file is too large for GitHub upload limits). 

To use the article analysis functionality, simply clone the repository, comment out the reddit connection on `main.py`, swap out out the URL string for your article URL and run. 
