.PHONY: format lint test all clean install

# 一键全部
all: format lint test

# 格式化代码
format:
	black src/ tests/
	ruff check --fix src/ tests/

# 代码检查
lint:
	ruff check src/ tests/

# 运行测试
test:
	pytest -v

# 测试覆盖率
cov:
	pytest --cov=backup_py --cov-report=term-missing

# 清理缓存
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +

# 安装
install:
	pip install -e ".[dev]"
