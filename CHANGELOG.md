# Changelog

本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [0.2.0] - 2026-10-17

### 新增
- Dockerfile 多阶段构建（镜像体积从 199MB 减小到 150MB）
- Docker Compose 配置（环境变量 + 命名卷）
- 镜像发布到 Docker Hub (`kylephelps/backup-py:v2`)
- 环境变量支持（`.env` 文件）
- 数据持久化（命名卷）

### 修改
- `main.py` 的 `parse_args` 支持环境变量作为默认值
- 移除 `__init__.py` 的循环导入警告

### 文档
- README 添加 Docker Hub 使用说明
- 添加 GitHub Actions 和 Docker 徽章

## [0.1.0] - 2026-10-10

### 新增
- 自动打包备份目录
- 文件名带UTC时间戳归档
- 清理7天前的旧备份
- 日志记录（屏幕 + 文件）
- 命令行参数支持（-s/-b/-k/-v）
- 完整的单元测试（36个）
- 类型注解 + mypy 检查
- 代码格式化（black）+ 检查（ruff）

### 技术栈
- Python 3.10+
- pytest + freezegun
- mypy
- black + ruff