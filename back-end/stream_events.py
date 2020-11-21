from twitivity import Event
import json


class StreamEvent(Event):
    CALLBACK_URL: str = "http://c9c0e3b12930.ngrok.io/listener"

    def on_data(self, data: json) -> None:
        print(data)


stream_events = StreamEvent()
resp = stream_events.listen()

print(resp)
