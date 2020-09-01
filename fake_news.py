#!/usr/bin/env python3

from functions import analyzer, scraper, reddit_conn


def test_run():
    url = 'https://www.infowars.com/watch-live-riots-are-rehearsal-for-revolution/'
    text = scraper.get_data(url)
    print(f'\n\nURL: {url}')
    result = analyzer.analyze(text)
    print(result)


if __name__ == '__main__':
    # Run with custom URL (uncomment to run)
    # test_run()

    # Run Reddit bot
    reddit_conn.connect()
