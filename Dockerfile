FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpoppler-cpp-dev \
    tesseract-ocr \
    poppler-utils \
    libglib2.0-0 \
    libpangocairo-1.0-0 \
    libpangoft2-1.0-0 \
    libcairo2 \
    && pip install --no-cache-dir -r requirements.txt

EXPOSE 8501 8000

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
