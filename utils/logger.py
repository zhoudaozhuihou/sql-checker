from loguru import logger
import os
import sys
from pathlib import Path

# 创建日志目录
log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(exist_ok=True)

# 配置日志
def setup_logger():
    # 移除默认的控制台输出
    logger.remove()
    
    # 添加文件输出
    log_file = log_dir / "sql_check.log"
    logger.add(
        log_file,
        rotation="10 MB",  # 当日志文件达到10MB时轮转
        retention="1 month",  # 保留1个月的日志
        compression="zip",  # 压缩旧的日志文件
        level="INFO",  # 日志级别
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        enqueue=True,  # 异步写入
        encoding="utf-8"
    )
    
    # 添加控制台输出（可选，用于开发调试）
    logger.add(
        sys.stderr,
        level="INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True
    )

# 导出logger实例供其他模块使用
setup_logger()