import tweepy
import config


# OAuth2 test method
def getTweets(api):
    """Return tweet containing the codechella hashtag.

    You can modify the query by changing the parameter passed to q
    """
    for tweet in tweepy.Cursor(api.search, q='#Codechella').items(10):
        print("\n Next tweet: \n")
        print(tweet.text)


def main():
    api = config.get_api()
    print(api.list_direct_messages())


#print(sendDM("1172192131118784514", "Test").text)
