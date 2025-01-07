"""日志记录工具模块。

该模块提供了简单的日志记录功能,可以通过命令行参数记录消息。

典型用法:
    python log_info.py "要记录的消息"

属性:
    logger: 日志记录器实例
"""

import logging
import sys
from typing import NoReturn

# 配置根日志记录器
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def log_message(message: str) -> None:
    """记录一条信息级别的日志消息。

    Args:
        message: 要记录的消息文本
    """
    logger.info(f"📝 {message}")


def main() -> NoReturn:
    """主函数,处理命令行参数并记录日志。

    从命令行参数获取要记录的消息。如果没有提供参数,
    则记录错误并退出。
    """
    if len(sys.argv) < 2:
        logger.error("❌ 请提供要记录的消息作为命令行参数")
        sys.exit(1)
    message = sys.argv[1]
    log_message(message)


if __name__ == "__main__":
    main()
