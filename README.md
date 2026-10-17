# backup-py

![CI](https://github.com/KylePhelps821/backup-py/actions/workflows/ci.yml/badge.svg)
![Docker Pulls](https://img.shields.io/docker/pulls/kylephelps/backup-py)
![Docker Image Size](https://img.shields.io/docker/image-size/kylephelps/backup-py)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.10+-blue)

自动备份脚本（Python版）。

## 功能

- 打包备份指定目录
- 文件名带日期归档（UTC时间戳）
- 清理7天前的旧备份
- 日志记录（同时输出到屏幕和文件）
- 支持命令行参数与环境变量
- 完整的单元测试与 Docker 部署支持

## 本地安装与开发

```bash
# 克隆项目
git clone git@github.com:KylePhelps821/backup-py.git
cd backup-py

# 创建虚拟环境并安装依赖
python3 -m venv venv
source venv/bin/activate
pip install -e ".[dev]"