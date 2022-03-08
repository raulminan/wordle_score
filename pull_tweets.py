
import tweepy
import pandas as pd
import numpy as np
from collections import Counter
from datetime import datetime
import os
import pytz
import re
import time



def pull_tweets(language="esp", amount=10, wordle_id=None):
    """
    Pulls tweets
    
    :args:
        :arg amount: amount of tweets to pull
        :wordle_id: custom wordle ID if you don't want to use today's wordle
        
    :returns:
        dataframe with all the tweets
    
    """
    
    #API identification
    mykeys = open("C:/Users/raulm/Desktop/Raúl/#Formación/#Programación/Python/python_work/wordle_score/keys.txt", "r").readlines()
    
    api_key = mykeys[0].rstrip()
    api_key_secret = mykeys[1].rstrip()
    access_token = mykeys[2].rstrip()
    access_token_secret = mykeys[3].rstrip()
    
    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    
    #if language == "eng":
        #future implementation

    
    #if wordle_id not given, take today's id
    if wordle_id is None:
        wordle_start = pytz.timezone("Europe/Madrid").localize(datetime(2022, 1, 6))
        now = pytz.utc.localize(datetime.now()).astimezone(pytz.timezone("Europe/Madrid"))

        wordle_id = (now-wordle_start).days
    
    wordle_tweets = []
    search_term = f"Wordle (ES) #{wordle_id}"
    tweet_amount = amount
    cursor = tweepy.Cursor(api.search_tweets, q=search_term)
    tweets = list(cursor.items(tweet_amount))
    
    #find tweets with a wordle id
    for tweet in tweets:
        text = re.findall(f"[1-6X]/6", tweet.text)#get score
        text_str = "".join(str(x) for x in text)
        wordle_tweets.append((wordle_id, text_str))
    
    #store tweets in a dataframe
    new_tweets_df = pd.DataFrame([tweet for tweet in wordle_tweets],
            columns=["wordle_id","tweet_text"])

    return new_tweets_df