import json
from jinja2 import Template
import pprint
import datetime
import htmlmin

#import code; code.interact(local=dict(globals(), **locals()))

def merge_data():

    with open("/data/meetup.json", "r") as eventfile:
        events = json.loads(eventfile.read())

    # with open("../data/sven.json", "r") as eventfile:
    # ---> merging, sorting

    sorted_events = sorted(events, key=lambda x: x['local_date'])

    with open("/templates/index.template", "r") as template_file:
        events_template = Template(template_file.read().strip())
        print(htmlmin.minify(
            events_template.render(events = sorted_events, now = datetime.datetime.now()),
            remove_comments=True, remove_empty_space=True
            )
            )

if __name__ == "__main__":
    merge_data()
