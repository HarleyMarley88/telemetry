FROM python:3.12-slim

WORKDIR /app

COPY simulation.py .

RUN pip install kafka-python

CMD ["python", "simulation.py"]