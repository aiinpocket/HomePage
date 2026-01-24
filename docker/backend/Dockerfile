FROM python:3.11-slim

WORKDIR /app

# 安裝依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式
COPY app/ ./app/

# 設定環境變數
ENV PYTHONUNBUFFERED=1

# 啟動
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
