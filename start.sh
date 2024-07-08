#!/bin/bash
set -e

# 启动数据库
python /app/app/backend_pre_start.py
# 运行数据库迁移
alembic upgrade head
# 初始化数据库
python /app/app/initial_data.py
# 启动应用
exec uvicorn app.main:app --reload --host 0.0.0.0 --port 80