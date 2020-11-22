from enum import IntEnum
from nlp import NLPAnalyzer


class InquiryType(IntEnum):
    chat = 1
    meet_irl = 2
    request = 3


class Inquiry:
    def __init__(self, user, inquiry_type, inquiry_str, time_limit=None):
        self.user = user  # (User) user class associated with this inquiry
        if user:
            self.location = user.location_info  # (dict) same as user.location_info
        else:
            self.location = None
        self.inquiry_type = InquiryType(inquiry_type)  # (Enum) type of inquiry, see InquiryType
        self.inquiry_str = inquiry_str  # (str) the open-response text the user sent to chat bot describing their inquiry
        self.time_limit = time_limit  # (int) time limit in seconds that the inquiry will exist for
        self.matched_user = None  # (User) user class of other user that matches with this inquiry

        nlp = NLPAnalyzer.get_instance()
        self.entities = nlp.get_entity_analysis(inquiry_str)  # (dict) list of named entities from inquiry_str for NLP analysis

    def match_inquiry(self, user):
        self.matched_user = user
