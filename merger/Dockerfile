FROM python:3.7

RUN pip install jinja2

COPY merge.py /merge.py
RUN mkdir /templates
COPY templates/index.template /templates

CMD ["python", "/merge.py"]

