"""测试backup_py模块。"""

import os
import time
import pytest

from backup_py.main import cleanup_old_backups, create_backup


def test_create_backup(tmp_path):
    """测试创建备份。"""
    source = tmp_path / "source"
    source.mkdir()
    (source / "test.txt").write_text("hello")

    backup_dir = tmp_path / "backups"
    result = create_backup(str(source), str(backup_dir))

    assert os.path.exists(result)
    assert result.endswith(".tar.gz")
    assert os.path.getsize(result) > 0


def test_create_backup_creates_backup_dir(tmp_path):
    """测试备份目录自动创建。"""
    source = tmp_path / "source"
    source.mkdir()
    (source / "test.txt").write_text("hello")

    backup_dir = tmp_path / "nonexistent" / "backups"
    create_backup(str(source), str(backup_dir))

    assert backup_dir.exists()


def test_cleanup_old_backups(tmp_path):
    """测试清理旧备份。"""
    backup_dir = tmp_path / "backups"
    backup_dir.mkdir()

    # 创建新文件
    new_file = backup_dir / "backup_new.tar.gz"
    new_file.touch()

    # 创建旧文件（设为8天前）
    old_file = backup_dir / "backup_old.tar.gz"
    old_file.touch()
    eight_days_ago = time.time() - 8 * 24 * 3600
    os.utime(old_file, (eight_days_ago, eight_days_ago))

    deleted = cleanup_old_backups(str(backup_dir), keep_days=7)

    assert len(deleted) == 1
    assert str(old_file) in deleted
    assert not old_file.exists()
    assert new_file.exists()


def test_cleanup_no_old_backups(tmp_path):
    """测试没有旧备份时返回空。"""
    backup_dir = tmp_path / "backups"
    backup_dir.mkdir()

    (backup_dir / "backup_new.tar.gz").touch()

    deleted = cleanup_old_backups(str(backup_dir), keep_days=7)

    assert len(deleted) == 0


def test_cleanup_nonexistent_dir():
    """测试目录不存在时返回空。"""
    deleted = cleanup_old_backups("/nonexistent/path", keep_days=7)
    assert len(deleted) == 0


def test_my_first_test():
    """我的第一个测试。"""
    assert 1 + 1 == 2

@pytest.mark.parametrize("keep_days, expected_count", [
    (7, 1),      # 保留7天，删除1个（8天前）
    (10, 0),     # 保留10天，不删除
    (1, 1),      # 保留1天，删除1个
])
def test_cleanup_with_param(tmp_path, keep_days, expected_count):
    """参数化测试清理功能。"""
    backup_dir = tmp_path / "backups"
    backup_dir.mkdir()

    # 创建一个8天前的文件
    old_file = backup_dir / "backup_old.tar.gz"
    old_file.touch()
    eight_days_ago = time.time() - 8 * 24 * 3600
    os.utime(old_file, (eight_days_ago, eight_days_ago))

    deleted = cleanup_old_backups(str(backup_dir), keep_days=keep_days)

    assert len(deleted) == expected_count