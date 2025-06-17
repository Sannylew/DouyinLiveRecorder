FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV TZ=Asia/Shanghai

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements_webui.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements_webui.txt

# 复制应用代码
COPY . .

# 创建必要目录
RUN mkdir -p config downloads logs web/static

# 设置权限
RUN chmod +x start_webui.py app.py

# 暴露端口
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/status || exit 1

# 启动命令
CMD ["python", "app.py"]
