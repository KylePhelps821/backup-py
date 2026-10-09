"""backup_py - 自动备份工具。"""

from backup_py.main import cleanup_old_backups, create_backup

__version__ = "0.1.0"
__all__ = ["cleanup_old_backups", "create_backup"]
