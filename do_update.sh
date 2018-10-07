#!/bin/sh

# collect events from all source streams
for i in collector-*; do
    echo "Collect from $i ..."
    (cd $i && make build run)
done

# merge them together
echo "Merging events ..."
(cd merger && make build run)

# start nginx if not running
if netstat -lnt | grep -q :80; then
    echo "Server is already running. Skipping."
else
    echo "Starting webserver ..."
    (cd delivery && make run)
fi
echo "Done."
