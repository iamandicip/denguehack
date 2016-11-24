from got3.manager import TweetCriteria
from got3.manager import TweetManager

from geo_locator import GeoLocator

import tweepy

import re

class TwitterOldTweetsExtractor:

    def search_and_collect_tweets(self, params, file_name):

        geo_locator = GeoLocator()

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
            if self.has_location_data(tweet) and tweet.id not in saved_ids:
                with open(file_name, 'a', encoding='utf8') as f:
                    try:
                        f.write(self.tweeet_to_string(tweet, geo_locator) + '\n')
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

    def tweeet_to_string(self, tweet, geo_locator):
        attributes = []

        if tweet.text:
            tweet.text = re.sub('"', '', tweet.text)
            tweet.text = re.sub(',', '', tweet.text)

        if tweet.geo:
            lat, lng = geo_locator.get_coordinates_for_location(tweet.geo)

            attributes = ['"' + str(tweet.id) + '"', \
                          '"' + str(tweet.date) + '"', \
                          '"' + tweet.geo + '"',\
                          '"' + str(lat) + '"',\
                          '"' + str(lng) + '"',\
                          '"' + tweet.text + '"']

        return ','.join(attributes)

    def get_saved_tweets_ids(self, file_name):
        ids = []
        with open(file_name, 'r', encoding='utf8') as f:
            for line in f:
                tweet_id = line.split(',')[0]
                tweet_id = re.sub('"', '', tweet_id)
                if tweet_id.isdigit():
                    ids.append(tweet_id)

        print('There are {0} already saved tweets in file {1}'.format(len(ids), file_name))

        return ids


if __name__ == '__main__':
    search_params = {'keyword' : 'dengue OR Dengue',\
                     'since' : '2016-09-01',\
                     'until' : '2016-11-17',\
                     'location' : 'Alta Floresta, Brazil',\
                     'radius' : '3000km',\
                     'max_tweets' : 9999}

    file_name = 'old_tweets.csv'

    tote = TwitterOldTweetsExtractor()

    tote.search_and_collect_tweets(search_params, file_name)
