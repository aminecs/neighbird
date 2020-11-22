import config

api = config.get_api()

print(api.list_direct_messages(count=10))
