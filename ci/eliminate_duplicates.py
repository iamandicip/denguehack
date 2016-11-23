import json

def eliminate_duplicates(original_file, cleaned_file):
    print('Eliminating duplicates from file {0} and saving to {1}'.format(original_file, cleaned_file))
    with open(original_file, 'r') as f:
        ids = []
        total_tweets = 0

        for line in f:
            tweet = json.loads(line)
            total_tweets += 1
            if tweet['id'] not in ids:
                ids.append(tweet['id'])
                with open(cleaned_file, 'a') as ff:
                    ff.write(json.dumps(tweet)+ '\n')

        print('Found a total of {0} tweets, of which {1} unique'.format(total_tweets, len(ids)))

if __name__== '__main__':
    eliminate_duplicates('historical_tweets.json', 'historical_tweets_unique.json')
