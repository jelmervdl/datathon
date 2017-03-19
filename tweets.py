import re

def read_tweets(filename):
    tweets = []
    tweet = None
    for line in open(filename, 'r'):
        # A single line
        match = re.match(r'^(\d+)\t(\d+)\t([^\t]+?)\t(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\r\n', line)
        if match:
            tweet = dict(user=int(match.group(1)), tweet_id=int(match.group(2)), text=match.group(3), datetime=match.group(4))
            tweets.append(tweet)
            continue
        
        # Tweet start
        match = re.match(r'^(\d+)\t(\d+)\t(.+(?!\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})+?)\r\n$', line)
        if match:
            tweet = dict(user=int(match.group(1)), tweet_id=int(match.group(2)), text=match.group(3))
            continue
        
        # Tweet end
        match = re.match(r'^(.+)\t(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\r\n$', line)
        if match:
            tweet['text'] += match.group(1)
            tweet['datetime'] = match.group(2)
            tweets.append(tweet)
            tweet = None
        else:
            if tweet is None:
                print(repr(line))
                raise Exception("No Tweet")
            tweet['text'] += line
    return tweets

if __name__ == '__main__':
    from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
    from collections import defaultdict
    from datetime import datetime
    import pandas as pd
    import sqlite3

    tweets = read_tweets('data/social/twitter_cikm_2010/training_set_tweets.txt')

    isis_tweets = pd.read_csv('data/social/how-isis-uses-twitter/tweets.csv')

    for tweet in tweets:
        tweet['user'] = str(tweet['user'])

    def parse_datetime(time):
        return str(datetime.strptime(time, "%m/%d/%Y %H:%M"))

    for idx, isis_tweet in isis_tweets.iterrows():
        tweets.append({
            'datetime': parse_datetime(isis_tweet['time']),
            'text': isis_tweet['tweets'],
            'user': isis_tweet['username'],
        })

    for tweet in tweets:
        for key in tweet.keys():
            tweet[key] = unicode(tweet[key])

    conn = sqlite3.connect('tweets.db')

    c = conn.cursor()

    c.execute('''CREATE TABLE tweets
             (datetime text, text text, user text)''')

    c.executemany("INSERT INTO tweets (datetime, text, user) VALUES (?, ?, ?)", ((t['datetime'], t['text'], t['user']) for t in tweets))

    con.close()

