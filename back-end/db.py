import os
from pymongo import MongoClient
from pprint import pprint

db = None

def connect():
    """
    Connects to a mongodb uri
    """
    global db
    if not db:
        MONGO_ATLAS_URI = os.environ.get("MONGO_ATLAS_URI", "")
        client = MongoClient(MONGO_ATLAS_URI)
        db = client["community"] # create a db called community
    if db:
        print("Connected to db")
    else:
        print("Couldn't connect")


def getDB():
    """
    Returns DB object that can be used by the models
    """
    global db
    if not db:
        connect()
    return  db

if __name__ == "__main__":
    connect()