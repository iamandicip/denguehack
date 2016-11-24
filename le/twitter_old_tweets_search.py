from got3.manager import TweetCriteria
from got3.manager import TweetManager

from geo_locator import GeoLocator

import tweepy

import re

import sys

from datetime import datetime, timedelta


class TwitterOldTweetsExtractor:
    last_id = -1

    def search_and_collect_tweets(self, params, file_name):

        geo_locator = GeoLocator()

        tweetCriteria = TweetCriteria().setQuerySearch(params['keyword'])\
        .setSince(params['since'])\
        .setUntil(params['until'])\
        .setLocation(params['location'])\
        .setRadius(params['radius'])\
        .setMaxTweets(params['max_tweets'])

        tweets_count = 0
        count = 0

        saved_ids = self.get_saved_tweets_ids(file_name)

        oldest_tweet_date = None

        for tweet in TweetManager.getTweets(tweetCriteria):
            count = count + 1
            if self.has_location_data(tweet) and tweet.id not in saved_ids:
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
                    print('Retrieved {0} tweets. Collected {1} tweets'.format(count, tweets_count))
                    sys.stdout.flush()

        print('Reached the limit of {0} searched tweets'.format(params['max_tweets']))
        print('Oldest saved tweet date is : {0}'.format(oldest_tweet_date))

    def has_location_data(self, tweet):
        return tweet.geo != None and tweet.geo.strip() != ''

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

            print('There are {0} already saved tweets in file {1}'.format(len(ids), file_name))

            if len(ids) == 0:
                ids.append(self.last_id)
        except:
            ids.append(self.last_id)
            print('There are 0 already saved tweets in file {0}'.format(file_name))

        return ids



if __name__ == '__main__':
    search_params = {'keyword': '',\
                     'since' : '2016-09-01',\
                     'until' : '2016-10-09',\
                     'location' : 'Alta Floresta, Brazil',\
                     'radius' : '3000km',\
                     'max_tweets' : 9999}

    file_name = 'general_tweets.csv'

    tote = TwitterOldTweetsExtractor()

    now = datetime.now()
    week = datetime(2016, 1, 1)
    while week < now:
        week_start = str(week.date())
        week_end = str((week + timedelta(6)).date())

        print(week_start, week_end)
        search_params = {'keyword': '', \
                         'since': week_start, \
                         'until': week_end, \
                         'location': 'Alta Floresta, Brazil', \
                         'radius': '3000km', \
                         'max_tweets': 999}

        tote.search_and_collect_tweets(search_params, file_name)

        week = week + timedelta(7)
