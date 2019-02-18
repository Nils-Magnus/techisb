import json
from git import Repo
import os
import yaml
import shutil
import sys
# import code; code.interact(local=dict(globals(), **locals()))


def retrieve_curated(remote, local):
    remote = "https://github.com/techisb/curated"
    local = '/tmp/curated/'
    shutil.rmtree(local, ignore_errors=True)
    Repo.clone_from(remote, local)

    all_events = []

    with os.scandir(local) as listOfEntries:
        for entry in listOfEntries:
            if entry.name.endswith('.yaml') and entry.is_file():
                with open(entry, "r") as f:
                    for events in yaml.load_all(f.read()):
                        for event in events:
                            all_events.append(event)

    shutil.rmtree(local, ignore_errors=True)
    print(json.dumps(all_events, indent=4, sort_keys=True, default=str))


if __name__ == "__main__":
    if sys.argv[1] == 'berlin':
        retrieve_curated('https://github.com/techisb/curated', '/tmp/curated/')
    elif sys.argv[1] == 'munich':
        retrieve_curated('https://github.com/techisb/curated-munich', '/tmp/curated-munich/')
