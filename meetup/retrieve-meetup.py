import requests
from   requests.auth import HTTPDigestAuth
import json

apikey = "00000000000000000000000000000"

api = "https://api.meetup.com/"

req = api + "find/upcoming_events"

with open("apikey.txt", "r") as keyfile:
    apikey = keyfile.read().strip()

# resp = requests.get(req,
#                     data={'key':'value'},
#                     auth=HTTPDigestAuth(raw_input("username: "),
#                                         raw_input("Password: ")),
#                     verify=True)

resp = requests.get(req,
                    params={"sign":       "true",
                            "photo-host": "public",
                            "page":       20,
                            "key":        apikey})


print("We retrieved the URL " + resp.url + " ...\n")

if (resp.ok):

    # Loading the response data into a dict variable
    # json.loads takes in only binary or string variables so using content to fetch binary content
    # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
    all = json.loads(resp.content)
    result = all["events"]
    
    print("The response contains {0} properties:\n".format(len(result)))

    for event in result:
        print("--------------------------------------------------------------\n")
        # print(event["name"] + "\n")
        # print(json.dumps(event, indent=4, sort_keys=True))
       
        line = "{0} {1} {2} {4}\n".format(event["local_date"],
                                              event["local_time"],
                                              event["name"],
                                              event["venue"]["address_1"],
                                              event["link"])
#        line = event["venue"]["address_1"]
        #line = event["link"]
        print(line)
        
#    print(json.dumps(result, indent=4, sort_keys=True))
#    for key in result:
#        print key + ": " + result[key]

else:

    # If response code is not ok (200), print the resulting http error code with description
    print("Oh, no, too bad we received a HTTP {0} status.".format(resp.status_code))
    resp.raise_for_status()
