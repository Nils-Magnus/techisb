FROM python:3.7

RUN pip install requests jinja2

RUN mkdir /templates
COPY apikey.txt /apikey.txt
COPY retrieve-meetup.py /retrieve-meetup.py
COPY templates/index.template /templates

CMD ["python", "/retrieve-meetup.py"]

