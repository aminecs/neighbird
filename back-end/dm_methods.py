import config, bot_behaviour_init


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


def send_WelcomeDM(recipient_id):
    oauth = config.setUpAuth()
    message_data = bot_behaviour_init.getWelcomeMessage(oauth).json()["welcome_message"]["message_data"]
    return oauth.post("https://api.twitter.com/1.1/direct_messages/events/new.json",
                      json={"event": {"type": "message_create",
                                      "message_create": {"target": {"recipient_id": f"{recipient_id}"},
                                                         "message_data": message_data}}})
