import requests
import os
from dotenv import load_dotenv
load_dotenv()

GOOGLE_API_KEY = os.environ.get('GOOGLE_GEOLOCATION_KEY', "")

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
    print(getLocationInfo("gbagada phase 2lagos"))
