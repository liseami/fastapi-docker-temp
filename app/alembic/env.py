import os
import logging
from app.models.table import SQLModel
from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool


# 导入必要的模块

# 从配置中获取 Alembic 配置对象
config = context.config

# 解释用于 Python 日志记录的配置文件。
# 这行设置了日志记录器。
fileConfig(config.config_file_name)

# 获取logger实例
logger = logging.getLogger("alembic")

target_metadata = SQLModel.metadata


# 从配置中获取其他需要的值，根据 env.py 的需要定义
# my_important_option = config.get_main_option("my_important_option")
# ... 等等。


# docker中运行，应当连接的是host.docker.internal
# IDE中，执行迁移，应当使用localhost
# 根据运行环境选择不同的服务器地址
def is_running_in_docker() -> bool:
    return os.getenv("RUNINDOCKER", "False").lower() == "true"


def get_url():
    # 获取数据库连接 URL，在开发中或者在docker中进行迁移工作
    user = os.getenv("POSTGRES_USER", "")
    password = os.getenv("POSTGRES_PASSWORD", "")

    # 根据运行环境选择不同的服务器地址
    if is_running_in_docker():
        server = os.getenv("POSTGRES_SERVER", "")
        # docker环境使用的本地连接地址 host.docker.internal
    else:
        server = "localhost"
        # 本地开发环境使用 localhost

    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "")
    return f"postgresql+psycopg://{user}:{password}@{server}:{port}/{db}"


def run_migrations_offline():
    logger.info("数据库迁移: 以'离线'模式运行迁移。")
    logger.info(f"数据库迁移: RUNINDOCKER环境变量值为: {os.getenv('RUNINDOCKER', '')}")
    logger.info(f"数据库迁移: 是否在Docker中运行: {is_running_in_docker()}")
    logger.info(f"数据库迁移: 数据库连接URL为: {get_url()}")
    """以'离线'模式运行迁移。

    这将配置上下文仅包含 URL
    而不是 Engine，尽管在这里也可以接受 Engine。
    通过跳过 Engine 创建，我们甚至不需要 DBAPI 可用。

    在这里对 context.execute() 的调用会将给定的字符串发送到脚本输出。

    """
    # 获取数据库连接 URL
    url = get_url()
    # 配置上下文
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, compare_type=True
    )

    with context.begin_transaction():
        # 执行迁移
        context.run_migrations()


def run_migrations_online():
    logger.info("数据库迁移: 以'在线'模式运行迁移。")
    logger.info(f"数据库迁移: RUNINDOCKER环境变量值为: {os.getenv('RUNINDOCKER', '')}")
    logger.info(f"数据库迁移: 是否在Docker中运行: {is_running_in_docker()}")
    logger.info(f"数据库迁移: 数据库连接URL为: {get_url()}")
    """以'在线'模式运行迁移。

    在这种情况下，我们需要创建一个 Engine
    并将一个连接与上下文关联起来。

    """
    # 从配置中获取配置项
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    # 创建可连接的 Engine
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        # 配置上下文
        context.configure(
            connection=connection, target_metadata=target_metadata, compare_type=True
        )
        with context.begin_transaction():
            # 执行迁移
            context.run_migrations()


# 检查是否处于离线模式
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
