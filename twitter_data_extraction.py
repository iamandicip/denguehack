import json
from datetime import datetime

import tweepy
from tweepy import OAuthHandler
import urlmarker
import private_tokens
import re

import operator
from collections import Counter
from nltk.corpus import stopwords
import string

from nltk.tokenize import word_tokenize
from nltk import bigrams


auth = OAuthHandler(private_tokens.consumer_key, private_tokens.consumer_secret)
auth.set_access_token(private_tokens.access_token, private_tokens.access_secret)

api = tweepy.API(auth)

tweets_file_name = 'tweets.json'

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    urlmarker.URL_REGEX,
    # r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]

tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

def save_tweet(tweet):
    simplified_tweet = {'created_at' : tweet.created_at.isoformat(),\
                        'text' : tweet.text,\
                        'lang' : tweet.lang,\
                        'place' : tweet.place,\
                        'coordinates' : tweet.coordinates,\
                        'geo' : tweet.geo,\
                        'favorite_count' : tweet.favorite_count,
                        'retweet_count' : tweet.retweet_count,
                        'id' : tweet.id, \
                        'user_location' : tweet.user.location,\
                        'user_screen_name' : tweet.user.screen_name,\
                        'user_name' : tweet.user.name}
    # print(dir(tweet.user))
    # print('storing:{0}'.format(json.dumps(simplified_tweet)))
    with open(tweets_file_name, 'a') as fp:
        fp.write(json.dumps(simplified_tweet) + '\n')

def clean_text(text):
    return re.sub(urlmarker.URL_REGEX, '', text)

def store_tweets(number_of_tweets):
    for tweet in tweepy.Cursor(api.home_timeline).items(number_of_tweets):
        save_tweet(tweet)

def preprocess(s):
    tokens = tokens_re.findall(s)
    tokens = [token[0] if emoticon_re.search(token[0]) else token[0].lower() for token in tokens]
    return tokens

def process_stored_tweets():
    with open(tweets_file_name, 'r') as f:
        punctuation = list(string.punctuation)
        stop = stopwords.words('english') + punctuation + ['rt', 'via', '...','…', '\'']
        # print(stop)

        count_single, count_hash, count_terms, count_bigrams = Counter(),Counter(),Counter(),Counter()
        for line in f:
            tweet = json.loads(line)
            # Create a list with all the terms
            terms_stop = [term for term in preprocess(tweet['text']) if term not in stop]

            # Count terms only once, equivalent to Document Frequency
            terms_single = set(terms_stop)
            # Count hashtags only
            terms_hash = [term for term in preprocess(tweet['text'])
                          if term.startswith('#')]
            # Count terms only (no hashtags, no mentions)
            terms_only = [term for term in preprocess(tweet['text'])
                          if term not in stop and
                          not term.startswith(('#', '@'))]
              # mind the ((double brackets))
              # startswith() takes a tuple (not a list) if
              # we pass a list of inputs

            terms_bigram = bigrams(terms_stop)

            # Update the counter
            count_single.update(terms_single)
            count_hash.update(terms_hash)
            count_terms.update(terms_only)
            count_bigrams.update(terms_bigram)

        # print(count_single.most_common(5))
        # print(count_hash.most_common(5))
        # print(count_terms.most_common(5))
        print(count_bigrams.most_common(5))


# store_tweets(50)
process_stored_tweets()

#API.search(q[, lang][, locale][, rpp][, page][, since_id][, geocode][, show_user])
