import requests
from   requests.auth import HTTPDigestAuth
import json
from jinja2 import Template
import pprint
import datetime


#import code; code.interact(local=dict(globals(), **locals()))

def retrieve_meetup_events():
    api = "https://api.meetup.com/"

    req = api + "find/upcoming_events"

    with open("apikey.txt", "r") as keyfile:
        apikey = keyfile.read().strip()

# resp = requests.get(req,
#                     data={'key':'value'},
#                     auth=HTTPDigestAuth(raw_input("username: "),
#                                         raw_input("Password: ")),
#                     verify=True)

    #import code; code.interact(local=dict(globals(), **locals()))
    resp = requests.get(req,
                        params={ "key":        apikey})


    #print("We retrieved the URL " + resp.url + " ...\n")

    if (resp.ok):

        # Loading the response data into a dict variable
        # json.loads takes in only binary or string variables so using content to fetch binary content
        # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
        # events = json.loads(str(resp.content))['events']
        events = json.loads(resp.content)['events']

        with open("templates/index.template", "r") as template_file:
            events_template = Template(template_file.read().strip())
            line = events_template.render(events = events, now = datetime.datetime.now())
            print(line)

#    print(json.dumps(result, indent=4, sort_keys=True))
#    for key in result:
#        print key + ": " + result[key]

    else:

        # If response code is not ok (200), print the resulting http error code with description
        print("Oh, no, too bad we received a HTTP {0} status.".format(resp.status_code))
        resp.raise_for_status()


if __name__ == "__main__":
    retrieve_meetup_events()
