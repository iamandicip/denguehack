import tweepy
from tweepy import OAuthHandler
from tweepy.parsers import JSONParser
import json
import private_tokens
import custom_stream_listener
import util_constants as uc
from datetime import datetime


class TwitterDataExtractor:

    def search_and_collect_tweets(self, params):
        searched_tweets = []
        last_id = -1
        tweets_count = 0
        call_count = 0
        call_count_max = 180
        dt_max = 15 * 60 * 1000
        initial_dt = datetime.now().microsecond * 1000
        current_dt = initial_dt

        print('Collecting tweets')
        #authentication
        auth = OAuthHandler(private_tokens.consumer_key, private_tokens.consumer_secret)
        auth.set_access_token(private_tokens.access_token, private_tokens.access_secret)
        api = tweepy.API(auth)

        with open('historical_tweets.json', 'a') as f:

            # for tweet in tweepy.Cursor(api.search,
                                    #    q=search_params['q'],\
                                    #    geocode=search_params['geocode'],\
                                    #    include_entities=False,\
                                    #    rpp=100).items():
                # call_count += 1

            while (current_dt - initial_dt < dt_max) or (call_count < call_count_max):
                # results = api.search(search_params['q'], \
                                    #  geocode=search_params['geocode'], \
                                    #  count=200, since_id=24012619984051000, \
                                    #  max_id=str(last_id - 1))
                current_dt = datetime.now().microsecond * 1000

                try:
                    new_tweets = api.search(q=search_params['q'], \
                                            geocode=search_params['geocode'],\
                                            count=200, max_id=str(last_id - 1),\
                                            since_id=24012619984051000)

                    call_count += 1

                    if not new_tweets:
                        print('Existing because of no new tweets')
                        break

                    searched_tweets.extend(new_tweets)
                    last_id = new_tweets[-1].id

                except tweepy.TweepError as e:
                    # depending on TweepError.code, one may want to retry or wait
                    # to keep things simple, we will give up on an error
                    print(e)
                    break

            for tweet in searched_tweets:
                if 'dengue' in tweet.text.lower() and (tweet.place != None or tweet.coordinates != None):
                    # print(tweet.place)
                    # print(tweet.coordinates)
                    f.write(json.dumps(tweet._json)+ '\n')
                    tweets_count += 1

                    if tweets_count % 10 == 0:
                        print('Collected {0} tweets'.format(tweets_count))

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
    search_params = {'q' : 'dengue',
                     'geocode' : '-10,-56,3000km', \
                     'since_id':24012619984051000}

    params = {'search_terms' : uc.dengue_south_america,\
              'locations' : uc.south_central_america_box}

    tde = TwitterDataExtractor()
    tde.search_and_collect_tweets(search_params)
    # tde.collect_tweets(params)
