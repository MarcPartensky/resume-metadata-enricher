FROM python:3.11-alpine

WORKDIR /root

# Requirements dont change ofter
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Code does
COPY resume-metadata-enricher/__main__.py ./

ENTRYPOINT ["python", "."]
