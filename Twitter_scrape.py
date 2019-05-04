
# coding: utf-8

# In[7]:


import re 
import numpy as np
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob
import pandas as pd 
import matplotlib.pyplot as plt
import nltk


class TwitterClient(object): 

    def __init__(self): 
        #Intructions to find your Keys and tokens 
        # apps.twitter.com ---> create an account or log in ----> Get keys and tokens from application settings.
        # keys and tokens from the Twitter Console 
        #API requests on your own account's behalf. Do not share your access token secret with anyone.
        
        consumer_key = "FHFptYK0XrSGGsSrcd5DcCncK"
        consumer_secret = "BrjqHKBoX1GJWJxGoxXCbZY2wnZonjMXwUhWA0r9QZr1YnYr7I"
        access_token = "935589591364653057-vMt0hV3cVH8XcRzgEuH3DcqX2b2kTbo"
        access_token_secret = "EGxGT5vO1sjKgIDpQmu00o5nEQR2TCFYXMPHKiZaqCnkX"
  
        # We try to attempt authentication 
        try: 
            # First we create OAuthHandler object 
            self.auth = OAuthHandler(consumer_key, consumer_secret) 
            # setting access token and secret 
            self.auth.set_access_token(access_token, access_token_secret) 
            # creating tweepy API object to fetch tweets 
            self.api = tweepy.API(self.auth) 
        except: 
            print("Error: Authentication Failed") 
 

    def plain_tweet(self, tweet): 
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 
  
    def fetch_tweet_sentiment(self, tweet): 
        ''' 
        Utility function to classify sentiment of passed tweet 
        using textblob's sentiment method 
        '''
        # create TextBlob object of passed tweet text 
        analysis = TextBlob(self.plain_tweet(tweet)) 
        # set sentiment 
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        else: 
            return 'negative'
  
    def extract_tweets(self, query, count = 10): 
        # empty list to store parsed tweets 
        tweets = [] 
  
        try: 
            # call twitter api to fetch tweets 
            all_fetched_tweets = self.api.search(q = query, count = count) 
  
            # parsing tweets one by one 
            for tweet in all_fetched_tweets: 
                # empty dictionary to store required params of a tweet 
                parsed_tweet = {} 
  
                # saving text of tweet 
                parsed_tweet['text'] = tweet.text 
                # saving sentiment of tweet 
                parsed_tweet['sentiment'] = self.fetch_tweet_sentiment(tweet.text) 
  
                # appending parsed tweet to tweets list 
                if tweet.retweet_count > 0: 
                    # if tweet has retweets, ensure that it is appended only once 
                    if parsed_tweet not in tweets: 
                        tweets.append(parsed_tweet) 
                else: 
                    tweets.append(parsed_tweet) 
  
            # return parsed tweets 
            return tweets 
  
        except tweepy.TweepError as e: 
            # print error (if any) 
            print("Error : " + str(e)) 


def main(): 
    # Enter the name in query (calling function) for sentiment analysis.
    # For eg : Warren Buffet
    
    # creating object of TwitterClient Class 
    api = TwitterClient() 
    # calling function to get tweets 
    tweets = api.extract_tweets(query = 'Warren Buffet', count = 280) 
  
    # picking positive tweets from tweets 
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
    # percentage of positive tweets 
    print("Percentage of positive tweets : {} %".format(100*len(ptweets)/len(tweets))) 
    # picking negative tweets from tweets 
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
    # percentage of negative tweets 
    print("Percentage of negative tweets : {} %".format(100*len(ntweets)/len(tweets)))
 
 
  
    # print first 5 positive tweets 
    print("\n\nPositive tweets:") 
    for tweet in ptweets[:10]: 
        print(tweet['text']) 
  
    # print first 5 negative tweets 
    print("\n\nNegative tweets:") 
    for tweet in ntweets[:10]: 
        print(tweet['text']) 
  
    
if __name__ == "__main__":
    main()

    
## References
## https://www.ijcaonline.org/research/volume125/number3/dandrea-2015-ijca-905866.pdf
## https://textblob.readthedocs.io/en/dev/quickstart.html#sentiment-analysis

