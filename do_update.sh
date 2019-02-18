for COLLECTOR in meetup curated eventbrite inberlin; do
  (cd collector-${COLLECTOR} && python3 retrieve-${COLLECTOR}.py "berlin" > ../data/${COLLECTOR}.json)
done

(cd merger && python3 merge.py "inberlin")
