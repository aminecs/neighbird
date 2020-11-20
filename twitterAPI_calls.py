import tweepy
import os

consumer_key = os.environ.get('PUBLIC_KEY')  # Add your API key here
consumer_secret = os.environ.get('SECRET_KEY')


def authentication(consumer_key, consumer_secret):
    return tweepy.AppAuthHandler(consumer_key, consumer_secret)


# OAuth2 test method
def getTweets(api):
    """Return tweet containing the codechella hashtag.

    You can modify the query by changing the parameter passed to q
    """
    for tweet in tweepy.Cursor(api.search, q='#Codechella').items(10):
        print("\n Next tweet: \n")
        print(tweet.text)



def main():
    auth = authentication(consumer_key, consumer_secret)
    api = tweepy.API(auth)
    getTweets(api)


main()
