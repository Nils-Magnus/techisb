import json
from jinja2 import Template
import pprint
import datetime
import htmlmin
import icalendar
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


    calendar = icalendar.Calendar({
            'PRODID': '-//techisb.de//Berlin tech events/',
            'METHOD': 'PUBLISH',
            'X-WR-CALNAME': 'Berlin tech events via http://techisb.de',
            'X-WR-TIMEZONE': 'Europe/Berlin',
            'X-WR-CALDESC': 'All the relevant Berlin tech events handily in one calendar'
            })


    # Provide timezone info - see https://github.com/collective/icalendar/blob/master/src/icalendar/tests/test_timezoned.py#L50
    tzc = icalendar.Timezone()
    tzc.add('tzid', 'Europe/Berlin')
    tzc.add('x-lic-location', 'Europe/Berlin')

    tzs = icalendar.TimezoneStandard()
    tzs.add('tzname', 'CET')
    tzs.add('dtstart', datetime.datetime(1970, 10, 25, 3, 0, 0))
    tzs.add('rrule', {'freq': 'yearly', 'bymonth': 10, 'byday': '-1su'})
    tzs.add('TZOFFSETFROM', datetime.timedelta(hours=2))
    tzs.add('TZOFFSETTO', datetime.timedelta(hours=1))

    tzd = icalendar.TimezoneDaylight()
    tzd.add('tzname', 'CEST')
    tzd.add('dtstart', datetime.datetime(1970, 3, 29, 2, 0, 0))
    tzs.add('rrule', {'freq': 'yearly', 'bymonth': 3, 'byday': '-1su'})
    tzd.add('TZOFFSETFROM', datetime.timedelta(hours=1))
    tzd.add('TZOFFSETTO', datetime.timedelta(hours=2))

    tzc.add_component(tzs)
    tzc.add_component(tzd)
    calendar.add_component(tzc)

    berlin_timezone = pytz.timezone('Europe/Berlin')

    for this_event in ics_data:

        event = icalendar.Event()

        event.add('summary', this_event['name'])
        starttime = berlin_timezone.localize(datetime.datetime.strptime(this_event['date'] + ' ' + this_event['time'], '%Y-%m-%d %H:%M'))
        # brutal hack to show correct timezone in Google calendar
        starttime = starttime - datetime.timedelta(hours=2)
        event.add('dtstart', starttime)

        duration = 3600000
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
