from got3.manager import TweetCriteria
from got3.manager import TweetManager

import re

class TwitterOldTweetsExtractor:

    def search_and_collect_tweets(self, params):

        file_name = 'old_tweets.csv'

        tweetCriteria = TweetCriteria().setQuerySearch(params['keyword'])\
        .setSince(params['since'])\
        .setUntil(params['until'])\
        .setLocation(params['location'])\
        .setRadius(params['radius'])\
        .setMaxTweets(params['max_tweets'])

        tweets_count = 0

        saved_ids = self.get_saved_tweets_ids(file_name)

        oldest_tweet_date = ''

        for tweet in TweetManager.getTweets(tweetCriteria):
            if self.has_location_data(tweet) and tweet.id not in saved_ids:
                with open(file_name, 'a') as f:
                    f.write(self.tweeet_to_string(tweet) + '\n')

                oldest_tweet_date = tweet.formatted_date

                tweets_count += 1

                if tweets_count % 10 == 0:
                    print('Collected {0} tweets'.format(tweets_count))

        print('Reached the limit of {0} searched tweets'.format(params['max_tweets']))
        print('Oldest saved tweet date is : {0}'.format(oldest_tweet_date))

    def has_location_data(self, tweet):
        return tweet.geo != None and tweet.geo.strip() != ''

    def tweeet_to_string(self, tweet):
        if tweet.text:
            tweet.text = re.sub('"', '', tweet.text)

        attributes = [tweet.id, str(tweet.date), \
                      '"' + tweet.formatted_date + '"',
                      '"' + tweet.geo + '"',\
                      '"' + tweet.text + '"']

        return ','.join(attributes)

    def get_saved_tweets_ids(self, file_name):
        ids = []
        with open(file_name, 'r') as f:
            for line in f:
                tweet_id = line.split(',')[0]
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

    tote = TwitterOldTweetsExtractor()
    tote.search_and_collect_tweets(search_params)
