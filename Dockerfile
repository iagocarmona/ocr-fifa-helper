FROM python:3.10-slim

WORKDIR /app

# 🔥 dependências do sistema (agora com Tesseract)
RUN apt-get update && \
    apt-get install -y \
    tesseract-ocr \
    libgl1 \
    libglib2.0-0 \
    && apt-get clean

COPY . .

# instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# start da aplicação
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-10000}"]