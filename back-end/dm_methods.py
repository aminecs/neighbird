import config


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
