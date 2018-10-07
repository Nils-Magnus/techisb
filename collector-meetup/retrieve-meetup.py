import requests
import json

# import code; code.interact(local=dict(globals(), **locals()))

def retrieve_meetup_events():
    api = "https://api.meetup.com/"

    req = api + "find/upcoming_events"

    with open("apikey.txt", "r") as keyfile:
        apikey = keyfile.read().strip()

    resp = requests.get(req, params={"key": apikey})

    if (resp.ok):

        events = json.loads(resp.content)["events"]

        # we should apply some filtering here

        print(json.dumps(events, indent=4, sort_keys=True))

    else:

        print("Oh, no, too bad we received a HTTP {0} status.".format(resp.status_code))
        resp.raise_for_status()

if __name__ == "__main__":
    retrieve_meetup_events()
