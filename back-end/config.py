import tweepy
import os
from requests_oauthlib import OAuth1Session

consumer_key = os.environ.get('PUBLIC_KEY')
consumer_secret = os.environ.get('SECRET_KEY')
access_token = os.environ.get('ACCESS_TOKEN')
access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')

# Barebone setup
def setupAuth():
    oauth = OAuth1Session(consumer_key,
                          client_secret=consumer_secret,
                          resource_owner_key=access_token,
                          resource_owner_secret=access_token_secret)

    return oauth
    # response = oauth.post("https://api.twitter.com/1.1/direct_messages/welcome_messages/new.json",
    #           json={
    #                   "welcome_message" : {
    #                     "name": "codechella_welcome-message 01",
    #                     "message_data": {
    #                       "text": "Welcome this is the dream team!"
    #                       }
    #                     }
    #                   }
    #                 )
    # response = oauth.post("https://api.twitter.com/1.1/direct_messages/welcome_messages/rules/new.json",
    #                       json={
    #                               "welcome_message_rule": {
    #                                 "welcome_message_id": "1330165063995551752"
    #                               }
    #                             })
    #

# Tweepy setup
def get_api():
    # setup authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    response = auth.post("https://api.twitter.com/1.1/direct_messages/welcome_messages/new.json",
              json={"message_data": {"text": "Hello World!"}})
    print(response.text)
    api = tweepy.API(auth)
    return api

setupAuth()