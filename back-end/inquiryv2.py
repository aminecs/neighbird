from enum import IntEnum
import db as db_
import geolocation as geo
import pprint
from geolocation import distanceBetweenLocations
from nlp import NLPAnalyzer


class InquiryType(IntEnum):
    chat = 1
    meet_irl = 2
    request = 3


class Inquiry:
    def __init__(self, user_id):
        # one user per enquiry
        self.user_id = user_id  # (User) user class associated with this inquiry
        self.inquiry_type = 0  # (Enum) type of inquiry, see InquiryType
        self.inquiry_str = None  # (str) the open-response text the user sent to chat bot describing their inquiry
        self.time_limit = None  # (int) time limit in seconds that the inquiry will exist for
        self.matched_user = None  # (User) user class of other user that matches with this inquiry
        self.entities = []

    def save(self):
        """
        Saves to the db
        """
        Inquiry_coll = db_.getDB().inquiry
        inq = Inquiry_coll.find_one({"user_id": self.user_id})

        new_inquiry = {
            "user_id": self.user_id,
            "inquiry_type": self.inquiry_type,
            "inquiry_str": self.inquiry_str,
            "time_limit": self.time_limit,
            "matched_user": self.matched_user,
            "entities": self.entities,
        }

        if not inq:
            print("new Inq: {}".format(self))
            inserted_inq = Inquiry_coll.insert_one(new_inquiry)
            print("Inserted user: {}. Has mongoID: {}".format(new_inquiry, inserted_inq.inserted_id))
        else:
            Inquiry_coll.replace_one({"_id": inq["_id"]}, new_inquiry)

    @staticmethod
    def get_all_inquiries():
        """
        Get all enquiries in the db
        """
        Inquiry_coll = db_.getDB().inquiry
        all_inqs = Inquiry_coll.find()
        inquries = []

        for inq in all_inqs:
            inquries.append(Inquiry.dbinq2object(inq))
        return inquries

    @staticmethod
    def get_inquiry(twitter_id):
        """
        Get enquiry by user id
        """
        Inquiry_coll = db_.getDB().inquiry
        inq = Inquiry_coll.find_one({"user_id": twitter_id})
        return Inquiry.dbinq2object(inq)

    @staticmethod
    def dbinq2object(inq):
        inq_obj = None
        if inq:
            "Adding to the user"
            print(inq)
            inq_obj = Inquiry(inq["user_id"])
            inq_obj.inquiry_type = inq["inquiry_type"]
            inq_obj.inquiry_str = inq["inquiry_str"]
            inq_obj.time_limit = inq["time_limit"]
            inq_obj.matched_user = inq["matched_user"]

            inq_obj.entities = inq['entities']
        return inq_obj

    @staticmethod
    def delete_inquiry(twitter_id):
        Inq_coll = db_.getDB().inquiry
        no_deleted = Inq_coll.delete_one({"user_id": twitter_id})
        return no_deleted

    def set_inquiry_type(self, inquiry_type):
        self.inquiry_type = inquiry_type
        self.save()
        return self.inquiry_type

    def set_inquiry_str(self, inquiry_str):
        self.inquiry_str = inquiry_str

        analyzer = NLPAnalyzer.get_instance()
        self.entities = analyzer.get_entity_analysis(inquiry_str)

        self.save()
        return self.inquiry_str

    def match_inquiry(self, user):
        self.matched_user = user

    def __repr__(self):
        return "{}, {}, {}, {}, {}".format(self.user_id, self.inquiry_type, self.inquiry_str, self.time_limit,
                                           self.matched_user)


if __name__ == "__main__":
    # print("Testing entities")
    # i1 = Inquiry("123453")
    # i2 = Inquiry("tromgold")
    # i3 = Inquiry("sadkfjds")
    # print(i1)
    # i1.set_inquiry_type(1)
    # i2.set_inquiry_type(1)
    # i1.set_inquiry_type(0)
    # i1.set_inquiry_str("Play football")
    # i2.set_inquiry_str("Play tennis")
    # i3.set_inquiry_str("Feelings")
    # print(i1)
    # i1.save()
    # i2.save()
    # i2.save()
    # all_inq = Inquiry.get_all_inquiries()
    # print(all_inq[0])

    # test get inq
    print(Inquiry.get_inquiry("4"))
