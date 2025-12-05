FROM python:3.11-slim
WORKDIR /app
COPY mqttexporter.py .
RUN pip install prometheus_client paho-mqtt
EXPOSE 9641
CMD ["python3", "mqttexporter.py"]
