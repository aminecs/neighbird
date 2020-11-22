from twitivity import Activity

account_activity = Activity()
account_activity.register_webhook("https://c39615499b6a.ngrok.io/payload")
account_activity.subscribe()
