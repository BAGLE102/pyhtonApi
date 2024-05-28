# 使用官方 Python 鏡像作為基礎鏡像
FROM python:3.9-slim

# 設定工作目錄
WORKDIR /app

# 安裝必要的系統包和 ODBC 驅動程式
RUN apt-get update && \
     apt-get install -y gcc g++ unixodbc unixodbc-dev curl apt-transport-https && \
     curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
     curl https://packages.microsoft.com/config/debian/$(lsb_release -rs)/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
     apt-get update && \
     ACCEPT_EULA=Y apt-get install -y msodbcsql17 && \
     apt-get clean && \
     rm -rf /var/lib/apt/lists/*

# 將目前目錄中的所有檔案複製到工作目錄中
COPY . .

# 查看 requirements.txt 檔案內容
RUN cat requirements.txt

# 安裝 Python 依賴項
RUN pip install --no-cache-dir -r requirements.txt

# 暴露應用程式運行的端口，例如 5000
EXPOSE 5000

# 設定環境變量，如果需要
ENV PYTHONUNBUFFERED=1

# 使用 gunicorn 啟動應用程式
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
