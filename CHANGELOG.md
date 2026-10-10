# Changelog

本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

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
