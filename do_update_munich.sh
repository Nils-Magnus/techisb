for COLLECTOR in meetup ; do
  (cd collector-${COLLECTOR} && python3 retrieve-${COLLECTOR}.py "munich" > ../data/${COLLECTOR}.json)
done

(cd merger && python3 merge.py "inberlinmunich")
