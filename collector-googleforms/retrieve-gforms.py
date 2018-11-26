import csv
import json

# import code; code.interact(local=dict(globals(), **locals()))

def retrieve_gforms_events():
    events = []

    with open('/techisb.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            event = {}
            event['url'] = row['Event URL']
            event['name'] = row['Event title']
            event['organizer'] = row['Event organizer']
            event['date'] = row['Date and time of event'].split(' ')[0]
            event['time'] = row['Date and time of event'].split(' ')[1]
            event['venue'] = {}
            event['venue']['name'] = row['Venue name']
            event['venue']['address'] = row['Venue address']

            events.append(event)

        print(json.dumps(events, indent=4, sort_keys=True, default=str))

if __name__ == "__main__":
    retrieve_gforms_events()
