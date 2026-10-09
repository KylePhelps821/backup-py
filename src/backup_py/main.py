"""自动备份脚本（Python版）。

功能：
1. 打包备份指定目录
2. 文件名带日期归档
3. 清理7天前的旧备份
4. 日志记录
5. 支持命令行参数
"""

import argparse
import logging
import os
import tarfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

# ---------- 配置日志 ----------
logger = logging.getLogger(__name__)


def setup_logging(level: int = logging.INFO) -> None:
    """配置日志。

    Args:
        level: 日志级别
    """
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 屏幕handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    # 文件handler
    log_file = Path("backup.log")
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # 配置root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)


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

    logger.info("开始打包：%s", source.name)

    with tarfile.open(backup_file, "w:gz") as tar:
        tar.add(source, arcname=source.name)

    logger.info("打包完成：%s", backup_file.name)
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
        logger.debug("备份目录不存在：%s", backup_dir)
        return []

    cutoff = datetime.now(timezone.utc) - timedelta(days=keep_days)
    deleted = []

    for f in backup.glob("backup_*.tar.gz"):
        mtime = datetime.fromtimestamp(f.stat().st_mtime, tz=timezone.utc)
        if mtime < cutoff:
            logger.info("删除旧备份：%s", f.name)
            f.unlink()
            deleted.append(str(f))

    return deleted


def parse_args() -> argparse.Namespace:
    """解析命令行参数。

    Returns:
        解析后的参数命名空间
    """
    parser = argparse.ArgumentParser(description="自动备份工具")
    parser.add_argument(
        "-s",
        "--source",
        default="~/projects/backup_script/source_data",
        help="要备份的源目录",
    )
    parser.add_argument(
        "-b",
        "--backup",
        default="~/projects/backup-py/backups",
        help="备份存放目录",
    )
    parser.add_argument(
        "-k",
        "--keep-days",
        type=int,
        default=7,
        help="保留天数（默认7天）",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="显示调试信息",
    )
    return parser.parse_args()


def main() -> None:
    """主函数入口。"""
    args = parse_args()

    level = logging.DEBUG if args.verbose else logging.INFO
    setup_logging(level=level)

    source = os.path.expanduser(args.source)
    backup = os.path.expanduser(args.backup)

    logger.info("=" * 50)
    logger.info("备份工具启动")
    logger.info("源目录：%s", source)
    logger.info("备份目录：%s", backup)
    logger.info("保留天数：%d", args.keep_days)
    logger.info("=" * 50)

    if not os.path.isdir(source):
        logger.error("源目录不存在：%s", source)
        return

    try:
        backup_file = create_backup(source, backup)
        size = os.path.getsize(backup_file) / 1024
        logger.info("备份成功：%s (%.1f KB)", os.path.basename(backup_file), size)
    except Exception:
        logger.exception("备份失败")
        return

    deleted = cleanup_old_backups(backup, keep_days=args.keep_days)
    if deleted:
        logger.info("清理了 %d 个旧备份", len(deleted))
        for f in deleted:
            logger.debug("   - %s", os.path.basename(f))
    else:
        logger.info("没有需要清理的旧备份")

    logger.info("备份完成！")


if __name__ == "__main__":
    main()
