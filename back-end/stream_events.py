from twitivity import Event
import json, bot_interaction, user

recipient_user = user.User("1234")


class StreamEvent(Event):
    CALLBACK_URL: str = "https://29f556047377.ngrok.io/payload"

    def on_data(self, data: json) -> None:
        event_type = list(data.keys())[1]
        if "direct_message_events" == event_type:
            if data["direct_message_events"][0]["message_create"]["sender_id"] != '1328476914600833025':
                recipient_user.user_id = data["direct_message_events"][0]["message_create"]["sender_id"]
                bot_interaction.processData(data, recipient_user)


stream_events = StreamEvent()
stream_events.listen()
