FROM python:3.7

RUN pip install requests

RUN mkdir /templates
COPY apikey.txt /apikey.txt
COPY retrieve-meetup.py /retrieve-meetup.py
COPY run-retrieve.sh /run-retrieve.sh
RUN chmod 755 /run-retrieve.sh

CMD ["/run-retrieve.sh"]

