# ============================================
# backup-py - 多阶段构建
# ============================================

# ---------- 阶段1：构建 ----------
FROM python:3.10-slim AS builder

WORKDIR /app

# 安装构建依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 先复制依赖文件（利用缓存）
COPY pyproject.toml README.md ./
COPY src/ ./src/

# 安装到指定目录（方便复制）
RUN pip install --upgrade pip && \
    pip install --prefix=/install .

# ---------- 阶段2：运行 ----------
FROM python:3.10-slim

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TZ=UTC

# 从构建阶段复制已安装的包
COPY --from=builder /install /usr/local

# 设置工作目录
WORKDIR /app

# 创建目录
RUN mkdir -p /app/backups /app/data

# 声明数据卷
VOLUME ["/app/data", "/app/backups"]

# 启动命令
ENTRYPOINT ["python", "-m", "backup_py.main"]
CMD ["-s", "/app/data", "-b", "/app/backups"]