import requests
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
import json


class InberlinHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.current = None
        self.values = {}

    def handle_data(self, data):
        if data == 'Start':
            self.current = 'Start'
        elif self.current == 'Start':
            self.values['start'] = data
            self.current = None
        elif data == 'End':
            self.current = 'End'
        elif self.current == 'End':
            self.values['end'] = data
            self.current = None
        elif data == 'Description':
            self.current = 'Description'
        elif self.current == 'Description':
            self.values['description'] = data
            self.current = None

# import code; code.interact(local=dict(globals(), **locals()))

def retrieve_inberlin_events():
    def dedup_dict_list(list_of_dicts: list, columns: list) -> list:
        return list({''.join(row[column] for column in columns): row
                for row in list_of_dicts}.values())

    api = "https://user.in-berlin.de/vrkalender/export/atom-subscribe.php?uid=&sid=5095c2027826b&rid=&icskey=in-berlin"

    response = requests.get(api)

    if (response.ok):

        events = []

        root = ET.fromstring(response.content)
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            event = {}
            event['url'] = 'https://user.in-berlin.de/vrkalender/view-schedule.php'
            event['organizer'] = 'IN-Berlin'
            event['venue'] = {}
            event['venue']['name'] = 'IN-Berlin'
            event['venue']['address'] = 'Lehrter Str. 35, 10557 Berlin'
            event['venue']['lat'] = '52.534254'
            event['venue']['lon'] = '13.359344'

            for entry_data in entry:
                if entry_data.tag == '{http://www.w3.org/2005/Atom}summary':
                    parser = InberlinHTMLParser()
                    parser.feed(entry_data.text)
                    start = parser.values['start'].split(' ')
                    date = start[1].split('.')
                    event['date'] = date[2] + '-' + date[1] + '-' + date[0]
                    event['time'] = start[2]
                elif entry_data.tag == '{http://www.w3.org/2005/Atom}title':
                    event['name'] = entry_data.text
                elif entry_data.tag == '{http://www.w3.org/2005/Atom}id':
                    event['id'] = entry_data.text

            if event['name'] not in ['IN-Berlin-Aktiventreffen']:
                events.append(event)

        print(json.dumps(dedup_dict_list(events, ['id']), indent=4, sort_keys=True))
    else:

        print("Oh, no, too bad we received a HTTP {0} status.".format(resp.status_code))
        resp.raise_for_status()

if __name__ == "__main__":
    retrieve_inberlin_events()
