FROM python:3.7

RUN pip install requests

RUN mkdir /templates
COPY retrieve-gforms.py /retrieve-gforms.py
COPY "techisb.csv" /techisb.csv
COPY run-retrieve.sh /run-retrieve.sh
RUN chmod 755 /run-retrieve.sh

CMD ["/run-retrieve.sh"]

