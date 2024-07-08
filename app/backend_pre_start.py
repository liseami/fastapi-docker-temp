

# 每次启动时连接数据库并且自动重试


from sqlalchemy import Engine
from sqlmodel import Session, select
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed
# from app.third_part.logsnag import LogSNAG
from app.core.db import engine
from app.core.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init(db_engine: Engine) -> None:
    try:
        with Session(db_engine) as session:
            # Try to create session to check if DB is awake
            session.exec(select(1))
            logger.info("✅——————数据库连接正常")
    except Exception as e:
        logger.error(e)
        logger.info("❌数据库连失败，等待重试...")
        logger.info(f"当前数据库地址{settings.SQLALCHEMY_DATABASE_URI}")
        raise e


def main() -> None:
    logger.info("🔗——————开始数据库连接")
    init(engine)
    logger.info("✅——————完成数据库连接")
    # LogSNAG.get_instance().service_init_success()


if __name__ == "__main__":
    main()
