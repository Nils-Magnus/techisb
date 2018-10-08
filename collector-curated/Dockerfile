FROM python:3.7

RUN pip install gitpython pyyaml

RUN mkdir /templates
COPY retrieve-curated.py /retrieve-curated.py
COPY run-retrieve.sh /run-retrieve.sh
RUN chmod 755 /run-retrieve.sh

CMD ["/run-retrieve.sh"]
