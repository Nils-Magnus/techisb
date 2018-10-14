FROM python:3.7

RUN pip install jinja2 htmlmin icalendar

COPY merge.py /merge.py
RUN mkdir /templates
COPY templates/index.template /templates

CMD ["python", "/merge.py", "/web/index.html", "/web/techisb.ics"]
