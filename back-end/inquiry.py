from enum import IntEnum


class InquiryType(IntEnum):
    chat = 1
    meet_irl = 2
    request = 3


class Inquiry:
    def __init__(self, user_id):
        self.user_id = user_id  # (User) user class associated with this inquiry
        self.inquiry_type = 0  # (Enum) type of inquiry, see InquiryType
        self.inquiry_str = None  # (str) the open-response text the user sent to chat bot describing their inquiry
        self.time_limit = None  # (int) time limit in seconds that the inquiry will exist for
        self.matched_user = None  # (User) user class of other user that matches with this inquiry

    def set_inquiry_type(self, inquiry_type):
        self.inquiry_type = inquiry_type
        return self.inquiry_type

    def set_inquiry_str(self, inquiry_str):
        self.inquiry_str = inquiry_str
        return self.inquiry_str

    def match_inquiry(self, user):
        self.matched_user = user
