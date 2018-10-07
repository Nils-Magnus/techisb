import json
from jinja2 import Template
import pprint
import datetime

#import code; code.interact(local=dict(globals(), **locals()))

def merge_data():

    with open("/data/meetup.json", "r") as eventfile:
        events = json.loads(eventfile.read())

    # with open("../data/sven.json", "r") as eventfile:
    # ---> merging, sorting
    
    with open("/templates/index.template", "r") as template_file:
        events_template = Template(template_file.read().strip())
        line = events_template.render(events = events, now = datetime.datetime.now())
        print(line)

if __name__ == "__main__":
    merge_data()
