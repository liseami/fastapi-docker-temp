import multiprocessing
import logging
from sqlmodel import Session, create_engine, select
from app.core.config import settings
from app.models.table import User
from app.crud.UserCRUD import UserCRUD


def create_database_engine():
    """创建数据库引擎实例

    计算最佳连接池配置并创建SQLAlchemy引擎。

    说明:
    1. CPU核心数计算:
       - 获取CPU核心数并乘以2,这样可以充分利用CPU超线程
       - workers数等于CPU核心数,确保每个worker都有对应的CPU资源

    2. 连接池配置:
       - 设置最大数据库连接数为500,这是PostgreSQL的推荐值
       - pool_size = 最大连接数 ÷ (workers × 2)
         原因:每个worker都需要连接池,除以2是为了预留buffer
       - max_overflow设为pool_size,在需要时可以翻倍扩容

    3. 超时设置:
       - pool_timeout=30秒,防止连接长时间占用

    Returns:
        SQLAlchemy engine实例
    """
    # 1. 计算CPU和workers
    cpu_count = multiprocessing.cpu_count() * 2
    workers = cpu_count
    max_db_conn = 500  # PostgreSQL推荐的最大连接数

    # 2. 计算连接池参数
    pool_size = max_db_conn // (workers * 2)  # 每个worker预留足够连接
    max_overflow = pool_size  # 允许连接池翻倍扩容

    # 3. 创建引擎
    engine = create_engine(
        str(settings.SQLALCHEMY_DATABASE_URI),
        pool_size=pool_size,
        max_overflow=max_overflow,
        pool_timeout=30
    )

    return engine


# 创建全局引擎实例
engine = create_database_engine()


def init_db(session: Session) -> None:
    """初始化数据库并创建超级用户。

    Args:
        session: 数据库会话实例
    """
    logger = logging.getLogger(__name__)
    logger.info("初始化数据库")

    user = session.exec(
        select(User)
        .where(User.phone_number == settings.FIRST_SUPERUSER_PHONE_NUMBER)
    ).first()

    if not user and settings.FIRST_SUPERUSER:
        logger.info(f"创建超级用户: {settings.FIRST_SUPERUSER}")
        try:
            super_user = UserCRUD(session).create_super_user(
                settings.FIRST_SUPERUSER_PHONE_NUMBER,
                settings.FIRST_SUPERUSER,
                settings.FIRST_SUPERUSER_PASSWORD
            )
            logger.info(f"超级用户创建成功: {super_user.username}")
        except Exception as e:
            logger.error(f"创建超级用户失败: {str(e)}")
    if user:
        logger.info(f"超级用户已存在: {user.username}")
