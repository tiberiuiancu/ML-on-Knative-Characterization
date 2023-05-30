FROM python:3.9-slim

RUN pip install pandas requests boto3 numpy

WORKDIR /app

COPY dates.csv .
COPY request.py .
COPY images/* images/

ENTRYPOINT ["python", "request.py"]
