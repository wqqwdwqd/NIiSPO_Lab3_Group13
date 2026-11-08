# 使用官方 Python 基础镜像
FROM python:3.12-slim
# 指定容器内工作目录
WORKDIR /app
# 先复制依赖列表并安装，利用 Docker 构建缓存
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
# 复制 Flask 应用源代码
COPY app.py ./
# 容器对内监听 5000 端口
EXPOSE 5000
# 不缓存 Python 输出，方便检查日志
ENV PYTHONUNBUFFERED=1
# 启动应用
CMD ["python", "app.py"]
