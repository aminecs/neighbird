from twitivity import Event
import json

class StreamEvent(Event):
     CALLBACK_URL: str = "https://29f556047377.ngrok.io/payload"

     def on_data(self, data: json) -> None:
         print(data.keys())

stream_events = StreamEvent()
stream_events.listen()