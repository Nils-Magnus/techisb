FROM python:3.7

RUN pip install requests

RUN mkdir /templates
COPY apikey.txt /apikey.txt
COPY retrieve-meetup.py /retrieve-meetup.py

CMD ["python", "/retrieve-meetup.py"]

