import json
from jinja2 import Template, Environment, FileSystemLoader
import datetime
import htmlmin
import icalendar
import sys
import itertools
import pytz
import glob
import copy
import os


def merge_data(web_dir, json_dir, calendar_filename, is_berlin):
    def _to_datetime(date, time):
        return datetime.datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M')

    def _calendar_header():
        # generate ical file
        if is_berlin:
            calendar = icalendar.Calendar({
                    'PRODID': '-//TechisB//Berlin tech events//DE',
                    'METHOD': 'PUBLISH',
                    'VERSION': '2.0',
                    'X-WR-CALNAME': 'TechisB - Berlin tech events via https://techisb.de',
                    'X-WR-TIMEZONE': 'Europe/Berlin',
                    'X-WR-CALDESC': 'All the relevant Berlin tech events in one calendar'
                    })
        else:
            calendar = icalendar.Calendar({
                    'PRODID': '-//TechisM//Munich tech events//DE',
                    'METHOD': 'PUBLISH',
                    'VERSION': '2.0',
                    'X-WR-CALNAME': 'TechisM - Munich tech events via https://techisb.de',
                    'X-WR-TIMEZONE': 'Europe/Berlin',
                    'X-WR-CALDESC': 'All the relevant Munich tech events in one calendar'
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

        return calendar

    now = datetime.datetime.now()

    jinja_environment = Environment(loader=FileSystemLoader('.'))

    # read all events
    events = []
    for filename in glob.glob(json_dir + '/*.json'):
        with open(filename, encoding='utf-8') as file:
            events = events + json.loads(file.read())

    # sort them and provide two iterators for html and ical generation
    future_events = filter(lambda x: 'date' in x and _to_datetime(x['date'], x['time']) > now, events)
    sorted_events = sorted(future_events, key=lambda x: x['date'] + x['time'])

    today_string = now.date().strftime("%Y-%m-%d")
    tomorrow_string = (now.date() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    html_data, mobile_data, ics_data = itertools.tee(
            [dict(item,
                eventnumber=sorted_events.index(item),
                week_day=(_to_datetime(item['date'], item['time']).strftime("%A")),
                is_today=(item['date'] == today_string),
                is_tomorrow=(item['date'] == tomorrow_string)
                )
                for item in sorted_events], 3)

    # generate html file
    with open('templates/index.template', 'r') as template_file, open(web_dir + 'index.html', 'w') as output_file:
        events_template = Template(template_file.read().strip())
        output_file.write(htmlmin.minify(
            events_template.render(events=html_data, now=now, is_berlin=is_berlin),
            remove_comments=True, remove_empty_space=True
            )
        )

    # generate mobile html file
    with open(web_dir + 'mobile.html', 'w') as output_file:
        events_template = jinja_environment.get_template('templates/mobile.template')
        output_file.write(htmlmin.minify(
            events_template.render(events=mobile_data, now=now, is_berlin=is_berlin),
            remove_comments=True, remove_empty_space=True
            )
        )

    berlin_timezone = pytz.timezone('Europe/Berlin')

    dtstamp = berlin_timezone.localize(now)

    calendar = _calendar_header()

    for this_event in ics_data:

        event = icalendar.Event()

        event.add('summary', this_event['name'])
        starttime = berlin_timezone.localize(_to_datetime(this_event['date'], this_event['time']))
        event.add('dtstart', starttime)

        duration = 3600000  # one hour
        if 'duration' in this_event:
            duration = this_event['duration']
        event.add('dtend', starttime + datetime.timedelta(milliseconds=duration))
        event.add('dtstamp', dtstamp)

        event.add('organizer', this_event['organizer'])

        event.add('uid', (str(starttime.timestamp()) + this_event['url'] + 'techisb.de'))

        event.add('description', this_event['url'])

        if 'venue' in this_event:
            event.add('location', this_event['venue']['address'])

        calendar.add_component(event)

        this_events_calendar = _calendar_header()
        this_events_calendar.add_component(event)
        with open(web_dir + 'ics/' + str(this_event['eventnumber']) + '.ics', 'wb') as output_file:
            output_file.write(this_events_calendar.to_ical())

    with open(web_dir + calendar_filename, 'wb') as output_file:
        output_file.write(calendar.to_ical())


if __name__ == "__main__":
    if (sys.argv[1] == 'inberlin'):
        parameters = [os.path.expanduser('~') + '/websites/dirkgomez.de/techisb.de/',
                      '../data/',
                      'techisb.ics',
                      True]
    elif (sys.argv[1] == 'inberlinmunich'):
        parameters = [os.path.expanduser('~') + '/websites/dirkgomez.de/techism.de/',
                      '../data/',
                      'techism.ics',
                      False]
    merge_data(*parameters)
