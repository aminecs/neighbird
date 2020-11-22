from twitivity import Activity

account_activity = Activity()
account_activity.register_webhook("https://29f556047377.ngrok.io/payload")
account_activity.subscribe()
