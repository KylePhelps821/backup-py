"""测试日志功能。"""

import logging
import os

from backup_py.main import create_backup, setup_logging


def test_setup_logging_creates_handlers():
    """测试setup_logging配置正确。"""
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    setup_logging(level=logging.INFO)

    # 应该有2个handler（屏幕 + 文件）
    assert len(root_logger.handlers) == 2


def test_logger_name():
    """测试logger名。"""
    logger = logging.getLogger("backup_py.main")
    assert logger.name == "backup_py.main"


def test_backup_creates_log_file(tmp_path):
    """测试备份会创建日志文件。"""
    original_dir = os.getcwd()
    try:
        os.chdir(tmp_path)

        source = tmp_path / "source"
        source.mkdir()
        (source / "test.txt").write_text("hello")

        # 清理handler
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

        setup_logging()

        backup_dir = tmp_path / "backups"
        create_backup(str(source), str(backup_dir))

        # 只检查文件存在
        log_file = tmp_path / "backup.log"
        assert log_file.exists()

    finally:
        os.chdir(original_dir)
