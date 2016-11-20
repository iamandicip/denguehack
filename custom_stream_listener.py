from tweepy import Stream
from tweepy.streaming import StreamListener
import json
import codecs

import util_constants as uc

class CustomStreamListener(StreamListener):

    counter = 0

    def on_data(self, data):
        try:
            with open(uc.tweets_file_name, 'a') as fp:
                fp.write(data)

                self.counter += 1

                if self.counter % 10 == 0:
                    print('Collected {0} tweets'.format(self.counter))

            return True
        except BaseException as e:
            print('Error on_data: %s' % str(e))
        return True

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False

"""
    def convert_tweet_to_csv(self, tweet):
        tweet_attrs = ['timestamp_ms', 'created_at',\
                      'text', 'lang', 'favorite_count', 'retweet_count', 'id']
        json_tweet = json.loads(tweet)

        # user_data = json_tweet['user']
        # print('user_data : {0}'.format(user_data))
        tweet_values = []
        for a in tweet_attrs:

            # pass
            # if json_tweet[a]:
            print('{0} : {1}'.format(a, json_tweet[a]))
            tweet_values.extend(json_tweet[a])

        # place_data = json_tweet['place']
        # print('place_data : {0}'.format(place_data))
        # if place_data:
            # tweet_values.extend(place_data['country'])
            # tweet_values += place_data['name']
            # tweet_values += place_data['place_type']
            # tweet_values += place_data['bounding_box']['type']
            # tweet_values += place_data['bounding_box']['coordinates']

        # coordinates_data = json_tweet['coordinates']
        # print('coordinates_data : {0}'.format(coordinates_data))

        print(tweet_values)
        result = ','.join(tweet_values)

        return result
"""
