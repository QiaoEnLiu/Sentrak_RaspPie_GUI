# Dockerfile for Flask API
FROM python:3.9-slim

WORKDIR /SentrakDocker

COPY flask_api.py .

# RUN chmod -R 777 /Sentrak_RaspPie_GUI/SentrakSQL/

RUN pip install flask

CMD ["python3", "flask_api.py"]

EXPOSE 5000
