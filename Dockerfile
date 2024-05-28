# 使用官方 Python 镜像作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 安装必要的系统包和 ODBC 驱动程序
RUN apt-get update && \
    apt-get install -y unixodbc unixodbc-dev libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

# 如果你使用特定的数据库驱动程序，例如 PostgreSQL ODBC 驱动
RUN apt-get update && \
    apt-get install -y odbc-postgresql && \
    rm -rf /var/lib/apt/lists/*

# 将当前目录中的所有文件复制到工作目录中
COPY . .

# 安装 Python 依赖项
RUN pip install --no-cache-dir -r requirements.txt

# 暴露应用运行的端口，例如 8000
EXPOSE 5000

# 设置环境变量，如果需要
ENV PYTHONUNBUFFERED=1

# 启动应用程序
CMD ["python", "app.py"]
