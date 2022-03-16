from pull_tweets import *
import matplotlib.pyplot as plt

def main():
    #get tweets
    tweets = pull_tweets("eng", 10_000)
    tweet_amount = len(tweets['tweet_text'])
    
    #drop if format isn't correct
    mask = tweets["tweet_text"].str.len() == 3
    tweets = tweets.loc[mask]

    #plot
    tweets['tweet_text'].value_counts().astype(int).sort_index().plot(kind='bar', 
                                                                      width=1.0)

    total = tweets['tweet_text'].value_counts().sum()
    mean = round((tweets['tweet_text'].value_counts()["X/6"] * 0 + 
            tweets['tweet_text'].value_counts()["1/6"] * 1 +
            tweets['tweet_text'].value_counts()["2/6"] * 2 +
            tweets['tweet_text'].value_counts()["3/6"] * 3 +
            tweets['tweet_text'].value_counts()["4/6"] * 4 +
            tweets['tweet_text'].value_counts()["5/6"] * 5 +
            tweets['tweet_text'].value_counts()["6/6"] * 6)/(total - tweets['tweet_text'].value_counts()["X/6"]), 3)
    
    if tweets["wordle_id"][1] < 200:
        plt.title(
            f"Distribución para el Wordle {tweets['wordle_id'][1]}: Puntuación media = {mean}\n n={tweet_amount}")
        plt.show()
    
    else:
        plt.title(
            f"Distribution for Wordle {tweets['wordle_id'][1]}: Average Score = {mean}\n n={tweet_amount}")
        plt.show()

if __name__ == '__main__':
    main()