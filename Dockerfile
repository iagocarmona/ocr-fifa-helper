FROM python:3.10-slim

WORKDIR /app

# 🔥 dependências do sistema (necessárias pro opencv / torch)
RUN apt-get update && \
    apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && apt-get clean

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-10000}"]