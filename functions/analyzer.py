import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
train_file = os.path.join(THIS_FOLDER, '../data_set/train.csv')


def reanalyze(article_text):
    df = pd.read_csv(train_file)

    # Change the labels
    df.loc[(df['label'] == 1), ['label']] = 'FAKE'
    df.loc[(df['label'] == 0), ['label']] = 'REAL'

    labels = df.label
    x_train, x_test, y_train, y_test = train_test_split(df['text'],
                                                        labels,
                                                        test_size=0.27,
                                                        random_state=7,
                                                        shuffle=True)

    # Initialize a TfidfVectorizer, vectorize the text
    tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)

    # Fit and transform train set, transform test set
    tfidf_train = tfidf_vectorizer.fit_transform(x_train.values.astype('U'))
    tfidf_test = tfidf_vectorizer.transform(x_test.values.astype('U'))

    # Initialize a PassiveAggressiveClassifier and fit training sets
    pac = PassiveAggressiveClassifier(max_iter=50)
    pac.fit(tfidf_train, y_train)

    # Predict on the test set and calculate accuracy
    y_pred = pac.predict(tfidf_test)
    score = accuracy_score(y_test, y_pred)

    vec_new = tfidf_vectorizer.transform([article_text])
    y_pred_new = pac.predict(vec_new)
    rounded_score = round(score * 100, 2)

    # confusion_matrix(y_test, y_pred, labels=['FAKE', 'REAL'])
    print(f'Accuracy: {rounded_score}')

    result = 'reliable content' if y_pred_new[0] == 'REAL' else 'unreliable content'
    str = f'Brrrrr, calculating... There is a good chance that this is **{result}**.'
    save_pickle(pac, tfidf_vectorizer)

    return str


def analyze(article_text):

    try:
        pac = pickle.load(open('pac.pickle', 'rb'))
        tfidf_vectorizer = pickle.load(open('vectorizer.pickle', 'rb'))
    except Exception as e:
        print(e)
        str = reanalyze(article_text)
        return str

    vec_new = tfidf_vectorizer.transform([article_text])
    y_pred_new = pac.predict(vec_new)

    result = 'reliable content' if y_pred_new[0] == 'REAL' else 'unreliable content'
    str = f'Brrrrr, calculating... There is a good chance that this is {result}.'

    return str


def save_pickle(pac, vectorizer):
    pickle.dump(pac, open('pac.pickle', 'wb'))
    pickle.dump(vectorizer, open('vectorizer.pickle', 'wb'))


