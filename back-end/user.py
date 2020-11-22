from location import GeoLocator
import inquiry
from geolocation import getLocationInfo

class User:
    def __init__(self, user_id):
        self.user_id = user_id  # (str) user id of Twitter user
        self.inquiries = []  # (list) list of inquiry objects
        self.location_info = None  # (dict) typical location information (lon/lat, city, region, country, etc)
        self.address = None  # (str) string of original address user gives to bot
        self.available_to_help = False  # (bool) indicates whether this user is available to help with a request from another user
        self.last_msg = None

    def set_address(self, address):
        self.address = address
        self.location_info = getLocationInfo(address)
        return self.location_info


if __name__ == '__main__':
    user = User('test')
    print(user.set_address('60 Ridge Road, Nashua, NH'))  # US address
    print(user.set_address('100 Harbour St, Toronto, Ontario'))  # Canada address
    print(user.set_address('15 Residence Road, Gbagada Phase 2, Lagos, Nigeria'))  # Nigeria address
    print(user.set_address('Palm Dr, Lekki Penninsula 2, Lagos, Nigeria'))  # Nigeria address
    print(user.set_address('12 Woodlands Drive, Woodlands, Glasgow G4 9EH'))  # Glasgow address
    print(user.set_address('10 Park Rd, Glasgow G4 9JG'))  # Glasgow address

    # Nominatim API can get location data for larger regions of Nigeria but not street addresses
    print(user.set_address('Lagos, Nigeria'))

    inquiry = inquiry.Inquiry(user=user, inquiry_type=inquiry.InquiryType.chat,
                              inquiry_str='i want to talk about apples')
    user.inquiries.append(inquiry)
    print(user.inquiries)
    users_inquiry = user.inquiries[0]
    print(users_inquiry.user.location_info)
    print(users_inquiry.inquiry_type)
    print(users_inquiry.inquiry_str)
    print(users_inquiry.time_limit)
