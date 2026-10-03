"""自动备份脚本（Python版）。

功能：
1. 打包备份指定目录
2. 文件名带日期归档
3. 清理7天前的旧备份
"""

import os
import tarfile
from datetime import datetime, timedelta, timezone
from pathlib import Path


def create_backup(source_dir: str, backup_dir: str) -> str:
    """打包备份目录，返回备份文件路径。

    Args:
        source_dir: 要备份的源目录
        backup_dir: 备份存放目录

    Returns:
        备份文件的完整路径
    """
    source = Path(source_dir)
    backup = Path(backup_dir)
    backup.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    backup_file = backup / f"backup_{timestamp}.tar.gz"

    with tarfile.open(backup_file, "w:gz") as tar:
        tar.add(source, arcname=source.name)

    return str(backup_file)


def cleanup_old_backups(backup_dir: str, keep_days: int = 7) -> list[str]:
    """清理N天前的旧备份。

    Args:
        backup_dir: 备份目录
        keep_days: 保留天数

    Returns:
        被删除的文件列表
    """
    backup = Path(backup_dir)
    if not backup.exists():
        return []

    cutoff = datetime.now(timezone.utc) - timedelta(days=keep_days)
    deleted = []

    for f in backup.glob("backup_*.tar.gz"):
        mtime = datetime.fromtimestamp(f.stat().st_mtime, tz=timezone.utc)
        if mtime < cutoff:
            f.unlink()
            deleted.append(str(f))

    return deleted


def main() -> None:
    """主函数入口。"""
    source = os.path.expanduser("~/projects/backup_script/source_data")
    backup = os.path.expanduser("~/projects/backup-py/backups")

    print("=" * 50)
    print(
        f"备份工具启动：{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC"
    )
    print("=" * 50)
    print(f"源目录：{source}")
    print(f"备份目录：{backup}")
    print()

    if not os.path.isdir(source):
        print(f"❌ 错误：源目录不存在：{source}")
        return

    backup_file = create_backup(source, backup)
    size = os.path.getsize(backup_file) / 1024
    print(f"✅ 备份成功：{os.path.basename(backup_file)}")
    print(f"   大小：{size:.1f} KB")

    deleted = cleanup_old_backups(backup)
    if deleted:
        print(f"🧹 清理了 {len(deleted)} 个旧备份")
        for f in deleted:
            print(f"   - {os.path.basename(f)}")
    else:
        print("没有需要清理的旧备份")

    print()
    print("=" * 50)
    print("备份完成！")


if __name__ == "__main__":
    main()
