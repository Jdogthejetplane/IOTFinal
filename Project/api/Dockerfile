FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY led-api.py .
CMD ["python", "led-api.py"]
