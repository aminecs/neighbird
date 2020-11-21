import twitterAPI_calls

""""
    Defining the both answers to specific messages

"""

address_options = [
    {
        "label": "Share my address",
        "description": "Let us get your address to connect you with your community",
        "metadata": "external_id_1"
    },
    {
        "label": "Why do you need this?",
        "description": "Want to know more?",
        "metadata": "external_id_2"
    }
]

community_options = [
    {
        "label": "Chat",
        "description": "I would like to chat with someone in my community",
        "metadata": "external_id_1"
    },
    {
        "label": "Engage",
        "description": "I would like to engage in an activity",
        "metadata": "external_id_2"
    },
    {
        "label": "Community help",
        "description": "I would like to make a request for help",
        "metadata": "external_id_3"
    }
]

opt_in_options = [
    {
        "label": "Sign me up",
        "description": "Join the community",
        "metadata": "external_id_1"
    },
    {
        "label": "Don't sign me up",
        "description": "Skip this stage",
        "metadata": "external_id_2"
    }
]

time_options = [
    {
        "label": "Now",
        "description": "Get someone as soon as possible",
        "metadata": "external_id_1"
    },
    {
        "label": "Later",
        "description": "I can wait",
        "metadata": "external_id_2"
    }
]


def processMessage(msg_received):
    msg_received = msg_received.lower()
    if msg_received == "community":
        # TO DO IMPLEMENT LOGIC FOR NEW USERS
        return "Community is a place where you can connect with other Tweeters in your neighbourhood. Since it’s your " \
               "first time here, we’ll need you to share your address ", address_options
    if msg_received == "why do you need this?":
        return "Security and trust is at the forefront of what we do here at Twitter. We need to verify that you’re a " \
               "real user to ensure that we keep the community a safe space for everyone. Your personal details or " \
               "address will not be shared with anyone. ", []
    if msg_received == "share my address":
        city = "Glasgow, Scotland"  # TO DO: GET CITY OF THE USER
        return f"Thanks for verifying your address, looks like you are located in {city}. Would you like to " \
               "'chat' with someone from your area, 'engage in an activity' (ie. football, tennis, scrabble) or " \
               "'request help' (ie. toilet paper, grocery shopping, help with homework) ?", community_options
    if msg_received == "community help":
        return "The greatness of a Community is most accurately measured by the compassionate actions of its members." \
               "Will you also opt in to respond to community requests?", opt_in_options
    if msg_received == "sign me up":
        return "Thank you for opting in. How soon would you like to chat with a fellow Tweeter on your current request?", time_options
    if msg_received == "now":
        return "Hang tight, we’re searching for other birds with the same criteria…", []
    else:
        return "I am clueless here. The dream team is working on it.", []


def getMessageReceived(data):
    return data["direct_message_events"][0]["message_create"]["message_data"]['text']


def getSender(data):
    return data["direct_message_events"][0]["message_create"]["sender_id"]


def processData(data):
    msg_received = getMessageReceived(data)
    recipient_id = getSender(data)

    answer, options = processMessage(msg_received)
    if not options:
        twitterAPI_calls.send_DM(recipient_id, answer)
    else:
        twitterAPI_calls.sendQR_DM(recipient_id, answer, options)
