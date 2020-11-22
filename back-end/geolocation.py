import requests
import os
import urllib.parse
from geopy import distance

MAPBOX_TOKEN = os.environ.get('MAPBOX_TOKEN')

def distanceBetweenLocations(locA, locB, inMiles):
    """Returns the distance between two locations
    Parameters
    ----------
    locA: tuple
        Has two attributes: (lat, lng)
    locB: tuple
        Has two attributes: (lat, lng)
    inMiles: str
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
        url_parsed_addr = urllib.parse.quote_plus(location_str)
        url = "https://api.mapbox.com/geocoding/v5/mapbox.places/{}.json".format(url_parsed_addr)
        query_params = {
            "access_token": MAPBOX_TOKEN,
        }


        res = requests.get(url, params=query_params)
        res.raise_for_status()

        locations = res.json()["features"]

        if not locations:
            ret["error"] = "Location not found"
        else:
            #API RETURNS [LNG, LAT]
            #print("Here: \n", locations[0]["context"])
            ret["data"] = {
                "formatted_address": locations[0]["place_name"],
                "city": locations[0]["context"][1]["text"],
                "country": locations[0]["context"][-1]["text"],
                "lng": locations[0]["geometry"]["coordinates"][0],
                "lat": locations[0]["geometry"]["coordinates"][1],
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
    addr = "panorama hotel, Victoria Island, Lagos"

    # print(getLocationInfo("7 Jayhawk way, Holmdel"))
    addr1 = getLocationInfo("panorama hotel, Victoria Island, Lagos")
    addr2 = getLocationInfo("gbagada phase 2, Lagos")

    # Test Distance between 2 points
    print(addr1)
    print(addr2)
    loca = (addr1["data"]["lat"], addr1["data"]["lng"])
    locb = (addr2["data"]["lat"], addr2["data"]["lng"])

    inMiles = False
    print(distanceBetweenLocations(loca, locb, inMiles), "km")