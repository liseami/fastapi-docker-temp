# 使用阿里云镜像仓库的 Python 3.10 基础镜像
FROM registry.cn-hangzhou.aliyuncs.com/mindbook/python:3.10 

# 设置工作目录为 /app/
WORKDIR /WORKDIR/

# 使用阿里云镜像源安装 Poetry 包管理工具
RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ poetry

# 复制项目依赖文件到容器中的 /app 目录
COPY ./poetry.lock ./pyproject.toml /WORKDIR/

# 配置 Poetry 源并重新生成 lock 文件
RUN poetry config virtualenvs.create false && \
    poetry source add --priority=primary aliyun https://mirrors.aliyun.com/pypi/simple/ && \
    poetry lock --no-update 

# 配置 Poetry 源并安装依赖
RUN poetry install --no-interaction --no-ansi

# 复制应用程序代码到容器
COPY ./app /WORKDIR/app

# 复制数据库迁移配置文件
COPY ./alembic.ini /WORKDIR/

# 复制应用启动脚本
COPY start.sh /WORKDIR/

# 复制环境配置文件
COPY .env /WORKDIR/app

# 设置 PYTHONPATH 环境变量
ENV PYTHONPATH=/WORKDIR

# 赋予启动脚本执行权限
RUN chmod +x /WORKDIR/start.sh
