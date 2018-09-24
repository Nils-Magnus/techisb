import requests
from   requests.auth import HTTPDigestAuth
import json


api = "http://jsonplaceholder.typicode.com/"

req = api + "posts"

# resp = requests.get(req,
#                     auth=HTTPDigestAuth(raw_input("username: "),
#                                         raw_input("Password: ")),
#                     verify=True)

resp = requests.get(req)

if (resp.ok):

    # Loading the response data into a dict variable
    # json.loads takes in only binary or string variables so using content to fetch binary content
    # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
    result = json.loads(resp.content)

    print("The response contains {0} properties:\n".format(len(result)))

    print(json.dumps(result, indent=4, sort_keys=True))
#    for key in result:
#        print key + ": " + result[key]

else:

    # If response code is not ok (200), print the resulting http error code with description
    print("Oh, no, too bad we received a HTTP {0} status.".format(resp.status_code))
    resp.raise_for_status()
