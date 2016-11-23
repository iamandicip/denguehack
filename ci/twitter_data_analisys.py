import re

import operator
from collections import Counter
from nltk.corpus import stopwords
import string

import util_constants as uc

from nltk.tokenize import word_tokenize
from nltk import bigrams

import json
from datetime import datetime


def preprocess(s):
    tokens = uc.tokens_re.findall(s)
    tokens = [token[0] if uc.emoticon_re.search(token[0]) else token[0].lower() for token in tokens]
    return tokens

def process_stored_tweets():
    with open(uc.tweets_file_name, 'r') as f:
        punctuation = list(string.punctuation)
        stop = stopwords.words('english') + punctuation + ['rt', 'via', '…', '\'']
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

process_stored_tweets()
