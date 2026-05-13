FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "python -c 'from consumer import consume_messages; import threading; threading.Thread(target=consume_messages, daemon=True).start()' & uvicorn main:app --host 0.0.0.0 --port 8000"]
