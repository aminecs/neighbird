import tweepy
import os

consumer_key = os.environ.get('PUBLIC_KEY')  # Add your API key here
consumer_secret = os.environ.get('SECRET_KEY')


def authentication(consumer_key, consumer_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    # Redirect user to Twitter to authorize
    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        print('Error! Failed to get request token.')
    print(redirect_url)
    verifier = input("Please input the verifier: ")

    auth.get_access_token(verifier)
    return auth


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
    print(api.list_direct_messages(auth))


main()
