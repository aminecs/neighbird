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


def sendQR_DM(recipient_id, msg, options):
    oauth = config.setUpAuth()
    return oauth.post("https://api.twitter.com/1.1/direct_messages/events/new.json",
                      json={"event": {"type": "message_create",
                                      "message_create": {"target": {"recipient_id": f"{recipient_id}"},
                                                         "message_data": {"text": f"{msg}",
                                                                          "quick_reply": {
                                                                              "type": "options",
                                                                              "options": options
                                                                          }
                                                                          }
                                                         }
                                      }
                            }
                      )


def send_DM(recipient_id, msg):
    oauth = config.setUpAuth()
    return oauth.post("https://api.twitter.com/1.1/direct_messages/events/new.json",
                      json={"event": {"type": "message_create",
                                      "message_create": {"target": {"recipient_id": f"{recipient_id}"},
                                                         "message_data": {"text": f"{msg}"}
                                                         }
                                      }
                            }
                      )


def main():
    api = config.get_api()
    print(api.list_direct_messages())


#print(sendDM("1172192131118784514", "Test").text)
