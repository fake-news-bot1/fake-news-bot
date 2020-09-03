import praw
import time
import pickle

from functions import credentials, scraper, analyzer


def connect():
    reddit = praw.Reddit(client_id=credentials.client_id,
                         client_secret=credentials.secret,
                         user_agent=credentials.user_agent,
                         username=credentials.username,
                         password=credentials.password)

    already_replied = load_pickle()

    subreddit = reddit.subreddit('worldnews+news+politics+testingground4bots')

    # phrase to activate the bot
    keyphrase = '!FakeNewsBot'

    while True:
        for comment in subreddit.stream.comments(skip_existing=True):
            try:
                # Skip comment if no article URL found
                if comment.submission.url and comment.body:
                    url = comment.submission.url
                else:
                    continue
    
                comment_id = [comment.submission, comment]
    
                # If bot is called and has not already replied to comment, scan article and reply
                if keyphrase in comment.body and comment_id not in already_replied:
                    article_text = scraper.get_data(url)
                    result = analyzer.analyze(article_text)

                    form_reply(comment, result)

                    already_replied.append(comment_id)
                    save_pickle(already_replied)
                    print(f'URL: {url} \n\nResult: {result}')
            except (TypeError, praw.exceptions.RedditAPIException):
                pass
            except TypeError:
                msg = 'Oops, looks like something has gone wrong. Please try again in a few minutes.'
                form_reply(comment, msg)


# Load 'replied.pickle' object and comments list, otherwise create new pickle
def load_pickle():
    try:
        file_handler = open('replied.pickle', 'rb')
        comments = pickle.load(file_handler)
        file_handler.close()

        return comments

    except FileNotFoundError:
        create_pickle()


# Create 'replied.pickle' object and return empty list
def create_pickle():
    comments = []

    file_handler = open('replied.pickle', 'wb')
    pickle.dump(comments, file_handler)
    file_handler.close()

    return comments


# Save list of  replied comments to 'replied.pickle' object
def save_pickle(comments):
    file_handler = open('replied.pickle', 'wb')
    pickle.dump(comments, file_handler)
    file_handler.close()


def form_reply(comment, result):
    msg = f'{result} \n_____ \n\nThis bot scrapes news articles and analyzes language patterns \
    using machine learning packages for bias and misinformation with roughly 80% accuracy on unseen articles. \
    \n\n\nThe Passive Aggressive Classifier runs on a training dataset of 20,799 articles found\
      [here](https://www.kaggle.com/c/fake-news/data?select=train.csv), and the  source code can be found\
      [here](https://github.com/fake-news-bot1/fake-news-bot).'

    comment.reply(msg)


if __name__ == '__main__':
    connect()
