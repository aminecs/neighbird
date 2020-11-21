import config


def createWelcomeMessage(oauth, new_welcome_message):
    response = oauth.post("https://api.twitter.com/1.1/direct_messages/welcome_messages/new.json",
                          json={
                              "welcome_message": {
                                  "name": "codechella_welcome-message 01",
                                  "message_data": {
                                      "text": f"{new_welcome_message}",
                                      "quick_reply": {
                                          "type": "options",
                                          "options": [
                                              {
                                                  "label": "Community",
                                                  "description": "Connect with your community",
                                                  "metadata": "external_id_1"
                                              },
                                              {
                                                  "label": "Topics",
                                                  "description": "Match with a fellow bird to chat about a topic",
                                                  "metadata": "external_id_2"
                                              }
                                          ]
                                      }
                                  }
                              }
                          }
                          )
    return response


def setWelcomeMessage(oauth, welcome_message_id):
    response = oauth.post("https://api.twitter.com/1.1/direct_messages/welcome_messages/rules/new.json",
                          json={
                              "welcome_message_rule": {
                                  "welcome_message_id": f"{welcome_message_id}"
                              }
                          })
    return response


def deleteWelcomeMessageRule(oauth, rule_id):
    return oauth.delete(
        f"https://api.twitter.com/1.1/direct_messages/welcome_messages/rules/destroy.json?id={rule_id}")


def getWelcomeMessageRules(oauth):
    return oauth.get("https://api.twitter.com/1.1/direct_messages/welcome_messages/rules/list.json")


def updateWelcomeMessage(oauth, new_welcome_message):
    prev_rule_id = getWelcomeMessageRules(config.setUpAuth()).json()["welcome_message_rules"][0]["id"]
    deleteWelcomeMessageRule(oauth, prev_rule_id)
    new_rule_id = createWelcomeMessage(oauth, new_welcome_message).json()["welcome_message"]['id']
    setWelcomeMessage(oauth, new_rule_id)
