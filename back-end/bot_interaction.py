import twitterAPI_calls

""""
    Defining the both answers to specific messages

"""


def processMessage(msg_received):
    if msg_received == "Community":
        return "Ok"
    else:
        return "Topics"


def getMessageReceived(data):
    return data["direct_message_events"][0]["message_create"]["message_data"]['text']


def getSender(data):
    return data["direct_message_events"][0]["message_create"]["sender_id"]


def processData(data):
    msg_received = getMessageReceived(data)
    recipient_id = getSender(data)

    answer = processMessage(msg_received)
    twitterAPI_calls.sendDM(recipient_id, answer)
