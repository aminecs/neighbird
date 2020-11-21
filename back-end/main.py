import configure, stream_events
import bot_behaviour_init, config


def setUpStreamingAPI():
    stream_events
    configure


def setUpBot():
    oauth = config.setUpAuth()
    response = bot_behaviour_init.updateWelcomeMessage(oauth,
                                                  "Hi, I’m Bird Bot. I am here to help you connect and start a "
                                                  "conversation "
                                                  "with other fellow Tweeters. You can start by selecting either "
                                                  "‘Community’ "
                                                  "or ‘Topics'")
    print(response)


setUpBot()
