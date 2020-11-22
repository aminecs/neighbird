from twitivity import Activity

account_activity = Activity()
account_activity.register_webhook("http://c9c0e3b12930.ngrok.io")
account_activity.subscribe()
