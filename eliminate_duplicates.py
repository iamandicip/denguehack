import json

unique_ids = []

with open('historical_tweets.json', 'r') as f:
    ids = []
    for line in f:
        tweet = json.loads(line)
        if tweet['id'] not in ids:
            ids.append(tweet['id'])
            with open('historical_tweets_clean.json', 'a') as ff:
                ff.write(json.dumps(tweet)+ '\n')
