import config

def createWelcomeMessage(new_welcome_message):
    response = oauth.post("https://api.twitter.com/1.1/direct_messages/welcome_messages/new.json",
              json={
                      "welcome_message" : {
                        "name": "codechella_welcome-message 01",
                        "message_data": {
                          "text": "Welcome this is the dream team!"
                          }
                        }
                      }
                    )
    return response