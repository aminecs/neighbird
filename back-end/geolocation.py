import requests
import os
from dotenv import load_dotenv
from geopy import distance
load_dotenv()

GOOGLE_API_KEY = os.environ.get('GOOGLE_GEOLOCATION_KEY', "")

def distanceBetweenLocations(locA, locB, inMiles):
    """Returns the distance between two locations

    Parameters
    ----------
    locA: tuple
        Has two attributes: (lat, lng)
    locB: tuple
        Has two attributes: (lat, lng)

    metric: str
        Used either 'mi' or 'km' to get your result in that format.
    Returns
    -------
    double
        the distance between the two locations
    """
    if inMiles:
        return distance.distance(locA, locB).miles
    return distance.distance(locA, locB).km


def getLocationInfo(location_str):
    """Returns Location information of a given address

    @input location_str - A string
    @output Object with data & error keys
    """
    ret = {"data": None, "error": None}

    try:
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        query_params = {
            "key": GOOGLE_API_KEY,
            "address": location_str,
        }

        res = requests.post(url, params=query_params)
        res.raise_for_status()
        locations = res.json()["results"]
        if not locations:
            ret["error"] = "Location not found"
        else:
            ret["data"]= {
                "formatted_address": locations[0]["formatted_address"],
                "lat": locations[0]["geometry"]["location"]["lat"],
                "lng": locations[0]["geometry"]["location"]["lng"],
        }
    except ValueError:
        ret["error"] = "Improper JSON response from URL"
    except requests.exceptions.HTTPError as err:
        print("Exception: {}".format(err))
        ret["error"] = "Error making request: {}".format(res.status_code)
    except Exception as e:
        print("Error: {}".format(e))
        ret["error"] = "An Error occured"

    return ret


if __name__=="__main__":
    """
    To test module functionality
    """
    # print(getLocationInfo("gbagada phase 2lagos"))
    addr1 = getLocationInfo("panorama hotel, Victoria Island")
    addr2 = getLocationInfo("gbagada phase 2, Lagos")

    # Test Distance between 2 points
    print(addr1)
    print(addr2)
    loca = (addr1["data"]["lat"], addr1["data"]["lng"])
    locb = (addr2["data"]["lat"], addr2["data"]["lng"])

    inMiles = False
    print(distanceBetweenLocations(loca, locb, inMiles), "km")

