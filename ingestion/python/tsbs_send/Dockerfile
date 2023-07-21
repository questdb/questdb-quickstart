# syntax=docker/dockerfile:1
FROM python:3.7-alpine
RUN apk add --no-cache gcc musl-dev linux-headers curl
COPY ilp_ingestion.py .
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD while [[ "$(curl -s -o /dev/null -w ''%{http_code}'' host.docker.internal:19003)" != "200" ]]; do sleep 1; done;python ./ilp_ingestion.py
