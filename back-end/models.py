import db as db_
import geolocation as geo
import pprint
from geolocation import distanceBetweenLocations


class User:
    """
    Represents a user of birdbot
    """

    def __init__(self, user_id):
        """
        """
        self.user_id = user_id  # (str) user id of Twitter user
        self.inquiries = []  # (list) list of inquiry objects
        self.location_info = {"data": None, "error": None}  # (dict) typical location information (lon/lat, city, region, country, etc)
        self.address = None  # (str) string of original address user gives to bot
        self.available_to_help = False  # (bool) indicates whether this user is available to help with a request from another user
        self.last_msg = None

    def set_address(self, address):
        """
        Set the address of the user and then save to db
        """
        self.address = address
        self.location_info = geo.getLocationInfo(address)
        print("Here: \n")
        print(geo.getLocationInfo(address))
        print("Over.")
        print("Adding address:")
        self.save()

    def save(self):
        """
        Saves user to db.
        Creates user if not already in there.
        Else replaces the whole object
        TODO: Perform an update instead of a replace
        """
        User_collection = db_.getDB().user
        user = User_collection.find_one({"user_id": self.user_id})

        new_user = {
            "user_id": self.user_id,
            "location_info": None,
            "address": self.address,
            "available_to_help": self.available_to_help,
            "last_msg": self.last_msg,
            "inquiries": self.inquiries,

        }
        if self.location_info["data"] is not None:
            new_user["location_info"] = self.location_info["data"]
            new_user["location_data"] = {
                "type": "Point",
                "coordinates": [self.location_info["data"]["lng"], self.location_info["data"]["lat"]],
            }

        if not user:
            print("new user: {}".format(user))
            inserted_user = User_collection.insert_one(new_user)
            print("Inserted user: {}. Has mongoID: {}".format(new_user, inserted_user.inserted_id))
        else:
            # Update the user
            inserted_user = User_collection.replace_one({"_id": user["_id"]}, new_user)
            print("Replaced user object")

    def addInquiry(self, inquiries):
        self.inquiries.append(1)
        self.save()
        return self.inquiries

    def deleteInquiry(self):
        self.inquiries = []
        self.save()
        return self.inquiries

    def set_last_msg(self, last_msg):
        self.last_msg = last_msg
        self.save()
        return self.last_msg

    def __repr__(self):
        return "{}, {}, {}, {}, {}, {}".format(self.user_id, self.address, self.available_to_help, self.last_msg,
                                               self.location_info, self.inquiries)

    @staticmethod
    def find_user(twitter_id):
        """
        Gets a user from the DB based on their twitter id
        Returns either the object or None
        """
        User_collection = db_.getDB().user
        user = User_collection.find_one({"user_id": twitter_id})
        # print(user)
        twitter_user = None
        if user:
            "Adding to the user"
            twitter_user = User(user["user_id"])
            twitter_user.location_info = {
                "data": user["location_info"],
                "error": None
            }
            twitter_user.address = user["address"]
            twitter_user.available_to_help = user["available_to_help"]
            twitter_user.last_msg = user["last_msg"]
            twitter_user.inquiries = user["inquiries"]
        else:
            twitter_user = User(twitter_id)
        return twitter_user

    @staticmethod
    def get_all_users():
        # get all users
        User_collection = db_.getDB().user
        all_users = User_collection.find()
        users = []
        for user in all_users:
            users.append(User.dbuser2object(user))
        return users

    @staticmethod
    def delete_user(twitter_id):
        User_collection = db_.getDB().user
        no_deleted = User_collection.delete_one({"user_id": twitter_id})
        return no_deleted

    @staticmethod
    def dbuser2object(user):
        twitter_user = None
        if user:
            "Adding to the user"
            twitter_user = User(user["user_id"])
            twitter_user.location_info = {
                "data": user["location_info"],
                "error": None
            }
            twitter_user.address = user["address"]
            twitter_user.available_to_help = user["available_to_help"]
            twitter_user.last_msg = user["last_msg"]
            twitter_user.inquiries = user["inquiries"]
        return twitter_user

    def get_closest_users(self, radius=10):
        """
        Get the closest user to this user.
        Rank closest to furthest
        Limit is in miles

        Return user object from closest to object
        (Userobject, distance) distance in Km
        """
        # get all users
        User_collection = db_.getDB().user
        # grab all users from the same country
        all_users = User_collection.find({"location_info.country": self.location_info["data"]["country"]})

        locA = (self.location_info["data"]["lat"], self.location_info["data"]["lng"])
        neighbors = []
        for user in all_users:
            # check if it is within radius
            locB = (user["location_data"]["coordinates"][1], user["location_data"]["coordinates"][0])
            if locA == locB:
                continue
            distance_between = distanceBetweenLocations(locA, locB, False)
            if distance_between <= radius:
                neighbors.append((distance_between, User.dbuser2object(user)))

        # sort neighbors based on distance
        return sorted(neighbors)


def seed_users():
    usernames = ["keji_irl__", "trombone", "White House", "Radisson Blu"]
    addresses = ["2 olumoroti jaiyesimi street, Lagos", "19b Ogunyemi street, Victoria Island Lagos",
                 "9 Chapel street Yaba, Lagos", "1a Ozumba Mbadiwe Victoria Island Lagos"]

    for idx in range(len(usernames)):
        user = User(usernames[idx])
        user.set_address(addresses[idx])
        user.save()


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)

    #db_.connect()
    #User.delete_user("1172192131118784514")
    # print(db_.getDB().list_collection_names())

    # Seeding users
    # seed_users()

    # user = User("keji_irl")
    # user.save()
    # user = User("keji_irl__")
    # print(User.find_user("amine"))
    # user = User.find_user("keji_irl")

    # print("User: {}".format(user))
    # print(user.has_pending_inquiry())

    # Testing Closest users
    # user = User.find_user("trombone")
    # user.save()
    # closest = user.get_closest_users(20)

    #pp.pprint(closest)
    User.find_user(1172192131118784514).set_address("537 Duke Street, Glasgow, Scotland")
    print(User.find_user(1172192131118784514).address)
    print(User.find_user(1172192131118784514).location_info)
