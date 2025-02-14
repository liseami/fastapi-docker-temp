#!/bin/bash
set -e

# 数据库初始化
 python /WORKDIR/app/backend_pre_start.py
 alembic upgrade head
 python /WORKDIR/app/initial_data.py

# # 计算总 worker 数
 CORES=$(nproc)
 WORKERS_PER_CORE=${WORKERS_PER_CORE:-1}  # 如果未设置，默认为1
 WORKERS=$((CORES * WORKERS_PER_CORE))

# # 使用 logger.info 打印核心计算过程
 python /WORKDIR/app/log_info.py "CPU核心数: $CORES"
 python /WORKDIR/app/log_info.py "每个核心的worker数: $WORKERS_PER_CORE"
 python /WORKDIR/app/log_info.py "总worker数: $WORKERS"

# # 启动应用
 if [ "$ENVIRONMENT" = "production" ] || [ "$ENVIRONMENT" = "staging" ]; then
     python /WORKDIR/app/log_info.py "在生产或暂存环境中启动应用，使用 $WORKERS 个workers"
     exec uvicorn app.main:app --host 0.0.0.0 --port 8888 --workers $WORKERS
 else
 # 本地开发模式
     python /WORKDIR/app/log_info.py "在开发环境中启动应用，启用热重载模式"
     exec uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
 fi