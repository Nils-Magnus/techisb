import json
from jinja2 import Template
import pprint
import datetime
import htmlmin

#import code; code.interact(local=dict(globals(), **locals()))

def merge_data():

    with open("/data/meetup.json", "r") as eventfile:
        meetup_events = json.loads(eventfile.read())

    with open("/data/curated.json", "r") as eventfile:
        curated_events = json.loads(eventfile.read())

    # with open("../data/sven.json", "r") as eventfile:
    # ---> merging, sorting

    sorted_events = filter(
            lambda x: datetime.datetime.strptime(x['date'] + ' ' + x['time'], '%Y-%m-%d %H:%M') > datetime.datetime.now(),
            sorted(meetup_events + curated_events, key=lambda x: x['date']),
            )

    with open("/templates/index.template", "r") as template_file:
        events_template = Template(template_file.read().strip())
        print(htmlmin.minify(
            events_template.render(events = sorted_events, now = datetime.datetime.now()),
            remove_comments=True, remove_empty_space=True
            )
            )

if __name__ == "__main__":
    merge_data()
