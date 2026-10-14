# ============================================
# backup-py 的 Dockerfile
# 构建：docker build -t backup-py:v1 .
# 运行：docker run --rm backup-py:v1
# ============================================

# 1. 基础镜像
FROM python:3.10-slim

# 2. 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    TZ=UTC

# 3. 设置工作目录
WORKDIR /app

# 4. 先复制依赖文件（利用缓存）
COPY pyproject.toml README.md ./

# 5. 复制源代码
COPY src/ ./src/

# 6. 安装项目（可编辑模式不适用容器，用普通模式）
RUN pip install --upgrade pip && \
    pip install .

# 7. 创建默认备份目录
RUN mkdir -p /app/backups /app/data

# 8. 声明数据卷（可选）
VOLUME ["/app/data", "/app/backups"]

# 9. 容器启动时执行的命令
ENTRYPOINT ["python", "-m", "backup_py.main"]
CMD ["-s", "/app/data", "-b", "/app/backups"]