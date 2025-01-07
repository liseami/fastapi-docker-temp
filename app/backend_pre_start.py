"""数据库预启动检查模块

在应用启动前验证数据库连接,实现自动重试机制。
"""

from sqlalchemy import Engine
from sqlmodel import Session, select
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed
from app.core.db import engine
from app.core.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 重试配置
max_tries = 60 * 5  # 5分钟,每秒一次
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init(db_engine: Engine) -> None:
    """验证数据库连接

    Args:
        db_engine: SQLAlchemy数据库引擎

    Raises:
        Exception: 数据库连接失败
    """
    try:
        with Session(db_engine) as session:
            session.exec(select(1))
            logger.info("✅——————数据库连接正常")
    except Exception as e:
        logger.error(e)
        logger.info("❌数据库连失败，等待重试...")
        logger.info(f"当前数据库地址{settings.SQLALCHEMY_DATABASE_URI}")
        raise e


def main() -> None:
    """执行数据库连接初始化"""
    logger.info("🔗——————开始数据库连接")
    init(engine)
    logger.info("✅——————完成数据库连接")


if __name__ == "__main__":
    main()
