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
    # already_replied = []
    print(f'Replied to: {already_replied}')

    subreddit = reddit.subreddit('testingground4bots')
    # subreddit = reddit.subreddit('worldnews')

    # phrase to activate the bot
    keyphrase = '!FakeNewsBot'

    while True:
        for comment in subreddit.stream.comments():
            try:
                if comment.submission.url:
                    url = comment.submission.url
                else:
                    continue
                print(f'Commenter ID: {comment}, comment: {comment.body}')
                if keyphrase in comment.body and comment not in already_replied:
                    article_text = scraper.get_data(url)
                    msg = analyzer.analyze(article_text)

                    print(f'post: {url} \ntext: {article_text} \nresult: {msg}')
                    # comment.reply(msg)
                    # already_replied.append(comment)
                    print(f'Replied to: {already_replied}')
                    time.sleep(60)
            except TypeError:
                print(comment.submission.url)
                print("nope")
                continue
            # finally:
            #     save_pickle(already_replied)
                

def load_pickle():
    try:
        return pickle.load(open('replied.pickle', 'rb'))
    except Exception as e:
        print(e)
        create_pickle()


def create_pickle():
    arr = []
    pickle.dump(arr, open('replied.pickle', 'wb')) 
    return arr


def save_pickle(arr):
    pickle.dump(arr, open('replied.pickle', 'wb'))
    

if __name__ == '__main__':
    connect()
