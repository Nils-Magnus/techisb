import json
from jinja2 import Template
import pprint
import datetime
import htmlmin
from icalendar import Calendar, Event
import sys
import itertools
import pytz


#import code; code.interact(local=dict(globals(), **locals()))

def merge_data(html_file, ics_file, meetup_json, curated_json, template_file):

    with open(meetup_json, "r") as eventfile:
        meetup_events = json.loads(eventfile.read())

    with open(curated_json, "r") as eventfile:
        curated_events = json.loads(eventfile.read())

    # with open("../data/sven.json", "r") as eventfile:
    # ---> merging, sorting

    html_data, ics_data = itertools.tee(filter(
            lambda x: datetime.datetime.strptime(x['date'] + ' ' + x['time'], '%Y-%m-%d %H:%M') > datetime.datetime.now(),
            sorted(meetup_events + curated_events, key=lambda x: x['date']),
            ), 2)

    with open(template_file, "r") as template_file:
        events_template = Template(template_file.read().strip())
        f = open(html_file, 'w')
        f.write(htmlmin.minify(
            events_template.render(events = html_data, now = datetime.datetime.now()),
            remove_comments=True, remove_empty_space=True
            )
        )
        f.close()


    calendar = Calendar({
            'PRODID': '-//techisb.de//Berlin tech events/',
            'X-WR-CALNAME': 'Berlin tech events via http://techisb.de',
            'X-WR-TIMEZONE': 'Europe/Berlin',
            'X-WR-CALDESC': 'Áll the relevant Berlin tech events handily in one calendar'
            })

    berlin_timezone = pytz.timezone('Europe/Berlin')

    for this_event in ics_data:

        event = Event()

        event.add('summary', this_event['name'])
        starttime = berlin_timezone.localize(datetime.datetime.strptime(this_event['date'] + ' ' + this_event['time'], '%Y-%m-%d %H:%M'))
        event.add('dtstart', starttime)

        duration = 9000000
        if 'duration' in this_event:
            duration = this_event['duration']
        event.add('dtend', starttime + datetime.timedelta(milliseconds=duration))

        event.add('description', '')

        if 'venue' in this_event:
            event.add('location', this_event['venue']['address'])

        calendar.add_component(event)

    f = open(ics_file, 'wb')
    f.write(calendar.to_ical())
    f.close()


if __name__ == "__main__":
    if (sys.argv[1] == 'docker'):
        parameters = [ "/web/index.html",
                "/web/techisb.ics",
                "/data/meetup.json",
                "/data/curated.json",
                "/templates/index.template"
                ]
    else:
        parameters = [ "../web/index.html",
                "../web/techisb.ics",
                "../data/meetup.json",
                "../data/curated.json",
                "templates/index.template"
                ]
    merge_data(*parameters)
