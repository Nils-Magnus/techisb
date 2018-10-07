#!/bin/sh

# collect events from all source streams
for i in collector-*; do
    echo "Collect from $i ..."
    (cd $i && make run)
done

# merge them together
echo "Merging events ..."
(cd merger && make run)

# start nginx if not running
if netstat -lnt | grep -q :8088; then
    echo "Server is already running. Skipping."
else
    echo "Starting webserver ..."
    (cd delivery && make run)
fi
echo "Done."
