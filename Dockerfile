# 使用輕量級 Python
FROM python:3.10-slim

# 設定工作目錄
WORKDIR /app

# 安裝套件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製全部檔案
COPY . .

# 告訴 Docker container 要開哪個 port
EXPOSE 8080

# 設定環境變數（正確格式）
ENV PORT=8080

# 直接啟動你的主程式，而不是用 flask run
CMD ["python", "line_bot.py"]
