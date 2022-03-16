import tweepy
import pandas as pd
from datetime import datetime
import pytz
import re


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
    mykeys = open("keys.txt", "r").readlines()
    
    api_key = mykeys[0].rstrip()
    api_key_secret = mykeys[1].rstrip()
    access_token = mykeys[2].rstrip()
    access_token_secret = mykeys[3].rstrip()
    
    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    
    if language == "eng":
        timezone = "US/Pacific"
        start_date = datetime(2021, 6, 19)
        query = "Wordle "
    else:
        timezone = "Europe/Madrid"
        start_date = datetime(2022, 1, 6)
        query = "Wordle (ES) #"
        
    #if wordle_id not given, take today's id
    if wordle_id is None:
        wordle_start = pytz.timezone(timezone).localize(start_date)
        now = pytz.utc.localize(datetime.now()).astimezone(pytz.timezone(timezone))

        wordle_id = (now-wordle_start).days
    
    wordle_tweets = []
    search_term = f"{query}{wordle_id}"
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