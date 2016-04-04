import json
from collections import defaultdict
from datetime import datetime, timedelta


class TweetProcessor:
    
    def __init__(self):
        self.tweets_in_window = []
        self.ts_ending = None
        self.hs_graph = {}

    def is_in_time_window(self, tweet_a, tweet_b):
        t_1 = datetime.strptime(tweet_a['created_at'], "%a %b %d %H:%M:%S +0000 %Y")
        t_2 = datetime.strptime(tweet_b['created_at'], "%a %b %d %H:%M:%S +0000 %Y")
        if t_1+timedelta(seconds=60) > t_2:
            return True
        else:
            return False

    def compare(self, tweet_a, tweet_b):
        t_1 = datetime.strptime(tweet_a['created_at'], "%a %b %d %H:%M:%S +0000 %Y")
        t_2 = datetime.strptime(tweet_b['created_at'], "%a %b %d %H:%M:%S +0000 %Y")
        if t_1 > t_2:
            return True
        else:
            return False
    
    def insert_in_graph(self, tweet):
        # Insert an edge and update degree
        raw_hashtags = tweet['entities']['hashtags']
        hashtags = set()
        for hs in tweet['entities']['hashtags']:
            hashtags.add(hs['text'])
        hashtags = list(hashtags)
        for i in xrange(len(hashtags)-1):
            word_i = hashtags[i]
            if word_i not in self.hs_graph:
                self.hs_graph[word_i] = defaultdict(lambda: 0)
            for j in xrange(i+1, len(hashtags)):
                word_j = hashtags[j]
                if word_j not in self.hs_graph:
                    self.hs_graph[word_j] = defaultdict(lambda: 0)
                self.hs_graph[word_i][word_j] += 1
                self.hs_graph[word_j][word_i] += 1

    def delete_in_graph(self, tweet):
        # Delete an edge and update degree
        raw_hashtags = tweet['entities']['hashtags']
        hashtags = set()
        for hs in tweet['entities']['hashtags']:
            hashtags.add(hs['text'])
        hashtags = list(hashtags)
        for i in xrange(len(hashtags)-1):
            word_i = hashtags[i]
            for j in xrange(i+1, len(hashtags)):
                word_j = hashtags[j]
                if self.hs_graph[word_i][word_j] == 1:
                    del self.hs_graph[word_i][word_j]
                    if len(self.hs_graph[word_i]) == 0:
                        del self.hs_graph[word_i]
                    del self.hs_graph[word_j][word_i]
                    if len(self.hs_graph[word_j]) == 0:
                        del self.hs_graph[word_j]
                else:
                    self.hs_graph[word_i][word_j] -= 1
                    self.hs_graph[word_j][word_i] -= 1

    def delete_and_update_degree(self):
        # Find all the timeout tweets and delete those tweets 
        new_tweets = []
        for tweet in self.tweets_in_window:
            if self.is_in_time_window(tweet, self.ts_ending):
                # this tweet is in window
                new_tweets.append(tweet)
            else:
                # delete this tweet from graph
                self.delete_in_graph(tweet)
        self.tweets_in_window = new_tweets
    
    def cal_degree(self):
        word_count = len(self.hs_graph)
        degree_sum = 0
        for word_a in self.hs_graph:
            for word_b in self.hs_graph[word_a]:
                degree_sum += 1
        if word_count == 0:
            return 0
        return 1.0*degree_sum/word_count
    
    
    def is_valid(self, tweet):
        # Check if this tweet contains CreatedTime and hashtags
        if "created_at" not in tweet:
            return False
        if "entities" not in tweet or "hashtags" not in tweet['entities'] or len(tweet['entities']['hashtags']) == 0:
            return False
        return True
    
    
    def readTweet(self, input):
        # Every time return a tweet
        f = open(input)
        for line in f:
            yield json.loads(line)
    
    
    def execute(self, input, output):
        # Read tweets
        output_write = open(output, "w")
        for tweet in self.readTweet(input):
            # Check if this tweet is valid
            if not self.is_valid(tweet):
                continue
            if self.ts_ending is None:
                self.ts_ending = tweet
                self.tweets_in_window.append(tweet)
                self.insert_in_graph(tweet)
            else:
                if self.compare(self.ts_ending, tweet):
                    # ts_new > ts_ending
                    self.ts_ending = tweet
                    self.tweets_in_window.append(tweet)
                    self.insert_in_graph(tweet)
                    self.delete_and_update_degree()
                else:
                    if self.is_in_time_window(tweet, self.ts_ending):
                        # in window
                        self.tweets_in_window.append(tweet)
                        self.insert_in_graph(tweet)
                    else:
                        # ignore
                        pass
            avg_degree = self.cal_degree()
            output_write.write("{:0.2f}\n".format(avg_degree))

