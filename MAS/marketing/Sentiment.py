import requests
import numpy as np
from tensorflow.keras.models import load_model
import pickle
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from bs4 import BeautifulSoup
from string import digits
import string
import nltk
import re
from newspaper import Article
from newspaper import Config

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
config = Config()
config.browser_user_agent = user_agent

#  News API KEY
apiKey = '9e33b380b35543bf85a8d249bd209fd4'


def loading_model():
    # loading Model
    model = load_model('/static/marketing_models/model.h5')
    print("Model Loaded...")

    # loading Vectorizer
    with open('/static/marketing_models/vectorizer.pickle', 'rb') as handle:
        vectorizer = pickle.load(handle)
        print("Vectorizer Loaded...")

    # loading Feature Selector
    with open('/static/marketing_models/selector.pickle', 'rb') as handle:
        selector = pickle.load(handle)
        print("Feature Selector Loaded...")
    return model, vectorizer, selector


def make_predictions(clean_articles):
    # Load the Model, Vectorizer and the Selector
    model, vectorizer, selector = loading_model()

    # Vectorize unseen data
    X_unseen = vectorizer.transform(clean_articles)

    # Select top k of the vectorized features
    X_unseen = selector.transform(X_unseen).astype('float32')

    predictions = model.predict(X_unseen.toarray())

    # Returns - Class of the article, prob. that it belongs to that class, prob that it belongs to negative class

    sentiment_index = np.argmax(predictions, axis=1)
    maps = {0: 'Negative', 1: 'Neutral', 2: 'Positive'}
    return (np.vectorize(maps.get)(sentiment_index), np.max(predictions, axis=1))

    # return (np.argmax(predictions, axis = 1), np.max(predictions, axis = 1))


def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""

    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)


def clean_text(text, lemmatizer_active=True):
    """ 
        Input: String
        Output: String with punctuations and numbers removed 
        
        This is the version 2 of the clean_text function previously created.
    """

    assert isinstance(text, str), "Input variable should be a string"

    # Remove the html content and return the clean text
    text = BeautifulSoup(text, "lxml").text

    # Remove \n
    text = text.split('\n')
    text = ' '.join(text)

    # Remove \t
    text = text.split('\t')
    text = ' '.join(text)

    # Remove emails
    pattern = '\S*@\S*\s?'
    remove_emails = re.compile(pattern)
    text = remove_emails.sub('', text)

    # Remove urls
    pattern = r'\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b'
    remove_urls = re.compile(pattern)
    text = remove_urls.sub('', text)

    # Replacing the contractions
    # text = replace_contractions(text)

    # Remove punctuation
    no_punc = [char for char in text if char not in string.punctuation]
    text = ''.join(no_punc)

    # Remove digits
    remove_digits = str.maketrans('', '', digits)
    text = text.translate(remove_digits)

    # Word Tokenize
    tokens = word_tokenize(text)

    # Lemmatizaion
    if lemmatizer_active:
        lemmatizer = WordNetLemmatizer()
        words = [lemmatizer.lemmatize(word, get_wordnet_pos(word)) for word in tokens]

    # Lower case every word
    tokens = [w.lower() for w in words]

    # Remove single letter words, if present
    words = [word for word in tokens if (len(word) >= 2 or word == 'i' or word == 'a')]

    # Join the word list back to string
    article = ' '.join(words)

    return article


def get_article(url):
    # Get the url
    article = Article(url, config=config)

    # Download the article
    article.download()

    # parse the article
    article.parse()

    # return the text
    return article.text


def search_entity(entity,language = 'en',apiKey = apiKey):
  #Send a REST request, more parameters can be added
  search = f"https://newsapi.org/v2/top-headlines?q={entity}&language={language}&apiKey={apiKey}"
  articles_api = requests.get(search).json()
  
  #Converting the articles into a dataframe
  articles_df = pd.DataFrame.from_dict(articles_api.get('articles'))
  try:
    articles_df['Text'] = articles_df.url.apply(get_article)
    articles_df['Clean_text'] = articles_df.Text.apply(clean_text)
  except:
    articles_df['Clean_text'] = articles_df.content.apply(clean_text)
  return articles_df


def articles(entity):
    data = search_entity(entity)
    data['source'] = data['source'].apply(lambda x: x.get('name'))
    predictions = make_predictions(data['Clean_text'])
    return pd.DataFrame(list(zip(data['Text'], predictions[0], predictions[1])), columns=['Text', 'Sentiment',
                                                                                          'Sentiment Score'])
