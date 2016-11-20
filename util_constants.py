import urlmarker
import re

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

india_coord_box = [69.645311, 5.611202, 88.457192, 33.152259]

#all the official languages in India
dengue_punjabi = 'dengue'
dengue_en_upper = 'Dengue'
dengue_hindi = 'डेंगू'
dengue_tamil = 'டெங்கு'
dengue_telugu = 'డెంగ్యూ'
dengue_marathi = 'डेंग्यू'
dengue_kannada = 'ಡೆಂಗ್ಯೂ'
dengue_malayalam = 'ഡെങ്കിപ്പനി'
dengue_gujarati = 'ડેન્ગ્યુ'
dengue_bengali = 'ডেঙ্গু'

india_dengue = [dengue_punjabi, dengue_en_upper, dengue_hindi, dengue_tamil,\
                dengue_telugu, dengue_marathi, dengue_kannada, dengue_malayalam,\
                dengue_gujarati, dengue_bengali]
