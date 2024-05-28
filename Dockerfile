# 使用官方 Python 镜像作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 安装必要的系统包和 ODBC 驱动程序
RUN apt-get update && \
    apt-get install -y gcc g++ unixodbc unixodbc-dev curl apt-transport-https && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/$(lsb_release -rs)/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 将当前目录中的所有文件复制到工作目录中
COPY . .

# 查看 requirements.txt 文件内容
RUN cat requirements.txt

# 安装 Python 依赖项
RUN pip install --no-cache-dir -r requirements.txt

# 暴露应用运行的端口，例如 5000
EXPOSE 5000

# 设置环境变量，如果需要
ENV PYTHONUNBUFFERED=1

# 使用 gunicorn 启动应用程序
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
