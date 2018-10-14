import json
from jinja2 import Template
import datetime
import htmlmin
import icalendar
import sys
import itertools
import pytz
import glob


def merge_data(html_file, ics_file, json_dir):
    def _to_datetime(date, time):
        return datetime.datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M')

    now = datetime.datetime.now()

    # read all events
    events = []
    for filename in glob.glob(json_dir + '/*.json'):
        with open(filename) as file:
            events = events + json.loads(file.read())

    # sort them and provide two iterators for html and ical generation
    html_data, ics_data = itertools.tee(filter(
            lambda x: _to_datetime(x['date'], x['time']) > now,
            sorted(events, key=lambda x: x['date']),
            ), 2)

    # generate html file
    with open('templates/index.template', 'r') as template_file, open(html_file, 'w') as output_file:
        events_template = Template(template_file.read().strip())
        output_file.write(htmlmin.minify(
            events_template.render(events=html_data, now=now),
            remove_comments=True, remove_empty_space=True
            )
        )

    # generate ical file
    calendar = icalendar.Calendar({
            'PRODID': '-//TechisBe//Berlin tech events//DE',
            'METHOD': 'PUBLISH',
            'VERSION': '2.0',
            'X-WR-CALNAME': 'TechisB - Berlin tech events via http://techisb.de',
            'X-WR-TIMEZONE': 'Europe/Berlin',
            'X-WR-CALDESC': 'All the relevant Berlin tech events in one calendar'
            })

    # Provide timezone info -
    # see https://github.com/collective/icalendar/blob/master/src/icalendar/tests/test_timezoned.py#L50
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

    dtstamp = berlin_timezone.localize(now)

    for this_event in ics_data:

        event = icalendar.Event()

        event.add('summary', this_event['name'])
        starttime = berlin_timezone.localize(_to_datetime(this_event['date'], this_event['time']))
        event.add('dtstart', starttime)

        duration = 3600000
        if 'duration' in this_event:
            duration = this_event['duration']
        event.add('dtend', starttime + datetime.timedelta(milliseconds=duration))
        event.add('dtstamp', dtstamp)

        event.add('uid', (str(starttime.timestamp()) + this_event['url'] + 'techisb.de'))

        event.add('description', this_event['url'])

        if 'venue' in this_event:
            event.add('location', this_event['venue']['address'])

        calendar.add_component(event)

    with open(ics_file, 'wb') as output_file:
        output_file.write(calendar.to_ical())


if __name__ == "__main__":
    if (sys.argv[1] == 'docker'):
        parameters = ['/web/index.html',
                      '/web/techisb.ics',
                      '/data/']
    else:
        parameters = ['../web/index.html',
                      '../web/techisb.ics',
                      '../data/']
    merge_data(*parameters)
