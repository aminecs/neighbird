import tweepy
import os
from requests_oauthlib import OAuth1Session

consumer_key = os.environ.get('PUBLIC_KEY')
consumer_secret = os.environ.get('SECRET_KEY')
access_token = os.environ.get('ACCESS_TOKEN')
access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')


# Barebone setup
def setUpAuth():
    oauth = OAuth1Session(consumer_key,
                          client_secret=consumer_secret,
                          resource_owner_key=access_token,
                          resource_owner_secret=access_token_secret)

    return oauth


# Tweepy setup
def get_api():
    # setup authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api

#print(setUpAuth().get("https://api.twitter.com/1.1/users/show.json?user_id=1172192131118784514").json()["screen_name"])