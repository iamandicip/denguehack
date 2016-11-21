import tweepy
from tweepy import OAuthHandler

import private_tokens
import custom_stream_listener
import util_constants as uc

class TwitterDataExtractor:

    def collect_tweets(self, params):
        print('Collecting tweets')
        #authentication
        auth = OAuthHandler(private_tokens.consumer_key, private_tokens.consumer_secret)
        auth.set_access_token(private_tokens.access_token, private_tokens.access_secret)
        api = tweepy.API(auth)

        #streaming listener
        customStreamListener = custom_stream_listener.CustomStreamListener()
        dataStream = tweepy.Stream(auth = api.auth, listener = customStreamListener)

        dataStream.filter(track = params['search_terms'], locations = params['locations'], async = False)

if __name__== '__main__':
    params = {'search_terms' : uc.dengue_south_america,\
              'locations' : uc.south_central_america_box}

    tde = TwitterDataExtractor()
    tde.collect_tweets(params)
