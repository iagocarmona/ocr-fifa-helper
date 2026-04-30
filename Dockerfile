FROM python:3.10

# instala tesseract
RUN apt-get update && \
    apt-get install -y tesseract-ocr && \
    apt-get clean

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]