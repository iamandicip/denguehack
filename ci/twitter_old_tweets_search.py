from got3.manager import TweetCriteria
from got3.manager import TweetManager

from geo_locator import GeoLocator

import pandas as pd
import tweepy
from datetime import datetime, timedelta
import re

class TwitterOldTweetsExtractor:

    def search_and_collect_tweets(self, params, file_name):

        geo_locator = GeoLocator()

        # print(params)

        tweetCriteria = TweetCriteria().setQuerySearch(params['keyword'])\
        .setSince(params['since'])\
        .setUntil(params['until'])\
        .setLocation(params['location'])\
        .setRadius(params['radius'])\
        .setMaxTweets(params['max_tweets'])

        tweets_count = 0

        saved_ids = self.get_saved_tweets_ids(file_name)

        oldest_tweet_date = None

        for tweet in TweetManager.getTweets(tweetCriteria):
            if self.has_dengue_keyword(tweet) and self.has_location_data(tweet) and tweet.id not in saved_ids:
                with open(file_name, 'a', encoding='utf8') as f:
                    try:
                        tweet_string = self.tweeet_to_string(tweet, geo_locator)
                        if tweet_string:
                            f.write(tweet_string + '\n')
                            oldest_tweet_date = tweet.date

                        tweets_count += 1
                    except Exception as e:
                        print(e)

                if tweets_count % 10 == 0:
                    print('Collected {0} tweets'.format(tweets_count))

        print('Reached the limit of {0} searched tweets'.format(params['max_tweets']))
        print('Oldest saved tweet date is : {0}'.format(oldest_tweet_date))

    def has_location_data(self, tweet):
        return tweet.geo != None and tweet.geo.strip() != ''

    def has_dengue_keyword(self, tweet):
        return 'dengue' in tweet.text.lower()

    def tweeet_to_string(self, tweet, geo_locator):
        result = None

        if tweet.text:
            tweet.text = re.sub('"', '', tweet.text)
            tweet.text = re.sub(',', '', tweet.text)

        if tweet.geo:
            lat_long = geo_locator.get_coordinates_for_location(tweet.geo)

            if lat_long:
                attributes = ['"' + str(tweet.id) + '"', \
                              '"' + str(tweet.date) + '"', \
                              '"' + str(tweet.geo) + '"',\
                              '"' + str(lat_long[0]) + '"',\
                              '"' + str(lat_long[1]) + '"',\
                              '"' + str(tweet.text) + '"']

                result = ','.join(attributes)

        return result

    def get_saved_tweets_ids(self, file_name):
        ids = []
        try:
            with open(file_name, 'r', encoding='utf8') as f:
                for line in f:
                    tweet_id = line.split(',')[0]
                    tweet_id = re.sub('"', '', tweet_id)
                    if tweet_id.isdigit():
                        ids.append(tweet_id)
        except Exception as e:
            print(e)

        print('There are {0} already saved tweets in file {1}'.format(len(ids), file_name))

        return ids


if __name__ == '__main__':

    file_name = 'tweets_01_week1.csv'

    tote = TwitterOldTweetsExtractor()

    # rng = pd.date_range(start='2016-01-01', end='2016-01-02', freq='D').tolist()
    # dates = [str(ts.date) for ts in rng]
    # print(rng)

    to_date_end = datetime(2016, 1, 4)
    from_date = datetime(2016, 1, 5)
    while from_date >= to_date_end:

        to_date = from_date - timedelta(1)

        print('{0} - {1}'.format(from_date.strftime('%Y-%m-%d'), to_date.strftime('%Y-%m-%d')))

        search_params = {'keyword': 'dengue', \
                         'since': to_date.strftime('%Y-%m-%d'), \
                         'until': from_date.strftime('%Y-%m-%d'), \
                         'location': 'Alta Floresta, Brazil', \
                         'radius': '3000km', \
                         'max_tweets': 3333}

        tote.search_and_collect_tweets(search_params, file_name)

        from_date = from_date - timedelta(1)
