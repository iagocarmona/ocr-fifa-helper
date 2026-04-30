FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y tesseract-ocr && \
    apt-get clean

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "10000"]