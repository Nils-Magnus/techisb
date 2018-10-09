import requests
import json

def retrieve_eventbrite_events():
    api = "https://www.eventbriteapi.com/v3/"

    req = api + "events/search"

    with open("apikey.txt", "r") as keyfile:
        apikey = keyfile.read().strip()

    resp = requests.get(req, params={"token":            apikey,
                                     "q":                "linux",
                                     "location.address": "Berlin",
                                     "location.within":  "20km",
                                     "price":            "free"})
    
    if (resp.ok):

        events = json.loads(resp.content)["events"]

        print(json.dumps(events, indent=4, sort_keys=True))

    else:

        print("Oh, no, too bad we received a HTTP {0} status.".format(resp.status_code))
        resp.raise_for_status()

if __name__ == "__main__":
    retrieve_eventbrite_events()
