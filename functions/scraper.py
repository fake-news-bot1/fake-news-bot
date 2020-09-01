import requests
from bs4 import BeautifulSoup


def get_data(url):

    article = requests.get(url).text
    soup = BeautifulSoup(article, 'html.parser')

    # title = soup.find('h1')
    # title_text = title.get_text().strip()

    p_tags = soup.find_all('p')
    p_tags_text = [tag.get_text().strip() for tag in p_tags]

    # Filter out sentences that contain newline characters '\n' or don't contain periods.
    sentence_list = []
    for sentence in p_tags_text:
        if '.' in sentence or '\n' not in sentence:
            sentence_list.append(sentence)

    # Combine list items into string.
    article_text = ' '.join(sentence_list)

    return article_text
