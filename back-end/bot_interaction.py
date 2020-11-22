import dm_methods, models

""""
    Defining the both answers to specific messages

"""


def processMessage(msg_received, recipient_user, new_user, inquiry):  # TODO Add param: user, new_user
    msg_received = msg_received.lower()
    # Community bit
    if msg_received == "community":
        if new_user:  # New user welcome message for community
            return "Community is a place where you can connect with other Tweeters in your neighbourhood. " \
                   "Since it’s your first time here, we’ll need you to share your address ", address_options
        else:
            return "Welcome back ! Community is a place where you can connect with other Tweeters in your" \
                   "neighbourhood.", community_options
    if msg_received == "why do you need this?":
        return "Security and trust is at the forefront of what we do here at Twitter. We need to verify that you’re " \
               "a real user to ensure that we keep the community a safe space for everyone. Your personal details or " \
               "address will not be shared with anyone. Do you want to continue?", security_options
    if msg_received == "share address" or msg_received == "join the community":
        return "Please enter your address", []
    if msg_received == "abort":
        return "We are sorry to see you go. We wish you the best and I appreciate the time you spent with us.", []
    if msg_received == "chat":
        inquiry.set_inquiry_type(1)
        return "Is there something in particular you want to chat about?", chat_options
    if msg_received == "engage":
        inquiry.set_inquiry_type(2)
        return "What activity would you like to engage in?", []
    if msg_received == "community help":
        inquiry.set_inquiry_type(3)
        if not recipient_user.available_to_help:
            return "The greatness of a Community is most accurately measured by the compassionate actions " \
                   "of its members. Will you also opt in to respond to community requests?", opt_in_options
        else:
            return "How soon would you like to chat with a fellow Tweeter on your current request?", time_options
    if msg_received == "sign me up":
        recipient_user.available_to_help = True
        return "Thank you for opting in. How soon would you like to chat with a fellow Tweeter on your current " \
               "request?", time_options
    if msg_received == "Don't sign me up":
        recipient_user.available_to_help = False
        return "No worries. How soon would you like to chat with a fellow Tweeter on your current " \
               "request?", time_options
    if msg_received == "now":
        return "Hang tight, we’re searching for other birds with the same criteria…", []
    if msg_received == "later":
        return "All right, we will get back to you soon.", []
    # Topics bit
    if msg_received == "topics":
        inquiry.set_inquiry_type(1)
        return "Topics is the space where we can match you with a fellow Tweeter to chat about a specific topic" \
               "", topic_options
    if msg_received == "submit a topic":
        return "What topic are you interested in?", []
    if msg_received == "trending topics":
        return "The trending topics are: " + ', '.join(getTrendingTopics()), trending_topics_options
    if msg_received in map(lambda x: x.lower(), getTrendingTopics()):
        inquiry.set_inquiry_str(msg_received)
        return f"Hang tight, we’re searching for other birds interested in {msg_received}…", []
    # Edge cases
    if msg_received == "hi":
        return "hi", []
    if msg_received == "ok":
        return "ok", []
    else:
        if recipient_user.last_msg == "engage":
            inquiry.set_inquiry_str(msg_received)
            return f"Sounds good, we will try to find someone who wants to engage in this activity ({msg_received})." \
                   f"", []
        if recipient_user.last_msg == "submit a topic":
            inquiry.set_inquiry_str(msg_received)
            return f"Hang tight, we’re searching for other birds interested in {msg_received}…", []
        if recipient_user.last_msg == "join the community":
            return "Thank you for joining the community. Your records are stored safely.", []
        if recipient_user.last_msg == "share address":
            recipient_user.set_address(msg_received)
            location = recipient_user.location_info["data"]["city"] + ", " + recipient_user.location_info["data"][
                "country"]
            return f"Thanks for verifying your address, looks like you are located in {location}. Would you like to " \
                   "'chat' with someone from your area, 'engage in an activity' (ie. football, tennis, scrabble) or " \
                   "'request help' (ie. toilet paper, grocery shopping, help with homework) ?", community_options
        print(recipient_user.last_msg)
        print(msg_received)
        return "I am clueless here. The dream team is working on it.", []


def isNewUser(recipient_user):
    if recipient_user.location_info["data"] is None:
        return True
    else:
        return False


def getTrendingTopics():
    topics = ["Real Madrid", "Codechella", "Beckham"]
    return topics


def getMessageReceived(data):
    return data["direct_message_events"][0]["message_create"]["message_data"]['text']


def getSender(data):
    return data["direct_message_events"][0]["message_create"]["sender_id"]


def processData(data, inquiry):
    msg_received = getMessageReceived(data)
    recipient_id = getSender(data)
    recipient_user = models.User.find_user(recipient_id)
    new_user = isNewUser(recipient_user)
    answer, options = processMessage(msg_received, recipient_user, new_user, inquiry)
    recipient_user.set_last_msg(msg_received.lower())
    if answer == "hi":
        dm_methods.send_WelcomeDM(recipient_id)
    elif answer == "ok":
        dm_methods.send_DM(recipient_id, "cool")
    else:
        if not options:
            dm_methods.send_DM(recipient_id, answer)
        else:
            dm_methods.sendQR_DM(recipient_id, answer, options)


address_options = [
    {
        "label": "Share address",
        "description": "Let us get your address to connect you",
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
        "description": "I would like to chat with someone here",
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
    },
    {
        "label": "Join the community",
        "description": "I would like to join the community",
        "metadata": "external_id_4"
    }
]

chat_options = [
    {
        "label": "General chat",
        "description": "I just want to have a general chat",
        "metadata": "external_id_1"
    },
    {
        "label": "Submit a topic",
        "description": "I would like to talk about a topic",
        "metadata": "external_id_2"
    }
]

security_options = [
    {
        "label": "Share address",
        "description": "Yes, I would like to share my address",
        "metadata": "external_id_1"
    },
    {
        "label": "Abort",
        "description": "No, I don't want to share my address",
        "metadata": "external_id_2"
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

topic_options = [
    {
        "label": "Submit a topic",
        "description": "I want to submit my own topic",
        "metadata": "external_id_1"
    },
    {
        "label": "Trending topics",
        "description": "I want to see the trending topics",
        "metadata": "external_id_2"
    }
]

trending_topics_options = [
    {
        "label": getTrendingTopics()[0],
        "description": f"I want to chat about {getTrendingTopics()[0]}",
        "metadata": "external_id_1"
    },
    {
        "label": getTrendingTopics()[1],
        "description": f"I want to chat about {getTrendingTopics()[1]}",
        "metadata": "external_id_2"
    },
    {
        "label": getTrendingTopics()[2],
        "description": f"I want to chat about {getTrendingTopics()[2]}",
        "metadata": "external_id_3"
    },
    {
        "label": "Submit a topic",
        "description": "I want to submit my own topic",
        "metadata": "external_id_4"
    }
]
