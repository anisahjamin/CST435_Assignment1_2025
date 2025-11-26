FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir grpcio grpcio-tools langdetect textblob googletrans==4.0.0-rc1

COPY . .

RUN mkdir -p /app/output
RUN chmod +x client.py

EXPOSE 50050 50051 50052 50053 50054 50055

CMD ["python", "controller_server.py"]
