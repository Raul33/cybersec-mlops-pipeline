FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.ui.txt .

RUN pip install --no-cache-dir -r requirements.ui.txt

COPY frontend/ /app/frontend/

EXPOSE 8501

CMD ["streamlit", "run", "/app/frontend/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
