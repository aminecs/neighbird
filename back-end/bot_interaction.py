import twitterAPI_calls

""""
    Defining the both answers to specific messages

"""


def processMessage(msg_received):
    msg_received = msg_received.lower()
    if msg_received == "community":
        # TO DO IMPLEMENT LOGIC FOR NEW USERS
        return "Community is a place where you can connect with other Tweeters in your neighbourhood. Since it’s your " \
               "first time here, we’ll need you to share your address "
    if msg_received == "why do you need this ?":
        return "Security and trust is at the forefront of what we do here at Twitter. We need to verify that you’re a " \
               "real user to ensure that we keep the community a safe space for everyone. Your personal details or " \
               "address will not be shared with anyone. "
    if msg_received == "Address":
        city = "Glasgow, Scotland"  # TO DO: GET CITY OF THE USER
        return f"Thanks for verifying your address, looks like you are located in {city}. Would you like to " \
               "'chat' with someone from your area, 'engage in an activity' (ie. football, tennis, scrabble) or " \
               "'request help' (ie. toilet paper, grocery shopping, help with homework) ?"
    if msg_received == "request":
        return "The greatness of a Community is most accurately measured by the compassionate actions of its members." \
                "Will you also opt in to respond to community requests?"
    if msg_received == "sign me up":
        return "Thank you for opting in. How soon would you like to chat with a fellow Tweeter on your current request?"
    if msg_received == "yes, find me someone":
        return "Hang tight, we’re searching for other birds with the same criteria…"
    else:
        return "I am clueless here. The dream team is working on it."


def getMessageReceived(data):
    return data["direct_message_events"][0]["message_create"]["message_data"]['text']


def getSender(data):
    return data["direct_message_events"][0]["message_create"]["sender_id"]


def processData(data):
    msg_received = getMessageReceived(data)
    recipient_id = getSender(data)

    answer = processMessage(msg_received)
    twitterAPI_calls.sendDM(recipient_id, answer)
