from twitivity import Event
import json, bot_interaction


class StreamEvent(Event):
    CALLBACK_URL: str = "https://29f556047377.ngrok.io/payload"

    def on_data(self, data: json) -> None:
        event_type = list(data.keys())[1]
        if "direct_message_events" == event_type:
            if data["direct_message_events"][0]["message_create"]["sender_id"] != '1328476914600833025':
                bot_interaction.processMessage(data["direct_message_events"][0]["message_create"]["message_data"]['text'])


stream_events = StreamEvent()
stream_events.listen()
